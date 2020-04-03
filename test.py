import tkinter as tk
from tkinter import ttk

LARGE_FONT = ("Verdana 12")
NORM_FONT = "Verdana 10"
SMALL_FONT = ("Verdana 8")
ERROR_404 = "Error 404 : Page not found !"

class sjabloon(tk.Tk):
    def __init__(self, *args, **kwargs):
        #make window        
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry("600x600+10+10")

        #make top frame
        self.frame_header = tk.Frame(self, background='black', width=600, height=50)
        self.frame_header.grid(column=0, row=0 , columnspan= 10)

        #make body frame
        container = tk.Frame(self, width=600, height=400)
        container.grid(column=0, row=1 , columnspan= 10)

        #list of Pages
        self.frames = {}

        #everytime you create a "Page", you add it there
        for F in (StartPage, HomePage):
            frame = F(container, self)
            self.frames[F] = frame     
            frame.grid(row=1, column = 0, sticky="nsew", columnspan= 10)

        self.show_page("StartPage")


        #make body footer
        self.frame_footer = tk.Frame(self, background='yellow', width=600, height=50)
        self.frame_footer.grid(column=0, row=3 , columnspan= 10)



    def show_page(self, page_name):
        """
            let us use the NAME of the class to display(the function show_frame
            use directly the class).
            when we use the classe name, we can put our classes in defferent
            files
        """
        for F in self.frames:
            if F.__name__ == page_name:
                self.show_frame(F)
                return
        print(ERROR_404)


    def show_frame(self, cont):
        """raise to the front the frame we want

            :param cont: the frame
        """
        frame = self.frames[cont]
        frame.tkraise()



class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #button1 select
        tk.Label(self, text="Select:").grid(column=0, row=2, stick='W')
        self.button1 = tk.Button(self, text="Select")
        self.button1.grid(row=2, column=5, stick='W', padx=(50,0))
        #button1 select
        tk.Label(self, text="Select:").grid(column=0, row=3, stick='W')
        self.button2 = tk.Button(self, text="Select")
        self.button2.grid(row=4, column=5, stick='W', padx=(50,0))
        #button submit
        self.submit = tk.Button(self, text="Start")
        self.submit.grid(row=10, column=9, stick='W')


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text="""ALPHA application.
        use at your own risk. There is no promise
        of warranty""", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Agree",
                            command=lambda: controller.show_page("HomePage"))
        button1.pack()

        button2 = ttk.Button(self, text="Disagree",
                            command=controller.destroy)
        button2.pack()



if __name__ == "__main__":
    sjabloon = sjabloon()
    sjabloon.mainloop()