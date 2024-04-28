from flask import Flask, render_template, request, jsonify, redirect, session, url_for
import pandas as pd
import os
import datetime
import json
import sys
import ast
import logging
from flask_mail import Mail, Message 
from scripts.helper import *
import shutil
app = Flask(__name__)
app.secret_key = os.urandom(24) 
logging.basicConfig(level=logging.DEBUG)
now = datetime.datetime.now().strftime("%d %B, %Y %H:%M:%S")
mail = Mail(app) # instantiate the mail class 
   
# configuration of mail 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'yourmail@gmail.com'
app.config['MAIL_PASSWORD'] = 'yourpassword'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 

@app.route('/download')
def download():
      download_path = session.get('download_path') 
      
      return render_template(r'download.html', download_path=download_path, timestamp = now, class_name = session.get('classname'))
@app.route('/sendmail')
def sendmail():
    download_path = session.get('download_path') 
    download_path = os.path.join('static', download_path)
    app.logger.info(download_path)
    msg = Message( 
                'Hello', 
                sender ='yourmail@gmail.com', 
                recipients = ['tomail@gmail.com'] 
               ) 
    with app.open_resource(download_path, mode='rb') as fp:
            msg.attach(download_path, 'application/pdf', fp.read())
    msg.body = 'Attendance - ' + str(now) + ' Absentees copy'
    try:
        mail.send(msg)
        return render_template('success.html')  # Display success message (optional)
    except Exception as e:
        # Handle potential errors gracefully (e.g., log the error, display user-friendly message)
        print(f"Error sending email: {e}")
        return render_template('error.html', error_message="An error occurred while sending email.")  # Display error message (optional)

@app.route('/error')
def error_page():
    return render_template('error.html')
@app.route('/submit_deleted_items', methods=['POST'])
def submit_deleted_items():
  # app.logger.info('INSIDE SUBMIT DELETED ITEMS')
  deleted_items = request.form.getlist('deleted_items')  # Access the data

  deleted_items_list = ast.literal_eval(deleted_items[0])
  # app.logger.info(deleted_items_list)
  name = []
  regno = []
  absentees = pd.DataFrame()
  for i in deleted_items_list:
    #   app.logger.info('tYPE', type(i), "whole", i)
      name.append(i['name'])
      regno.append(i['regno'])
  absentees['name'] = name
  absentees['regno'] = regno
  
  data_dir = "static/data"
  class_name = session.get('classname')
  class_dir = os.path.join(data_dir, class_name)
  # timestamp = datetime.datetime.now()
  absent_path = class_name+"-"+str(now[:30])+"_absentees"+".csv"
  absent_path = absent_path.replace(' ','_')
  absent_path = absent_path.replace(':', '_')
  absent_path = absent_path.replace(',','_')
  absentees_path = os.path.join(class_dir,absent_path)
  absentees.to_csv(absentees_path)
  formatted_absentees_path = "data" + absentees_path.split("data")[-1]
  formatted_absentees_path = formatted_absentees_path.replace('\\', '/')
  session['download_path'] = formatted_absentees_path
#   absentees.to_csv(formatted_absentees_path)
#   return jsonify({'message' : absentees_path})
  # app.logger.info('Rendering now')

  # return render_template(r'download.html', download_path=formatted_absentees_path)
  return redirect(url_for('download'))

@app.route('/delclass', methods = ['POST'])
def delclass():
  class_name = request.form.get('classname')
  class_dir = os.path.join('static/data', class_name)
  
  try:
    shutil.rmtree(class_dir)
    return jsonify({'message':f"Class '{class_name}' and its contents have been successfully deleted."}), 200
  except Exception as e:
    return jsonify({"error": f"{e}"}), 400
@app.route('/myclass', methods=['POST'])  # Handle both GET and POST requests (if needed)
def myclass():
    # Extract class name from the query parameter
    class_name = request.form.get('classname')  # Use request.args for GET requests
    
    # Error handling (optional): Handle cases where classname is missing
    # if class_name is None:
    #     return redirect(url_for('error_page'))  # Redirect to an error page if no classname found
    df = pd.read_csv(r'static/data/{}/default.csv'.format(class_name))  # Format the path using f-strings
    data = df.to_dict('records')
    timestamp = datetime.datetime.now()  # Get current timestamp
    session['classname'] =  class_name
    return render_template('attendance.html', data=data, timestamp=timestamp, class_name = class_name)
    # Access and process data for the specified class
    # try:
    #     df = pd.read_csv(r'static/data/{}/default.csv'.format(class_name))  # Format the path using f-strings
    #     data = df.to_dict('records')
    #     timestamp = datetime.datetime.now()  # Get current timestamp

    #     return render_template('attendance.html', data=data, timestamp=timestamp)
    # except FileNotFoundError:
    #     # Handle case where the data file is not found
    #     return redirect(url_for('error_page'))
@app.route('/addclass', methods=['POST'])
def addclass():
    class_name = request.form.get('class_name')

    # Check if class directory already exists
    class_path = os.path.join("static/data", class_name)
    if os.path.exists(class_path):
        return jsonify({"error": "Class already exists. Please give a unique name."}), 400

    # Create class directory if it does not exist
    os.makedirs(class_path, exist_ok=True)

    # Save the uploaded Excel file as 'default.xlsx'
    excel_file = request.files.get('excel_file')
    if excel_file:
        excel_path = os.path.join(class_path, 'list.xlsx')
        excel_file.save(excel_path)
        extract_images(excel_path, class_name)
    return jsonify({"message": f"New class '{class_name}' added successfully."}), 200

  
# Add routes for other functionalities (e.g., attendance tracking)
@app.route('/')
def index():
  class_data_path = "static/data"
  class_names = os.listdir(class_data_path)
  # app.logger.info(class_names)
  return render_template(r'myclasses.html', class_data = class_names)
if __name__ == '__main__':
    app.run(debug=True)
