# Optical-Character-Recognition-Project
Extracting Business Card Data with OCR
# Overview
  OCR stands for Optical Character Recognition. It's a technology that converts images of text into a digital format that computers can understand and manipulate.

Here's a breakdown of OCR:
Input: An image containing text, like a scanned document, photo of a document, or even a screenshot.
Process: The OCR software analyzes the image, identifying and recognizing individual characters (letters, numbers, symbols).
Output: The extracted text in a digital format, often editable text in a document or a data file.

This makes OCR useful for various tasks, such as:
Converting scanned documents into searchable PDFs.
Extracting text from images for further processing or analysis.
Making historical documents with handwritten text accessible digitally.

  The aim of this project is to create a streamlit application that uses easy-ocr to extract details from business cards .The extracted information will then be 
displayed in the application's graphical user interface (GUI). In addition, the application should allow users to save the extracted information into a database 
along with the uploaded business card image.

# Required Libraries 
1.Pandas  2.Streamlit  3.Regular Expression  4.Pillow(PIL)  5.Image and ImageDraw from PIL  6.Numpy  7.EasyOCR  8.mysql.connector

# Workflow
* The application has 3 pages namely "Home","Correction","Server".Default is "Home" page.
* On launching the application you will find the upload button on the sidebar in the Home page, Click and upload the business card image.
* You will find the uploaded image in the UI below it you will see extract button, click to extract the card details such as the company name, card holder
  name, designation, mobile number, email address, website URL, area, city, state, and pin code.
* Below the extracted details you will find Edit button. Click it, to switch the screen to the "Correction" page.
* Now edit the extracted information and click update button below. On clicking you will see a table below along with the updated information.
* Now click the Upload-to-Mysql button below the updated table , the page will switch to "Server" page then the data will be uploaded to the Mysql databases and display the output.You 
  cant store duplicate values in databases.
* In the Server page you will find a tickbox on the sidebar named "View DataBase". On clicking it, you will see the data stored in the Mysql database. This option is to check the data 
  stored in the database.
 
