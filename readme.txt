# Automatic helmetless rider detection and penalizing system
In this  project it is extracting motorcycle license plates if the rider is not wearing a helmet and sending a penalty message.

In this project i am using yolv5 algorithm to detect rider, licence plate and riders head. Then using resnet50 image classifier, i classify wheather the rider is wearing a helmet or not. If not wearing a helmet then, it will save his licence plate number in a image folder, and also will capture rider image in a separate folder.Then it will send message to the registered mobile number of the license plate.
Step 1 : Install python 3.7 or above versions
Step2 : Install prerequisite python librarires
Pillow # PIL
opencv-python
torch
torchvision
numpy
tqdm
pandas
matplotlib
twilio
Step 3:In command promt change directory to the python program that is created then type "python main.py"
step 4:In this step program runs and a message is sent to the mobile number of the violator.




