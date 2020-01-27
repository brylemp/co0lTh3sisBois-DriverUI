from tkinter import *
from historyUI import *
from PIL import ImageTk, Image
import os,re

shflag=0
Total_Fare = 1500
Total_Passenger = 300
Driver_Name = "Dela Cruz, Juan Paolo"
Wifi_Status = 0

def is_wifi():
    wat = os.popen('iwgetid').read()
    watt = re.findall('"([^"]*)"',wat) ##FIND ENCLOSED IN ""##
    watt = ''.join(watt) ##CONVERT LIST TO STRING##
    if watt == "Patalinghug1":
        replace = ImageTk.PhotoImage(Image.open("wifistatus.png"))
    else:
        replace = ImageTk.PhotoImage(Image.open("nowifi.png"))
        
    wifi_label.config(image=replace)
    wifi_label.image=replace
    window.after(5000, is_wifi)

def sync(wifi_label,nowifi_label):
    # print("Sync!")
    global Wifi_Status
    
    if Wifi_Status == 0:
        wifi_label.place_forget()
        nowifi_label.place(x=10,y=10)
        Wifi_Status = not Wifi_Status
        print(Wifi_Status)
    elif Wifi_Status == 1:
        nowifi_label.place_forget()
        wifi_label.place(x=10,y=10)
        Wifi_Status = not Wifi_Status
        print(Wifi_Status)

def showhide(main_totalfare,main_totalpass):
    global shflag
    if shflag == 0:
        print("Hidden!")
        main_totalfare.config(text="Hidden")
        main_totalpass.config(text="Hidden")
        shflag = 1
    elif shflag == 1:
        print("Shown!")
        TTF = "₱"+str(Total_Fare)
        main_totalfare.config(text=TTF)
        main_totalpass.config(text=Total_Passenger)
        shflag = 0
        

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

####### MAIN UI BG through Pillow PIL ########
main_bg = Canvas(main_frame, bg="#e3e3e3", height=480, width=848) 
main_bg_image = ImageTk.PhotoImage(Image.open("emptybg.png")) # BG through Pillow PIL
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

wifi_image = ImageTk.PhotoImage(Image.open("wifistatus.png"))
wifi_label = Label(main_frame, image=wifi_image, bd=0, bg="#e3e3e3") 
wifi_label.place(x=10,y=10)


####### HISTORY UI BG through Pillow PIL ########
hist_bg = Canvas(hist_frame, bg="#e3e3e3", height=480, width=848) 
hist_bg_image = ImageTk.PhotoImage(Image.open("hist_screen.png")) # BG through Pillow PIL
hist_label = Label(hist_frame, image=hist_bg_image) 
hist_label.place(x=0, y=0, relwidth=1, relheight=1) 
hist_bg.pack()

###### BUTTONS FOR MAIN UI #######
###### BUTTON IMAGES LOAD #######
sd_image = ImageTk.PhotoImage(Image.open("sd.png"))
sy_image = ImageTk.PhotoImage(Image.open("sync.png"))
showhide_image = ImageTk.PhotoImage(Image.open("showhide.png"))
hist_image = ImageTk.PhotoImage(Image.open("hist.png"))

#### SYNC ####
syB = Button (main_frame, image=sy_image, width=182, height=74, highlightthickness=0, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: sync(wifi_label,nowifi_label))
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
bk = ImageTk.PhotoImage(Image.open("back.png"))
nx = ImageTk.PhotoImage(Image.open("next.png"))
pv = ImageTk.PhotoImage(Image.open("prev.png"))

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
window.mainloop() #Start



    
