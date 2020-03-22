import RPi.GPIO as GPIO
from tkinter import *
from PIL import ImageTk, Image
from mfrc522 import SimpleMFRC522
import os,re, sqlite3
import datetime

login = 0
handbrake_sensor = 29

history_page_counter = 0
history_page = []

showhide_flag = 0

grey_counter = 0
grey_flag = 0
grey_old = sqlite3.connect('../SHUTTLE/shuttle1.db').execute("SELECT uid from recentTransaction").fetchone()[0]

Driver_Name = ("",)
Driver_ID = ("",)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(handbrake_sensor,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setwarnings(False)

def updateDriverStatus(driverIDNum):
    try:
        conn=sqlite3.connect('../SHUTTLE/shuttle1.db')
        cursor=conn.execute("UPDATE driverStatus SET Driverstatus='1',Driverid=? where Id ='1'",driverIDNum)
        cursor=conn.cursor()
        conn.commit()
        cursor.close()
        conn.close()
    except sqlite3.Error as error:
        print("Error encountered in updating recent transaction sqlite",error)
        input("Press Enter to continue...")
    finally:
        if (conn):
            conn.close()
            # print("The SQLite connection is closed")

def refresh():
    global login
    if login == 0:
        login_reader = SimpleMFRC522()
        UID,IDNUM = login_reader.read_no_block()
        if UID!=None:
            UID=UID>>0x08                                           #removed last 16 bits/2 bytes of the uid read by the mfrc522
            conn = sqlite3.connect('../SHUTTLE/shuttle1.db')
            cursor = conn.execute("SELECT RFID_UID, Driver_ID, Fname from driverAccounts where RFID_UID=?",(UID, ))
            if cursor!=None:
                for row in cursor:
                    print(row)
                    if str(UID) == row[0]:
                        global Driver_ID, Driver_Name
                        Driver_ID = (row[1],)
                        Driver_Name = (row[2],)
                        print("DRIVER FOUND: %s - %s" % (Driver_Name,Driver_ID))
                        #update driver driverStatus=1, driverID
                        updateDriverStatus(Driver_ID)

                        main_drivername.config(text=Driver_Name[0])
                        login_frame.pack_forget()
                        main_frame.pack(expand=1,fill=BOTH)
                        login = 1
                        break
                        
                conn.close()
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
        
        #TOTAL PASSENGER/TOTAL FARE
        conn = sqlite3.connect('../SHUTTLE/shuttle1.db')
        cursor = conn.execute("SELECT Total_Amount FROM driverSummary WHERE Driver_ID = ? AND Date= ? LIMIT 1", (Driver_ID[0],datetime.datetime.now().strftime("%Y-%m-%d")))
        TTF = cursor.fetchone()[0]
        TTP = TTF/5
        TTF = "₱"+str(TTF)
        main_totalfare.config(text=TTF,anchor="center")
        main_totalpass.config(text=TTP,anchor="center")
        
        #GREY RFID
        global grey_flag
        global grey_counter
        global grey_old

        if(GPIO.input(handbrake_sensor)==GPIO.HIGH):
            main_frame.pack_forget()
            hist_frame.pack_forget()
            # grey_frame.pack(expand=1,fill=BOTH)
            conn = sqlite3.connect('../SHUTTLE/shuttle1.db')
            cursor = conn.execute("SELECT uid from recentTransaction")
            new = cursor.fetchone()[0]
            print(grey_old,new)
            if grey_old == new:
                
                if grey_flag == 1:
                    # print(grey_counter)
                    grey_frame.pack(expand=1,fill=BOTH)
                    grey_recent.config(text=new,anchor="w")
                    if grey_counter == 16:
                        grey_recent.config(text="",anchor="w")
                        grey_frame.pack_forget()
                        grey_counter = 0
                        grey_flag = 0
                    else:
                        grey_counter = grey_counter + 1
                else:
                    grey_recent.config(text="",anchor="w")
                    grey_frame.pack_forget()
                    
            else:
                grey_flag = 1
                grey_counter = 0
                grey_old = new
        else:
            grey_frame.pack_forget()
            main_frame.pack(expand=1,fill=BOTH)
        
        #Recent Passenger
        conn = sqlite3.connect('../SHUTTLE/shuttle1.db')
        cursor = conn.execute("SELECT uid from recentTransaction")
        recent = cursor.fetchone()[0]
        main_recent.config(text=recent,anchor="w")

    window.after(300, refresh)

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

    conn = sqlite3.connect('../SHUTTLE/shuttle1.db')

    cursor = conn.execute("SELECT Date, Total_Amount from driverSummary where Driver_id = ?", Driver_ID)
    rowexists = cursor.fetchone()
    if rowexists == None:
        print("None")
        history_date1.config(text="")
        history_total_amount1.config(text="")
        history_total_passenger1.config(text="")

        history_date2.config(text="")
        history_total_amount2.config(text="")
        history_total_passenger2.config(text="")

        history_date3.config(text="")
        history_total_amount3.config(text="")
        history_total_passenger3.config(text="")
    else:
        cursor = conn.execute("SELECT Date, Total_Amount from driverSummary where Driver_id = %s" % (Driver_ID))
        histrecord = []
        for row in cursor:
            driverquery = {
                'Date':row[0],
                'Total_Amount':row[1]
            }
            histrecord.append(driverquery)

        while (1):
            if len(histrecord)%3 == 0:
                break
            else:
                driverquery = {
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
window.overrideredirect(1) #Remove window border
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
main_totalfare = Label(main_frame, width="7", bd=0, bg="#e3e3e3", fg="#00ad31", font=("ArialUnicodeMS",55), text=" ")
main_totalfare.place(x=70,y=32)

main_totalpass = Label(main_frame, width="7", bd=0, bg="#e3e3e3", fg="#00ad31", font=("ArialUnicodeMS",55), text=" ")
main_totalpass.place(x=70,y=282)

main_drivername = Label(main_frame, anchor="sw", width="25", bd=0, bg="#e3e3e3", fg="#000000", font=("ArialUnicodeMS",15))
main_drivername.place(x=10,y=445) 

main_recent = Label(main_frame, anchor="center", height="1", width="8", bd=0, bg="#e3e3e3", fg="#000000", font=("ArialUnicodeMS",32))
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
grey_bg = Canvas(grey_frame, bg="#121212", height=480, width=848)
grey_bg_image = ImageTk.PhotoImage(Image.open("Images/hbbg.png")) # BG through Pillow PIL
grey_label = Label(grey_frame, image=grey_bg_image) 
grey_label.place(x=0, y=0, relwidth=1, relheight=1) 
grey_bg.pack()

grey_recent = Label(grey_frame, anchor="center", height="1", width="8", bd=0, bg="#e3e3e3", fg="#000000", font=("ArialUnicodeMS",32), text="")
grey_recent.place(x=520,y=158) 

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

