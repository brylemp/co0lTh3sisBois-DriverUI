from tkinter import *
from historyUI import *
from PIL import ImageTk, Image

shflag=0

def sync():
    print("Sync!")

def showhide(main_totalfare,main_totalpass):
    global shflag
    if shflag == 0:
        print("Hidden!")
        main_totalfare.config(text="Hidden")
        main_totalpass.config(text="Hidden")
        shflag = 1
    elif shflag == 1:
        print("Shown!")
        main_totalfare.config(text="₱500")
        main_totalpass.config(text="100")
        shflag = 0
        
def mainUI(window):
    ##### FRAME ######
    main_frame = Frame(window)
    main_frame.pack(expand=1,fill=BOTH)

    hist_frame = Frame(window)
    hist_frame.pack_forget()
    
    ####### MAIN UI BG through Pillow PIL ########
    main_bg = Canvas(main_frame, bg="#e3e3e3", height=480, width=848) 
    main_bg_image = ImageTk.PhotoImage(Image.open("db.png")) # BG through Pillow PIL
    main_label = Label(main_frame, image=main_bg_image) 
    main_label.place(x=0, y=0, relwidth=1, relheight=1) 
    main_bg.pack()

    ###### MAIN UI LABELS ###########
    main_totalfare = Label(main_frame, width="7", bd=0, bg="#e3e3e3", fg="#00ad31", font=("ArialUnicodeMS",70), text="₱500")
    main_totalfare.place(x=80,y=42)

    main_totalpass = Label(main_frame, width="7", bd=0, bg="#e3e3e3", fg="#00ad31", font=("ArialUnicodeMS",70), text="100")
    main_totalpass.place(x=80,y=262)

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
    syB = Button (main_frame, image=sy_image, width=182, height=74, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=sync)
    syB.place(bordermode=OUTSIDE,x=438,y=258)

    #### SHOW/HIDE ####
    showhideB = Button (main_frame, image=showhide_image, width=182, height=74, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: showhide(main_totalfare,main_totalpass))
    showhideB.place(bordermode=OUTSIDE,x=650,y=258)

    #### HISTORY ####
    histB = Button (main_frame, image=hist_image, width=182, height=74, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: [main_frame.pack_forget(),hist_frame.pack(expand=1,fill=BOTH)])
    histB.place(bordermode=OUTSIDE,x=438,y=370)

    #### SHUTDOWN ####
    shutdownB = Button (main_frame, image=sd_image, width=182, height=74, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=window.destroy) 
    shutdownB.place(bordermode=OUTSIDE,x=650,y=370)

    ###### BUTTONS FOR HISTORY UI #######
    ###### BUTTON IMAGES LOAD #######
    bk = ImageTk.PhotoImage(Image.open("back.png"))
    nx = ImageTk.PhotoImage(Image.open("next.png"))
    pv = ImageTk.PhotoImage(Image.open("prev.png"))

    #### BACK ####
    backB = Button (hist_frame, image=bk, width=182, height=74, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: [main_frame.pack(expand=1,fill=BOTH),hist_frame.pack_forget()])
    backB.place(bordermode=OUTSIDE,x=25,y=20)

    #### NEXT ####
    nextB = Button (hist_frame, image=nx, width=182, height=74, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: [main_frame.pack(expand=1,fill=BOTH),hist_frame.pack_forget()])
    nextB.place(bordermode=OUTSIDE,x=465,y=380)

    #### PREVIOUS ####
    prevB = Button (hist_frame, image=pv, width=182, height=74, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: [main_frame.pack(expand=1,fill=BOTH),hist_frame.pack_forget()])
    prevB.place(bordermode=OUTSIDE,x=200,y=380)

    window.mainloop() #Start

if __name__ == "__main__":
    ##### WINDOW #####
    window = Tk()
    window.geometry("848x480") #Size for Window
    # window.overrideredirect(1) #Remove window border
    window.resizable(False,False) #Prevent resize windows
    mainUI(window)
