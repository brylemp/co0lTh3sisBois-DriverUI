from tkinter import *
from PIL import ImageTk, Image
import os,re
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import datetime
import raspiRFID
import raspiRFID2
import threading
import sqlite3

login = 0
handbrake_sensor = 29
history_page_counter = 0
history_page = []
showhide_flag = 0
grey_counter = 0
grey_flag = 0
Total_Fare = 1500
Total_Passenger = 300

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
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(buzzer1,GPIO.OUT)
GPIO.setup(buzzer2,GPIO.OUT)
blockedAccounts=[]
timeWindow=60

def temporaryBlockFunc():
    global blockedAccounts
    toRemove=[]
    for accounts in blockedAccounts:
            print(accounts)
            print(time.time()-accounts[1])
            if(time.time()-accounts[1]>timeWindow):
                    toRemove.append(accounts)
                    print(toRemove)
    for x in toRemove:
            print("Remove="+str(x))
            blockedAccounts.remove(x)

def findIfBlocked(compare):
    for accounts in blockedAccounts:
            if(accounts[0]==compare):
                return 1
    return 0
        
def refresh():
    global login
    if login == 0:
        login_reader = SimpleMFRC522()
        UID,IDNUM = login_reader.read_no_block()
        conn = sqlite3.connect('shuttle1.db')
        cursor = conn.execute("SELECT Uid, Driver_id, Driver_name from driverAccounts")
        for row in cursor:
            print(row)
            if str(UID) == row[0]:
                print("DRIVER FOUND: %s - %s" % (row[2],row[1]))
                main_drivername.config(text=row[2])
                login_frame.pack_forget()
                main_frame.pack(expand=1,fill=BOTH)
                login = 1
    else:
        # WIFI CHECK
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

        #GREY RFID
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
        
        # call blocking accounts func
        temporaryBlockFunc()

        # RFID READER
        rfid_uid, text = RFID_reader1.read_no_block()
        print("RFID1 UID="+str(rfid_uid))
        rfid_idNum=raspiRFID.checkUID(rfid_uid)
        print("IDNUM="+str(rfid_idNum))
        
        if(rfid_idNum!=None):
            if(not findIfBlocked(rfid_idNum[0])):
                if(rfid_idNum[1]==1):
                    transactionRecord= [(str(rfid_uid),str(datetime.datetime.now()),str(rfid_idNum[0]),int(shuttlePrice),str(temp_DRIVERID))]
                    raspiRFID.inputTransactiontoDB(transactionRecord)
                    raspiRFID.buzzSuccessful(buzzer1)
                    #add to blocked list
                    blockedAccounts.append([rfid_idNum[0],time.time()])
                    main_recent.config(text=rfid_idNum[0],anchor="w")
                else:
                    raspiRFID.buzzNoBalance(buzzer1)
                    pass
            else:
                print("Blocked for 60 sec")
        else:
            print('UID not in database')
            #raspiRFID.buzzNotInDB(buzzer1)

        #SECOND RFID READER
        rfid_uid2, text2 = RFID_reader2.read_no_block()
        print("RFID2 UID="+str(rfid_uid2))
        rfid_idNum2=raspiRFID.checkUID(rfid_uid2)
        print('IDNUM2='+str(rfid_idNum2))
        
        if(rfid_idNum2!=None):
            if(not findIfBlocked(rfid_idNum2[0])):
                if(rfid_idNum2[1]==1):
                    transactionRecord= [(str(rfid_uid2),str(datetime.datetime.now()),str(rfid_idNum2[0]),int(shuttlePrice),str(temp_DRIVERID))]
                    raspiRFID.inputTransactiontoDB(transactionRecord)
                    raspiRFID.buzzSuccessful(buzzer2)
                    #add to blocked list
                    blockedAccounts.append([rfid_idNum2[0],time.time()])
                    main_recent.config(text=rfid_idNum2[0],anchor="w")
                else:
                    raspiRFID.buzzNoBalance(buzzer2)
                    pass
            else:
                print("Blocked for 60 sec")
        else:
                print('UID not in database')
                # raspiRFID.buzzNotInDB(buzzer2)

    window.after(300, refresh)

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

