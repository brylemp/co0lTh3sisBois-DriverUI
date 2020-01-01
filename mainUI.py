from Tkinter import *
from PIL import ImageTk, Image

window = Tk()
window.title("weweew") 
window.geometry("1000x600") #Size for Window
# window.overrideredirect(1) #Remove window border
window.resizable(False,False) #Prevent resize windows

####### BG through Pillow PIL ########
C = Canvas(window, bg="black", height=100, width=300) 
bg_image = ImageTk.PhotoImage(Image.open("db.png")) # BG through Pillow PIL
background_label = Label(window, image=bg_image) 
background_label.place(x=0, y=0, relwidth=1, relheight=1) 
C.pack()

###### BUTTON IMAGES LOAD #######
sd_image = ImageTk.PhotoImage(Image.open("sd.png"))
sy_image = ImageTk.PhotoImage(Image.open("sync.png"))
showhide_image = ImageTk.PhotoImage(Image.open("showhide.png"))
hist_image = ImageTk.PhotoImage(Image.open("hist.png"))

#### SYNC ####
syB = Button (window, image=sy_image, width=182, height=74, border=0, highlightthickness=0, highlightbackground="#ffffff", command=window.destroy)
syB.place(bordermode=OUTSIDE,x=550,y=349)

#### SHOW/HIDE ####
showhideB = Button (window, image=showhide_image, width=182, height=74, border=0, highlightthickness=0, highlightbackground="#ffffff", command=window.destroy)
showhideB.place(bordermode=OUTSIDE,x=760,y=349)

#### HISTORY ####
histB = Button (window, image=hist_image, width=182, height=74, border=0, highlightthickness=0, highlightbackground="#ffffff", command=window.destroy)
histB.place(bordermode=OUTSIDE,x=550,y=459)

#### SHUTDOWN ####
shutdownB = Button (window, image=sd_image, width=182, height=74, border=0, highlightthickness=0, highlightbackground="#ffffff", command=window.destroy) 
shutdownB.place(bordermode=OUTSIDE,x=760,y=459)

window.mainloop() #Start