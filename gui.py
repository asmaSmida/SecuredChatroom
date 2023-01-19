# Import Module
from tkinter import *
from tkinter import ttk
#from client import input_handler
class ChatInterface(Frame):

    def __init__(self, root=None, username="",handler=None):
        Frame.__init__(self, root)
        self.root = root
        self.username=username
        self.input_handler=handler
        lbl = Label(root, text = "Welcome to your private chatroom"+self.username)
        lbl.pack()



        
        self.notebook = ttk.Notebook(self.master)
        self.container = Frame(self.notebook, bd=0)
        self.container.pack(expand=True, fill=BOTH)
        
        self.notebook.pack(expand=True, fill=BOTH)
        self.upperFrame = Frame(self.container)
        self.upperFrame.pack(expand=True, fill=BOTH, side=TOP)

        self.text_frame = Frame(self.upperFrame, bd=0)
        self.text_frame.pack(expand=True, fill=BOTH, side=LEFT)
        
        # scrollbar for text box
        self.text_box_scrollbar = Scrollbar(self.text_frame, bd=0)
        self.text_box_scrollbar.pack(fill=Y, side=RIGHT)
        
        self.users_frame = Frame(self.upperFrame, bd=0)
        self.users_frame.pack(fill=BOTH, side=LEFT)
        

        # contains messages
        self.text_box = Text(self.text_frame, yscrollcommand=self.text_box_scrollbar.set, state=DISABLED,
                             bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 10", relief=GROOVE,
                             width=10, height=1)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        # frame containing user entry field
        self.entry_frame = Frame(self.container, bd=0)
        self.entry_frame.pack(side=BOTTOM, fill=X, expand=False)

        # entry field
        self.entry_field = Entry(self.entry_frame, bd=0, justify=LEFT)
        self.entry_field.pack(fill=X, padx=6, pady=6, ipady=3)
        self.entry_field.focus()
        # self.users_message = self.entry_field.get()
        
        # frame containing send button and emoji button
        self.send_button_frame = Frame(self.entry_frame, bd=0)
        self.send_button_frame.pack(fill=BOTH)

        # send button
      

# Execute Tkinter
