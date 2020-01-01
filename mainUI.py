from tkinter import *
from historyUI import *
from PIL import ImageTk, Image

def sync():
    print("Sync!")

def showhide():
    print("Hidden")

def mainUI(window):
    ##### FRAME ######
    main_frame = Frame(window)
    main_frame.pack(expand=1,fill=BOTH)

    hist_frame = Frame(window)
    hist_frame.pack_forget()
    
    ####### MAIN UI BG through Pillow PIL ########
    BackGround = Canvas(main_frame, bg="black", height=1000, width=600) 
    bg_image = ImageTk.PhotoImage(Image.open("db.png")) # BG through Pillow PIL
    background_label = Label(main_frame, image=bg_image) 
    background_label.place(x=0, y=0, relwidth=1, relheight=1) 
    BackGround.pack()

    ####### HISTORY UI BG through Pillow PIL ########
    hist_bg = Canvas(hist_frame, bg="black", height=1000, width=600) 
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
    syB.place(bordermode=OUTSIDE,x=550,y=349)

    #### SHOW/HIDE ####
    showhideB = Button (main_frame, image=showhide_image, width=182, height=74, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=showhide)
    showhideB.place(bordermode=OUTSIDE,x=762,y=349)

    #### HISTORY ####
    histB = Button (main_frame, image=hist_image, width=182, height=74, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: [main_frame.pack_forget(),hist_frame.pack(expand=1,fill=BOTH)])
    histB.place(bordermode=OUTSIDE,x=550,y=460)

    #### SHUTDOWN ####
    shutdownB = Button (main_frame, image=sd_image, width=182, height=74, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=window.destroy) 
    shutdownB.place(bordermode=OUTSIDE,x=760,y=459)

    ###### BUTTONS FOR MAIN UI #######
    ###### BUTTON IMAGES LOAD #######
    bk = ImageTk.PhotoImage(Image.open("back.png"))
    nx = ImageTk.PhotoImage(Image.open("next.png"))
    pv = ImageTk.PhotoImage(Image.open("prev.png"))

    #### BACK ####
    backB = Button (hist_frame, image=bk, width=182, height=74, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: [main_frame.pack(expand=1,fill=BOTH),hist_frame.pack_forget()])
    backB.place(bordermode=OUTSIDE,x=25,y=20)

    #### NEXT ####
    nextB = Button (hist_frame, image=nx, width=182, height=74, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: [main_frame.pack(expand=1,fill=BOTH),hist_frame.pack_forget()])
    nextB.place(bordermode=OUTSIDE,x=540,y=510)

    #### PREVIOUS ####
    prevB = Button (hist_frame, image=pv, width=182, height=74, bd=0, bg="#e3e3e3", activebackground="#e3e3e3", command=lambda: [main_frame.pack(expand=1,fill=BOTH),hist_frame.pack_forget()])
    prevB.place(bordermode=OUTSIDE,x=275,y=510)

    window.mainloop() #Start


if __name__ == "__main__":
    ##### WINDOW #####
    window = Tk()
    window.geometry("1000x600") #Size for Window
    # window.overrideredirect(1) #Remove window border
    window.resizable(False,False) #Prevent resize windows
    mainUI(window)