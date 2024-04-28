# Easy Attendance

Easy Attendance is an application designed to assist professors and teachers in efficiently taking attendance.

## Getting Started

To get started with Easy Attendance, follow these simple steps:

1. **Clone the Repository**: Use the following command to clone the repository to your local machine:
   ```bash
   git clone https://github.com/Jayasreem05/easy_attendance.git

2. **Create a virtual environment**: Use the following command to create a virtual env in your local machine:
   ```bash
   cd easy_attendance
   python3 -m venv .venv

3. **Install Dependencies**: Activate the virtual environment and install the required dependencies using the provided requirements.txt file
   ```bash
   
   .venv\Scripts\activate      # For Windows
   pip install -r requirements.txt

4. **Update mail to customise**: Update lines [21](CODEBASE/app.py#L21), [22](CODEBASE/app.py#L22) and [39](CODEBASE/app.py#L39), [40](CODEBASE/app.py#L40) in [app.py](CODEBASE/app.py) with your custom mails.
   ```bash
   app.config['MAIL_USERNAME'] = 'yourmail@gmail.com' # mail server mail
   app.config['MAIL_PASSWORD'] = 'yourpassword' # app password, if gmail

   ```
   ```bash
   msg = Message( 
                'Hello', 
                sender ='yourmail@gmail.com', # mail server mail
                recipients = ['tomail@gmail.com'] # recipient mail - can add multiple mail ids in the list
               ) 

6. **Running the Code**: Go to the CODEBASE directory and run the app.py
   ```bash
   cd CODEBASE
   python app.py

7. **Usage**: Click the local server url and start using the app.



## License
This project is licensed under the MIT License.


   


