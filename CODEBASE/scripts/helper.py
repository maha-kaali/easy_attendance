#Importing the modules
import openpyxl
import os
from openpyxl_image_loader import SheetImageLoader
import pandas as pd

def create_dir(dir_path):
      if not os.path.exists(dir_path):
          os.makedirs(dir_path)
          print("Successfully created directory : ", dir_path)
      else:
          print("Directory already exists : ", dir_path)
    
def extract_images(path, class_name):
    #loading the Excel File and the sheet
    pxl_doc = openpyxl.load_workbook(path)
    # sheet = pxl_doc[class_name]
    sheet = pxl_doc.active
    
    #calling the image_loader
    image_loader = SheetImageLoader(sheet)
    
    #get the image (put the cell you need instead of 'A1')
    extracted_df = pd.DataFrame()
    regno = []
    name = []
    image_path = []
    data_dir = "static/data"
    
    class_dir = os.path.join(data_dir, class_name)
    # create_dir(class_dir)
    img_dir = os.path.join(class_dir, "images")
    create_dir(img_dir)
    
    for i in range(1, 28):
        cell = "A" + str(i)
        text = sheet[cell].value
        # print(text)
        regno.append(text.split(" ")[0])
        name.append(" ".join(text.split(" ")[1:]))
        
        cell = "B" + str(i)
        image = image_loader.get(cell)
        actual_path =os.path.join(img_dir, regno[-1]+".jpg")
        image.save(actual_path)

        image_path.append("data" + actual_path.split("data")[-1])
    
    extracted_df['regno'] = regno
    extracted_df['name'] = name
    extracted_df['img path'] = image_path
    extracted_df['img path'] = extracted_df['img path'].str.replace('\\', '/')
    
    print(extracted_df)
    extracted_df.to_csv(os.path.join(class_dir, "default.csv"), index = False)

#showing the image
# image.show()

#saving the image
# image.save('my_path/image_name.jpg')