def pageturn(nextt):
    global history_page_counter
    if nextt == 0:
        history_page_counter+=1
    else:
        history_page_counter-=1
    
    if history_page_counter > len(history_page)-1:
        history_page_counter =  len(history_page)-1
    elif history_page_counter < 0:
        history_page_counter = 0

    history_date1.config(text=history_page[history_page_counter][0]['Date'])
    history_total_amount1.config(text=history_page[history_page_counter][0]['Total_Amount'])
    history_total_passenger1.config(text=int(history_page[history_page_counter][0]['Total_Amount']/5))

    history_date2.config(text=history_page[history_page_counter][1]['Date'])
    history_total_amount2.config(text=history_page[history_page_counter][1]['Total_Amount'])
    history_total_passenger2.config(text=int(history_page[history_page_counter][1]['Total_Amount']/5))

    history_date3.config(text=history_page[history_page_counter][2]['Date'])
    history_total_amount3.config(text=history_page[history_page_counter][2]['Total_Amount'])
    history_total_passenger3.config(text=int(history_page[history_page_counter][2]['Total_Amount']/5))

def history_frame_open():
    global history_page

    main_frame.pack_forget()
    hist_frame.pack(expand=1,fill=BOTH)

    conn = sqlite3.connect('shuttle1.db')

    cursor = conn.execute("SELECT Driver_id, Date, Total_Amount from driverSummary")
    histrecord = []
    for row in cursor:
        driverquery = {
            'Driver_id':row[0],
            'Date':row[1],
            'Total_Amount':row[2]
        }
        histrecord.append(driverquery)

    while (1):
        if len(histrecord)%3 != 0:
            driverquery = {
                'Driver_id':' ',
                'Date':' ',
                'Total_Amount':0
            }
            histrecord.append(driverquery)
            break
            
    history_page = []
    for x in range(int(len(histrecord)/3)):
        history_page.append(histrecord[x*3:(x*3)+3])

    history_date1.config(text=history_page[history_page_counter][0]['Date'])
    history_total_amount1.config(text=history_page[history_page_counter][0]['Total_Amount'])
    history_total_passenger1.config(text=int(history_page[history_page_counter][0]['Total_Amount']/5))

    history_date2.config(text=history_page[history_page_counter][1]['Date'])
    history_total_amount2.config(text=history_page[history_page_counter][1]['Total_Amount'])
    history_total_passenger2.config(text=int(history_page[history_page_counter][1]['Total_Amount']/5))

    history_date3.config(text=history_page[history_page_counter][2]['Date'])
    history_total_amount3.config(text=history_page[history_page_counter][2]['Total_Amount'])
    history_total_passenger3.config(text=int(history_page[history_page_counter][2]['Total_Amount']/5))
        
    conn.close()

##### WINDOW #####
window = Tk()
window.geometry("848x480") #Size for Window
# window.overrideredirect(1) #Remove window border
window.resizable(False,False) #Prevent resize windows

##### FRAMES ######
login_frame = Frame(window)
login_frame.pack(expand=1,fill=BOTH)

main_frame = Frame(window)
main_frame.pack_forget()

hist_frame = Frame(window)
hist_frame.pack_forget()

grey_frame = Frame(window)
grey_frame.pack_forget()

####### LOGIN UI BG through Pillow PIL ########
login_bg = Canvas(login_frame, bg="#e3e3e3", height=480, width=848) 
login_bg_image = ImageTk.PhotoImage(Image.open("Images/loginbg.png")) # BG through Pillow PIL
login_label = Label(login_frame, image=login_bg_image) 
login_label.place(x=0, y=0, relwidth=1, relheight=1) 
login_bg.pack()

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

main_drivername = Label(main_frame, anchor="sw", width="25", bd=0, bg="#e3e3e3", fg="#000000", font=("ArialUnicodeMS",15))
main_drivername.place(x=10,y=445) 

main_recent = Label(main_frame, anchor="center", height="1", width="8", bd=0, bg="#e3e3e3", fg="#000000", font=("ArialUnicodeMS",32), text="13174803")
main_recent.place(x=543,y=58) 

main_tap_status = Label(main_frame, anchor="center", height="1", width="8", bd=0, bg="#e3e3e3", fg="#00ad31", font=("ArialUnicodeMS",24), text="Success!")
main_tap_status.place(x=570,y=110) 

main_sync_status = Label(main_frame, anchor="center", height="2", width="15", bd=0, bg="#e3e3e3", fg="#a90011", font=("ArialUnicodeMS",24), text="Last Synced\n03/23/20 12:02")
main_sync_status.place(x=509,y=160) 

wifi_image = ImageTk.PhotoImage(Image.open("Images/yeswifi.png"))
wifi_label = Label(main_frame, image=wifi_image, bd=0, bg="#e3e3e3") 
wifi_label.place(x=10,y=10)

