from tkinter import *
from PIL import ImageTk, Image
import os,re
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import datetime
import raspiRFID
import raspiRFID2


handbrake_sensor = 29


showhide_flag = 0
grey_counter = 0
grey_flag = 0
Total_Fare = 1500
Total_Passenger = 300
Driver_Name = "Dela Cruz, Juan Paolo"

#initialization for RFID readers
shuttlePrice='5'
temp_DRIVERID='13'
RFID_reader1 = SimpleMFRC522()
RFID_reader2 = raspiRFID2.SimpleMFRC522a()
buzzer1=31
buzzer2=37
# GPIO.setup(buzzer1,GPIO.OUT)
# GPIO.setup(buzzer2,GPIO.OUT)

GPIO.setup(handbrake_sensor,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)

def is_wifi():
    wat = os.popen('iwgetid').read() ### RASPI ###
    watt = re.findall('"([^"]*)"',wat) ##FIND ENCLOSED IN ""##
    watt = ''.join(watt) ##CONVERT LIST TO STRING##

    # ipadd = os.popen('Netsh WLAN show interfaces').read() ### WINDOWS ###
    # x = ipadd.find('Profile                : ') + 25
    # watt = ipadd[x:].split(' ')[0]

    if watt == "thesisShuttle":
        replace = ImageTk.PhotoImage(Image.open("Images/yeswifi.png"))
    else:
        replace = ImageTk.PhotoImage(Image.open("Images/nowifi.png"))
        
    wifi_label.config(image=replace)
    wifi_label.image=replace
    window.after(5000, is_wifi)

def grey_toggle(channel):
    global grey_flag
    if(GPIO.input(handbrake_sensor)==GPIO.HIGH):
        grey_flag = 1
        main_frame.pack_forget()
        hist_frame.pack_forget()
        grey_frame.pack(expand=1,fill=BOTH)
        #grey_recent.config(text="")
    else:
        grey_flag = 0   
        grey_frame.pack_forget()
        main_frame.pack(expand=1,fill=BOTH)

GPIO.add_event_detect(handbrake_sensor,GPIO.RISING,callback=grey_toggle)

def grey_recent_student():
     rfid_uid,rfid_idnum = RFID_reader1.read_no_block()
     global grey_counter
     print(rfid_idnum)
     
     if(rfid_idnum!=None and grey_flag==1):
         grey_counter = 0
     
     if(grey_counter==40 and grey_flag==1):
         print(grey_counter)
         grey_counter = 0
         grey_recent.config(text="",anchor="w")
     elif(grey_counter<40 and grey_flag==1):
         grey_counter = grey_counter + 1
         grey_recent.config(text=rfid_idnum,anchor="w")
     
     window.after(100, grey_recent_student)

def recent_student():
    #check first RFID reader (RFID_reader1)
    rfid_uid, text = RFID_reader1.read_no_block()
    print("RFID1 UID="+string(rfid_uid))
    rfid_idNum=raspiRFID.checkUID(rfid_uid)
    print("IDNUM="+string(rfid_idNum))
    if(rfid_idNum!=None):
            if(rfid_idNum[1]==1):
                    transactionRecord= [(str(id),str(datetime.datetime.now()),str(rfid_idNum[0]),int(shuttlePrice),str(temp_DRIVERID))]
                    raspiRFID.inputTransactiontoDB(transactionRecord)
                    # raspiRFID.buzzSuccessful(buzzer1)
                    main_recent.config(text=rfid_idNum,anchor="w")
            else:
                    # raspiRFID.buzzNoBalance(buzzer1)
                    pass
    else:
            print('UID not in database')
            # raspiRFID.buzzNotInDB(buzzer1)

    #check seocnd RFID reader (RFID_reader2)
    rfid_uid2, text2 = RFID_reader2.read_no_block()
    print("RFID2 UID="+string(rfid_uid2))
    rfid_idNum2=raspiRFID.checkUID(rfid_uid2)
    print('IDNUM2='+string(rfid_idNum2))
    if(rfid_idNum2!=None):
            if(rfid_idNum2[1]==1):
                    transactionRecord= [(str(id),str(datetime.datetime.now()),str(rfid_idNum2[0]),int(shuttlePrice),str(temp_DRIVERID))]
                    raspiRFID.inputTransactiontoDB(transactionRecord)
                    # raspiRFID.buzzSuccessful(buzzer2)
                    main_recent.config(text=rfid_idNum2,anchor="w")
            else:
                    # raspiRFID.buzzNoBalance(buzzer2)
                    pass
    else:
            print('UID not in database')
            # raspiRFID.buzzNotInDB(buzzer2)

    window.after(100, recent_student)

def sync():
    print("Sync!")

def showhide(main_totalfare,main_totalpass):
    global showhide_flag
    if showhide_flag == 0:
        print("Hidden!")
        main_totalfare.config(text="Hidden")
        main_totalpass.config(text="Hidden")
        showhide_flag = 1
    elif showhide_flag == 1:
        print("Shown!")
        TTF = "₱"+str(Total_Fare)
        main_totalfare.config(text=TTF)
        main_totalpass.config(text=Total_Passenger)
        showhide_flag = 0
        
##### WINDOW #####
window = Tk()
window.geometry("848x480") #Size for Window
# window.overrideredirect(1) #Remove window border
window.resizable(False,False) #Prevent resize windows

