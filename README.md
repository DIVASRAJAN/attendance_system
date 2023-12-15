# Attendance system
Automated attendance system using face recognition - deep learning

used a pre trained model for face recognition, VGG16 is used here.

videos taken and it converted into images and stored, formed dataset for model training ( codes are in videoToPhoto file)

created an interface using flask,HTML,CSS -HTML codes are in template folder and CSS code is in static folder

VGG16 model trained using created dataset. - model_training file

created few functions and it stored in module file

used MySQL as the database management system. mySQL queries are in mysql_queries file

Also incorporated printing attendance sheet of present students

and send automated emails to the absent candidates - absend_msg file

here is the link for trained model
https://drive.google.com/file/d/1fgxYm2PYPMXQB4eTRHULyeypsVAuxzpU/view?usp=drive_link

this trained model should be on the assets folder

and should create a csv file named data1 for saving the attendance sheet

also have a new_member folder for saving the images of newly adding candidates


and we manually train the model and change the model on the assets folder