####### HISTORY UI BG through Pillow PIL ########
hist_bg = Canvas(hist_frame, bg="#e3e3e3", height=480, width=848) 
# hist_bg_image = ImageTk.PhotoImage(Image.open("Images/history_bg.png")) # BG through Pillow PIL
hist_bg_image = ImageTk.PhotoImage(Image.open("Images/history_emptybg.png")) # BG through Pillow PIL
hist_label = Label(hist_frame, image=hist_bg_image) 
hist_label.place(x=0, y=0, relwidth=1, relheight=1) 
hist_bg.pack()

###### HISTORY UI LABELS ###########
history_date1 = Label(hist_frame, width="10", height="1", bd=0, bg="#c5c5c5", fg="#000000", font=("ArialUnicodeMS",30))
history_date1.place(x=50,y=125)

history_total_amount1 = Label(hist_frame, width="10", height="1", bd=0, bg="#c5c5c5", fg="#00ad31", font=("ArialUnicodeMS",20))
history_total_amount1.place(x=685,y=115)

history_total_passenger1 = Label(hist_frame, width="10", height="1", bd=0, bg="#c5c5c5", fg="#00ad31", font=("ArialUnicodeMS",20))
history_total_passenger1.place(x=685,y=155)

history_date2 = Label(hist_frame, width="10", height="1", bd=0, bg="#e3e3e3", fg="#000000", font=("ArialUnicodeMS",30))
history_date2.place(x=50,y=209)

history_total_amount2 = Label(hist_frame, width="10", height="1", bd=0, bg="#e3e3e3", fg="#00ad31", font=("ArialUnicodeMS",20))
history_total_amount2.place(x=685,y=199)

history_total_passenger2 = Label(hist_frame, width="10", height="1", bd=0, bg="#e3e3e3", fg="#00ad31", font=("ArialUnicodeMS",20))
history_total_passenger2.place(x=685,y=239)

history_date3 = Label(hist_frame, width="10", height="1", bd=0, bg="#c5c5c5", fg="#000000", font=("ArialUnicodeMS",30))
history_date3.place(x=50,y=291)

history_total_amount3 = Label(hist_frame, width="10", height="1", bd=0, bg="#c5c5c5", fg="#00ad31", font=("ArialUnicodeMS",20))
history_total_amount3.place(x=685,y=281)

history_total_passenger3 = Label(hist_frame, width="10", height="1", bd=0, bg="#c5c5c5", fg="#00ad31", font=("ArialUnicodeMS",20))
history_total_passenger3.place(x=685,y=321)

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
syB.place(bordermode=OUTSIDE,x=448,y=278)

#### SHOW/HIDE ####
showhideB = Button (main_frame, image=showhide_image, width=182, height=74, highlightthickness=0, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: showhide(main_totalfare,main_totalpass))
showhideB.place(bordermode=OUTSIDE,x=640,y=278)

#### HISTORY ####
histB = Button (main_frame, image=hist_image, width=182, height=74, highlightthickness=0, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: history_frame_open())
histB.place(bordermode=OUTSIDE,x=448,y=370)

#### SHUTDOWN ####
shutdownB = Button (main_frame, image=sd_image, width=182, height=74, highlightthickness=0, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=window.destroy) 
shutdownB.place(bordermode=OUTSIDE,x=640,y=370)

###### BUTTONS FOR HISTORY UI #######
###### BUTTON IMAGES LOAD #######
bk = ImageTk.PhotoImage(Image.open("Images/back_button.png"))
nx = ImageTk.PhotoImage(Image.open("Images/next_button.png"))
pv = ImageTk.PhotoImage(Image.open("Images/prev_button.png"))

#### BACK ####
backB = Button (hist_frame, image=bk, width=182, height=74, highlightthickness=0, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: [main_frame.pack(expand=1,fill=BOTH),hist_frame.pack_forget()])
backB.place(bordermode=OUTSIDE,x=25,y=20)

#### NEXT ####
nextB = Button (hist_frame, image=nx, width=182, height=74, highlightthickness=0, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: pageturn(0))
nextB.place(bordermode=OUTSIDE,x=465,y=380)

#### PREVIOUS ####
prevB = Button (hist_frame, image=pv, width=182, height=74, highlightthickness=0, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: pageturn(1))
prevB.place(bordermode=OUTSIDE,x=200,y=380)

refresh()
window.mainloop() #Start

