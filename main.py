from tkinter import *
import ctypes,os,csv
from PIL import ImageTk, Image
import tkinter.messagebox as tkMessageBox
from tkinter.filedialog import askopenfilename
from my_functions import *
import os,webbrowser
from twilio.rest import Client

home = Tk()
home.title("Automatic Helmet Detection And panelizing system")

img = Image.open("images/home.png")
img = ImageTk.PhotoImage(img)
panel = Label(home, image=img)
panel.pack(side="top", fill="both", expand="yes")
if os.name == "nt":  # DPI awareness is a Windows-only API
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()

home.geometry("1920x1080+0+0")

file = ''

def browse():
    global file
    file = askopenfilename(initialdir=os.getcwd(), title="Select Image", filetypes=( ("video", ".mp4"),("video", ".MOV"),("video", ".mkv"),("image", ".png"),("image", ".jpg")))
    helmet()
def helmet():
    global file
    try:
        if file !='':
            fl = (file.split('.')[-1]).lower()
            val=['jpg','png']
            if fl not in val:
                source = file

                save_video = True # want to save video? (when video as source)
                show_video=True # set true when using video file
                save_img=False  # set true when using only image file to save the image
                # when using image as input, lower the threshold value of image classification

                #saveing video as output
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter('output.avi', fourcc, 20.0, frame_size)
                f = open('number.txt','w')
                f.write('')
                f.close()
                cap = cv2.VideoCapture(source)
                while(cap.isOpened()):
                        ret, frame = cap.read()
                        if ret == True:
                                frame = cv2.resize(frame, frame_size)  # resizing image
                                orifinal_frame = frame.copy()
                                frame, results = object_detection2(frame) 

                                rider_list = []
                                head_list = []
                                number_list = []

                                for result in results:
                                        x1,y1,x2,y2,cnf, clas = result
                                        if clas == 0:
                                                rider_list.append(result)
                                        elif clas == 1:
                                                head_list.append(result)
                                        elif clas == 2:
                                                number_list.append(result)

                                for rdr in rider_list:
                                        time_stamp = str(time.time())
                                        x1r, y1r, x2r, y2r, cnfr, clasr = rdr
                                        for hd in head_list:
                                                x1h, y1h, x2h, y2h, cnfh, clash = hd
                                                if inside_box([x1r,y1r,x2r,y2r], [x1h,y1h,x2h,y2h]): # if this head inside this rider bbox
                                                        try:
                                                                head_img = orifinal_frame[y1h:y2h, x1h:x2h]
                                                                helmet_present = img_classify(head_img)
                                                        except:
                                                                helmet_present[0] = None

                                                        if  helmet_present[0] == True: # if helmet present
                                                                frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0,255,0), 1)
                                                                frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                                                        elif helmet_present[0] == None: # Poor prediction
                                                                frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 255, 255), 1)
                                                                frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                                                        elif helmet_present[0] == False: # if helmet absent 
                                                                frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 0, 255), 1)
                                                                frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                                                                try:
                                                                        cv2.imwrite(f'riders_pictures/{time_stamp}.jpg', frame[y1r:y2r, x1r:x2r])
                                                                except:
                                                                        print('could not save rider')

                                                                for num in number_list:
                                                                        x1_num, y1_num, x2_num, y2_num, conf_num, clas_num = num
                                                                        if inside_box([x1r,y1r,x2r,y2r], [x1_num, y1_num, x2_num, y2_num]):
                                                                                try:
                                                                                        num_img = orifinal_frame[y1_num:y2_num, x1_num:x2_num]
                                                                                        cv2.imwrite(f'number_plates/{time_stamp}_{conf_num}.jpg', num_img)
                                                                                except:
                                                                                        print('could not save number plate')
                                                                                        
                                if save_video: # save video
                                        out.write(frame)
                                if save_img: #save img
                                        cv2.imwrite('saved_frame.jpg', frame)
                                if show_video: # show video
                                        frame = cv2.resize(frame, (900, 450))  # resizing to fit in screen
                                        cv2.imshow('Frame', frame)


                                if cv2.waitKey(1) & 0xFF == ord('q'):
                                        break
                                        
                        else:
                                break

                cap.release()
                cv2.destroyAllWindows()
                print('Execution completed')


            else:

                source = file

                save_video = True # want to save video? (when video as source)
                show_video=True # set true when using video file
                save_img=False  # set true when using only image file to save the image
                # when using image as input, lower the threshold value of image classification


                f = open('number.txt','w')
                f.write('')
                f.close()

                frame = cv2.imread(file)
                ret = True
                if ret == True:
                        frame = cv2.resize(frame, frame_size)  # resizing image
                        orifinal_frame = frame.copy()
                        frame, results = object_detection2(frame) 

                        rider_list = []
                        head_list = []
                        number_list = []

                        for result in results:
                                x1,y1,x2,y2,cnf, clas = result
                                if clas == 0:
                                        rider_list.append(result)
                                elif clas == 1:
                                        head_list.append(result)
                                elif clas == 2:
                                        number_list.append(result)

                        for rdr in rider_list:
                                time_stamp = str(time.time())
                                x1r, y1r, x2r, y2r, cnfr, clasr = rdr
                                for hd in head_list:
                                        x1h, y1h, x2h, y2h, cnfh, clash = hd
                                        if inside_box([x1r,y1r,x2r,y2r], [x1h,y1h,x2h,y2h]): # if this head inside this rider bbox
                                                try:
                                                        head_img = orifinal_frame[y1h:y2h, x1h:x2h]
                                                        helmet_present = img_classify(head_img)
                                                except:
                                                        helmet_present[0] = None

                                                if  helmet_present[0] == True: # if helmet present
                                                        frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0,255,0), 1)
                                                        frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                                                elif helmet_present[0] == None: # Poor prediction
                                                        frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 255, 255), 1)
                                                        frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                                                elif helmet_present[0] == False: # if helmet absent 
                                                        frame = cv2.rectangle(frame, (x1h, y1h), (x2h, y2h), (0, 0, 255), 1)
                                                        frame = cv2.putText(frame, f'{round(helmet_present[1],1)}', (x1h, y1h+40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1, cv2.LINE_AA)
                                                        try:
                                                                cv2.imwrite(f'riders_pictures/{time_stamp}.jpg', frame[y1r:y2r, x1r:x2r])
                                                        except:
                                                                print('could not save rider')

                                                        for num in number_list:
                                                                x1_num, y1_num, x2_num, y2_num, conf_num, clas_num = num
                                                                if inside_box([x1r,y1r,x2r,y2r], [x1_num, y1_num, x2_num, y2_num]):
                                                                        try:
                                                                                num_img = orifinal_frame[y1_num:y2_num, x1_num:x2_num]
                                                                                cv2.imwrite(f'number_plates/{time_stamp}_{conf_num}.jpg', num_img)
                                                                        except:
                                                                                print('could not save number plate')
                                                                                
                  
                        cv2.imshow('Frame', frame)


                        cv2.waitKey(0)
                       

    except:
        tkMessageBox.showinfo('Error','Please select video file')

def number():
    f = os.listdir('./number_plates')
    
    for i in f:
        j = os.getcwd()+'/number_plates//'+i
        
        webbrowser.open(j)

def helmetimage():
    f = os.listdir('./riders_pictures')
    
    for i in f:
        j = os.getcwd()+'/riders_pictures//'+i
        
        webbrowser.open(j)
        
def message():
    """Send an SMS for every detected plate found in the plate -> phone registry (number.csv).

    Twilio credentials are read from the environment, never from source code:
    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER (see .env.example).
    """
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    from_number = os.environ.get("TWILIO_FROM_NUMBER")
    if not (account_sid and auth_token and from_number):
        tkMessageBox.showerror("Twilio not configured", "Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN and TWILIO_FROM_NUMBER.")
        return
    client = Client(account_sid, auth_token)

    with open("number.txt", "r") as fh:
        detected = {line.strip() for line in fh.read().split("\n") if line.strip()}
    registry = {}
    with open("number.csv", "r", newline="") as fh:
        for row in csv.reader(fh):
            if len(row) == 2:
                registry[row[0]] = row[1]

    for plate in detected:
        match = next((key for key in registry if key.split(" ")[0] == plate), None)
        if match is None:
            continue  # plate not in the registry
        num = "+" + registry[match]
        try:
            client.messages.create(body=f"This message is regarding number plate {match}.", from_=from_number, to=num)
            tkMessageBox.showinfo("message", f"message sent to {num} regarding number plate {match}")
        except Exception as exc:  # network / Twilio errors are reported, not silently ignored
            tkMessageBox.showerror("SMS failed", f"Could not message {num}: {exc}")


photo = Image.open("images/1.png")
img2 = ImageTk.PhotoImage(photo)
b1=Button(home, highlightthickness = 0, bd = 0,activebackground="#EBE8E8", image = img2,command=browse)
b1.place(x=0,y=261)

photo = Image.open("images/2.png")
img3 = ImageTk.PhotoImage(photo)
b2=Button(home, highlightthickness = 0, bd = 0,activebackground="#EBE8E8", image = img3,command=helmetimage)
b2.place(x=0,y=386)

photo = Image.open("images/3.png")
img4 = ImageTk.PhotoImage(photo)
b3=Button(home, highlightthickness = 0, bd = 0,activebackground="#EBE8E8", image = img4,command=number)
b3.place(x=0,y=513)

photo = Image.open("images/4.png")
img5 = ImageTk.PhotoImage(photo)
b4=Button(home, highlightthickness = 0, bd = 0,activebackground="#EBE8E8", image = img5,command=message)
b4.place(x=0,y=638)

home.mainloop()