##### FRAME ######
main_frame = Frame(window)
main_frame.pack(expand=1,fill=BOTH)

hist_frame = Frame(window)
hist_frame.pack_forget()

grey_frame = Frame(window)
grey_frame.pack_forget()

####### MAIN UI BG through Pillow PIL ########
main_bg = Canvas(main_frame, bg="#e3e3e3", height=480, width=848) 
main_bg_image = ImageTk.PhotoImage(Image.open("Images/emptybg.png")) # BG through Pillow PIL
main_label = Label(main_frame, image=main_bg_image) 
main_label.place(x=0, y=0, relwidth=1, relheight=1) 
main_bg.pack()

###### MAIN UI LABELS ###########
TTF = "₱"+str(Total_Fare)
main_totalfare = Label(main_frame, width="7", bd=0, bg="#e3e3e3", fg="#00ad31", font=("ArialUnicodeMS",55), text=TTF)
main_totalfare.place(x=70,y=32)

main_totalpass = Label(main_frame, width="7", bd=0, bg="#e3e3e3", fg="#00ad31", font=("ArialUnicodeMS",55), text=Total_Passenger)
main_totalpass.place(x=70,y=282)

main_drivername = Label(main_frame, anchor="sw", width="25", bd=0, bg="#e3e3e3", fg="#000000", font=("ArialUnicodeMS",15), text=Driver_Name)
main_drivername.place(x=10,y=445) 

main_recent = Label(main_frame, anchor="center", height="1", width="8", bd=0, bg="#e3e3e3", fg="#000000", font=("ArialUnicodeMS",32), text="13174803")
main_recent.place(x=540,y=58) 

wifi_image = ImageTk.PhotoImage(Image.open("Images/yeswifi.png"))
wifi_label = Label(main_frame, image=wifi_image, bd=0, bg="#e3e3e3") 
wifi_label.place(x=10,y=10)

####### HISTORY UI BG through Pillow PIL ########
hist_bg = Canvas(hist_frame, bg="#e3e3e3", height=480, width=848) 
hist_bg_image = ImageTk.PhotoImage(Image.open("Images/history_bg.png")) # BG through Pillow PIL
hist_label = Label(hist_frame, image=hist_bg_image) 
hist_label.place(x=0, y=0, relwidth=1, relheight=1) 
hist_bg.pack()

####### GREYED OUT UI BG through Pillow PIL ########
grey_bg = Canvas(grey_frame, bg="#0e0e0e", height=480, width=848) 
grey_bg.pack()

grey_recent = Label(grey_frame, anchor="center", height="1", width="8", bd=0, bg="#e3e3e3", fg="#000000", font=("ArialUnicodeMS",32), text="")
grey_recent.place(x=540,y=58) 

###### BUTTONS FOR MAIN UI #######
###### BUTTON IMAGES LOAD #######
sd_image = ImageTk.PhotoImage(Image.open("Images/sd_button.png"))
sy_image = ImageTk.PhotoImage(Image.open("Images/sync_button.png"))
showhide_image = ImageTk.PhotoImage(Image.open("Images/showhide_button.png"))
hist_image = ImageTk.PhotoImage(Image.open("Images/hist_button.png"))

#### SYNC ####
syB = Button (main_frame, image=sy_image, width=182, height=74, highlightthickness=0, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: sync())
syB.place(bordermode=OUTSIDE,x=438,y=258)

#### SHOW/HIDE ####
showhideB = Button (main_frame, image=showhide_image, width=182, height=74, highlightthickness=0, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: showhide(main_totalfare,main_totalpass))
showhideB.place(bordermode=OUTSIDE,x=650,y=258)

#### HISTORY ####
histB = Button (main_frame, image=hist_image, width=182, height=74, highlightthickness=0, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: [main_frame.pack_forget(),hist_frame.pack(expand=1,fill=BOTH)])
histB.place(bordermode=OUTSIDE,x=438,y=370)

#### SHUTDOWN ####
shutdownB = Button (main_frame, image=sd_image, width=182, height=74, highlightthickness=0, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=window.destroy) 
shutdownB.place(bordermode=OUTSIDE,x=650,y=370)

###### BUTTONS FOR HISTORY UI #######
###### BUTTON IMAGES LOAD #######
bk = ImageTk.PhotoImage(Image.open("Images/back_button.png"))
nx = ImageTk.PhotoImage(Image.open("Images/next_button.png"))
pv = ImageTk.PhotoImage(Image.open("Images/prev_button.png"))

#### BACK ####
backB = Button (hist_frame, image=bk, width=182, height=74, highlightthickness=0, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: [main_frame.pack(expand=1,fill=BOTH),hist_frame.pack_forget()])
backB.place(bordermode=OUTSIDE,x=25,y=20)

#### NEXT ####
nextB = Button (hist_frame, image=nx, width=182, height=74, highlightthickness=0, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: [main_frame.pack(expand=1,fill=BOTH),hist_frame.pack_forget()])
nextB.place(bordermode=OUTSIDE,x=465,y=380)

#### PREVIOUS ####
prevB = Button (hist_frame, image=pv, width=182, height=74, highlightthickness=0, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: [main_frame.pack(expand=1,fill=BOTH),hist_frame.pack_forget()])
prevB.place(bordermode=OUTSIDE,x=200,y=380)

is_wifi()
recent_student()
grey_recent_student()
window.mainloop() #Start

