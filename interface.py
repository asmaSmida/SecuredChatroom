from tkinter import *
from tkinter import ttk
import time
import re
import os
import string
import tkinter as tk
#import webbrowser
import random
from threading import Thread

from Crypto.PublicKey import RSA
#from encryption_decryption import rsa_encrypt, rsa_decrypt
#, get_rsa_key
import pika


saved_username = ["You"]

# checks if username file exists, if not, makes one.
if not os.path.isfile("usernames.txt"):
    # doesnt exist, creates usernames.txt file
    # print('"username.txt" file doesn\'t exist. Creating new file.')
    with open ("usernames.txt", 'wb') as file:
        pass

else:
    # file exists, takes all existing usernames stored in file and adds them to saved_username list
    # print('"username.txt" file found.')
    with open("usernames.txt", 'r') as file:
        for line in file:
            saved_username.append(line.replace("\n", ""))
    pass


# checks if default_win_size file exists, if not, makes one.
if not os.path.isfile("default_win_size.txt"):
    # doesnt exist, creates default_win_size.txt file
    # print('"default_win_size.txt" file doesn\'t exist. Creating new file.')
    with open("default_win_size.txt", 'wb') as file:
        pass

    default_window_size = "600x500"

else:
    # file exists, takes existing window size and defines it
    #print('"default_win_size.txt" file found.')
    with open("default_win_size.txt", 'r') as file:
        size = file.readlines()
        default_window_size= ''.join(size)
        # default_window_size = "600x400"


class ChatInterface(Frame):

    def __init__(self, master=None, fullname=""):
        Frame.__init__(self, master)
        self.master = master
        self.selectedRoom=''
        self.selectedUser=''
        self.talking_users = {}
        self.tabs=[]
        self.theme_function=self.color_theme_hacker
        # self.username = ''.join(random.sample(string.ascii_lowercase,10)) #LDAP LOGIN RETURNS LATER
        self.username = fullname
        #OUR CONNECTION, SHOULD ONLY HAVE ONE PER APP(CLIENT)
        

        # sets default bg for top level windows
        self.tl_bg = "#EEEEEE"
        self.tl_bg2 = "#EEEEEE"
        self.tl_fg = "#000000"
        self.font = "Verdana 10"

        menu = Menu(self.master)
        self.master.config(menu=menu, bd=5)
# Menu bar

  
    # Options
        options = Menu(menu, tearoff=0)
        menu.add_cascade(label="Options", menu=options)

        # username
        username = Menu(options, tearoff=0)
        options.add_cascade(label="Username", menu=username)
        username.add_command(label="Change Username", command=lambda: self.change_username(height=80))
       
        options.add_separator()

        # font
        font = Menu(options, tearoff=0)
        options.add_cascade(label="Font", menu=font)
        font.add_command(label="Default", command=self.font_change_default)
        font.add_command(label="Times", command=self.font_change_times)
        font.add_command(label="System", command=self.font_change_system)
        font.add_command(label="Helvetica", command=self.font_change_helvetica)
        font.add_command(label="Fixedsys", command=self.font_change_fixedsys)

        # color theme
        def theme_change(theme_function):
            self.theme_function = theme_function
            theme_function()
        color_theme = Menu(options, tearoff=0)
        options.add_cascade(label="Color Theme", menu=color_theme)
        color_theme.add_command(label="Default", command=lambda:theme_change(self.color_theme_default))
        color_theme.add_command(label="Night", command=lambda:theme_change(self.color_theme_dark))
        color_theme.add_command(label="Grey", command=lambda:theme_change(self.color_theme_grey))
        color_theme.add_command(label="Blue", command=lambda:theme_change(self.color_theme_dark_blue))
        color_theme.add_command(label="Pink", command=lambda:theme_change(self.color_theme_pink))
        color_theme.add_command(label="Turquoise", command=lambda:theme_change(self.color_theme_turquoise))
        color_theme.add_command(label="Hacker", command=lambda:theme_change(self.color_theme_hacker))

        # all to default
        options.add_command(label="Default layout", command=self.default_format)

        options.add_separator()

        # change default window size
        # change default window size
        options.add_command(label="Change Default Window Size", command=self.change_default_window_size)

        # default window size
        options.add_command(label="Default Window Size", command=self.default_window_size)

     # Rooms
        help_option = Menu(menu, tearoff=0)
        menu.add_cascade(label="Rooms", menu=help_option)
        help_option.add_command(label="room 1", command=lambda : self.on_room_select("room1"))
        help_option.add_command(label="room 2", command=lambda : self.on_room_select("room2"))
        help_option.add_command(label="room 3", command=lambda : self.on_room_select("room3"))
        help_option.add_command(label="room 4", command=lambda : self.on_room_select("room4"))

    # Help
        help_option = Menu(menu, tearoff=0)
        menu.add_cascade(label="Help", menu=help_option)
        help_option.add_command(label="Features", command=self.features_msg)
        help_option.add_command(label="About", command=self.about_msg)

    # Chat interface
        # frame containing text box with messages and scrollbar

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
        
        self.usersPanel= Listbox(self.users_frame, selectmode=SINGLE)
        self.usersPanel.insert(1,"User 1")
        self.usersPanel.pack(expand=True, fill=BOTH)
        self.usersPanel.select_set(0) #This only sets focus on the first item.
        self.usersPanel.bind('<<ListboxSelect>>', self.on_user_select)


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
        self.send_button = Button(self.send_button_frame, text="Send", width=5, relief=GROOVE, bg='white',
                                  bd=1, command=lambda: self.send_message(None), activebackground="#FFFFFF",
                                  activeforeground="#000000")
        self.send_button.pack(side=LEFT, ipady=2)
        self.container.bind("<Return>", self.send_message_event)

        # emoticons
        self.emoji_button = Button(self.send_button_frame, text="☺", width=2, relief=GROOVE, bg='white',
                                   bd=1, command=self.emoji_options, activebackground="#FFFFFF",
                                   activeforeground="#000000")
        self.emoji_button.pack(side=RIGHT, padx=6, pady=6, ipady=2)

        self.last_sent_label(date="No messages sent.")
        self.notebook.add(self.container,text="Main Tab [Rooms]")
        
        

        self.get_rooms()
        self.get_connected_users()
  
    def last_sent_label(self, date):

        try:
            self.sent_label.destroy()
        except AttributeError:
            pass

        self.sent_label = Label(self.entry_frame, font="Verdana 7", text=date, bg=self.tl_bg2, fg=self.tl_fg)
        self.sent_label.pack(side=LEFT, fill=X, padx=3)
# Interface Function 
    def generate_tab(self,username="Pardefaut",userqueue=None):
        newTab = Frame(self.notebook,bd=0)
        text_frame = Frame(newTab, bd=0)
        text_frame.pack(expand=True, fill=BOTH, side=TOP)
        text_box_scrollbar = Scrollbar(text_frame, bd=0)
        text_box_scrollbar.pack(fill=Y, side=RIGHT)
        text_box = Text(text_frame, yscrollcommand=text_box_scrollbar.set, state=DISABLED,
                             bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font="Verdana 10", relief=GROOVE,
                             width=10, height=1)
        text_box.pack(expand=True, fill=BOTH)
        text_box_scrollbar.config(command=text_box.yview)

        # frame containing user entry field
        entry_frame = Frame(newTab, bd=1)
        entry_frame.pack(side=BOTTOM, fill=BOTH, expand=False)

        # entry field
        entry_field = Entry(entry_frame, bd=1, justify=LEFT)
        entry_field.pack(fill=X, padx=6, pady=6, ipady=3)
        entry_field.focus()
        # users_message = entry_field.get()

        # frame containing send button and emoji button
        def sending_message():
           # sender = SenderBroker(userqueue)
            # Get destination user pubkey
            dest_user_pubkey = self.talking_users[userqueue]['pubkey']
            message = entry_field.get()
            # Encrypt msg with dest user pubkey
            encrypted_msg = rsa_encrypt(message, dest_user_pubkey)
            print("[!] Sending encrypted msg: \n" + encrypted_msg.decode()[:40])
            sender.send_message("messageSent::"+self.queue_name+"::"+encrypted_msg.decode())
            text_box.configure(state=NORMAL)
            text_box.insert(END, str(time.strftime('%I:%M:%S ')) +'Me: '+ message+'\n')
            self.last_sent_label(str(time.strftime( "Last message sent: " + '%B %d, %Y' + ' at ' + '%I:%M %p')))
            text_box.see(END)
            text_box.configure(state=DISABLED)
            entry_field.delete(0, END)
        # send button
        send_button = Button(entry_frame, text="Send", width=5, relief=GROOVE, bg='white',
                                  bd=1, command=lambda: sending_message(), activebackground="#FFFFFF",
                                  activeforeground="#000000")
        send_button.pack(side=LEFT, ipady=2)
        newTab.bind("<Return>", sending_message)
        
        self.notebook.add(newTab,text=username)
        self.notebook.select(newTab)
        self.tabs.append(newTab)
        self.theme_function()
        return newTab,text_box
# File functions
    def client_exit(self):
        exit()

    
    def save_chat(self):
        # creates unique name for chat log file
        time_file = str(time.strftime('%X %x'))
        remove = ":/ "
        for var in remove:
            time_file = time_file.replace(var, "_")

        # gets current directory of program. creates "logs" folder to store chat logs.
        path = os.getcwd() + "\\logs\\"
        new_name = path + "log_" + time_file
        saved = "Chat log saved to {}\n".format(new_name)

        # saves chat log file
        try:
            with open(new_name, 'w')as file:
                self.text_box.configure(state=NORMAL)
                log = self.text_box.get(1.0, END)
                file.write(log)
                self.text_box.insert(END, saved)
                self.text_box.see(END)
                self.text_box.configure(state=DISABLED)

        except UnicodeEncodeError:
            # displays error when trying to save chat with unicode. (fix in future)
            self.error_window("Unfortunately this chat can't be saved as of this \nversion "
                              "because it contains unicode characters.", type="simple_error", height='100')

    # clears chat
    def clear_chat(self):
        self.text_box.config(state=NORMAL)
        self.last_sent_label(date="No messages sent.")
        self.text_box.delete(1.0, END)
        self.text_box.delete(1.0, END)
        self.text_box.config(state=DISABLED)

# Help functions
    def features_msg(self):
        msg_box = Toplevel()
        msg_box.configure(bg=self.tl_bg)

    def about_msg(self):
        about_message = "This is a chat interface created in " \
                        "Python by 3 of us, Jihed CHALGHAF - Khalil MEJRI - Mohammed Ali Marzouk. we started this " \
                        "project to help continue to grow our skills " \
                        "in python, especially with larger, more " \
                        "complex class based programs. This is our " \
                        "largest project with a UI so far. There are " \
                        "still many features we would like to add in " \
                        "the future."
        self.error_window(about_message, type="simple_error", height='140')

    def src_code_msg(self):
        webbrowser.open('https://github.com/khalilMejri/Talky-Walky')

# creates top level window with error message
    def error_window(self, error_msg, type="simple_error", height='100', button_msg="Okay"):
        # try's to destroy change username window if its an error with username content
        try:
            self.change_username_window.destroy()
        except AttributeError:
            pass

        # makes top level with placement relative to root and specified error msg
        self.error_window_tl = Toplevel(bg=self.tl_bg)
        self.error_window_tl.focus_set()
        self.error_window_tl.grab_set()

        # gets main window width and height to position change username window
        half_root_width = root.winfo_x()
        half_root_height = root.winfo_y() + 60
        placement = '400x' + str(height) + '+' + str(int(half_root_width)) + '+' + str(int(half_root_height))
        self.error_window_tl.geometry(placement)

        too_long_frame = Frame(self.error_window_tl, bd=5, bg=self.tl_bg)
        too_long_frame.pack()

        self.error_scrollbar = Scrollbar(too_long_frame, bd=0)
        self.error_scrollbar.pack(fill=Y, side=RIGHT)

        error_text = Text(too_long_frame, font=self.font, bg=self.tl_bg, fg=self.tl_fg, wrap=WORD, relief=FLAT,
                          height=round(int(height)/30), yscrollcommand=self.error_scrollbar.set)
        error_text.pack(pady=6, padx=6)
        error_text.insert(INSERT, error_msg)
        error_text.configure(state=DISABLED)
        self.error_scrollbar.config(command=self.text_box.yview)

        button_frame = Frame(too_long_frame, width=12)
        button_frame.pack()

        okay_button = Button(button_frame, relief=GROOVE, bd=1, text=button_msg, font=self.font, bg=self.tl_bg,
                             fg=self.tl_fg, activebackground=self.tl_bg, width=5, height=1,
                             activeforeground=self.tl_fg, command=lambda: self.close_error_window(type))
        okay_button.pack(side=LEFT, padx=5)

        if type == "username_history_error":
            cancel_button = Button(button_frame, relief=GROOVE, bd=1, text="Cancel", font=self.font, bg=self.tl_bg,
                             fg=self.tl_fg, activebackground=self.tl_bg, width=5, height=1,
                             activeforeground=self.tl_fg, command=lambda: self.close_error_window("simple_error"))
            cancel_button.pack(side=RIGHT, padx=5)

    def color_theme_hacker(self):
        self.master.config(bg="#0F0F0F")
        self.text_frame.config(bg="#0F0F0F")
        self.users_frame.config(bg="#0F0F0F")
        self.usersPanel.config(bg="#0F0F0F", fg="#33FF33", selectbackground="#336633", selectforeground="#33FF33")
        self.entry_frame.config(bg="#0F0F0F")
        self.text_box.config(bg="#0F0F0F", fg="#33FF33")
        self.entry_field.config(bg="#0F0F0F", fg="#33FF33", insertbackground="#33FF33")
        self.send_button_frame.config(bg="#0F0F0F")
        self.send_button.config(bg="#0F0F0F", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")
        self.emoji_button.config(bg="#0F0F0F", fg="#FFFFFF", activebackground="#0F0F0F", activeforeground="#FFFFFF")
        self.sent_label.config(bg="#0F0F0F", fg="#33FF33")

        self.tl_bg = "#0F0F0F"
        self.tl_bg2 = "#0F0F0F"
        self.tl_fg = "#33FF33"
        for tab in self.tabs:
            self.apply_theme_tab(tab,self.tl_bg,self.tl_bg2,self.tl_fg)
    # Default font and color theme
    def default_format(self):
        self.font_change_default()
        self.color_theme_hacker()

# Change Username or window size window
    def change_username(self, type="username", label=None, height=None):
        self.change_username_window = Toplevel()

        if type == "username":
            self.change_username_window.bind("<Return>", self.change_username_main_event)
        elif type == "window_size":
            self.change_username_window.bind("<Return>", self.change_window_size_event)

        self.change_username_window.configure(bg=self.tl_bg)
        self.change_username_window.focus_set()
        self.change_username_window.grab_set()

        # gets main window width and height to position change username window
        half_root_width = root.winfo_x()+100
        half_root_height = root.winfo_y()+60
        placement = '180x' + str(height) + '+' + str(int(half_root_width)) + '+' + str(int(half_root_height))
        self.change_username_window.geometry(placement)

        # frame for entry field
        enter_username_frame = Frame(self.change_username_window, bg=self.tl_bg)
        enter_username_frame.pack(pady=5)

        if label:
            self.window_label = Label(enter_username_frame, text=label, fg=self.tl_fg)
            self.window_label.pack(pady=4, padx=4)

        self.username_entry = Entry(enter_username_frame, width=22, bg=self.tl_bg, fg=self.tl_fg, bd=1,
                      insertbackground=self.tl_fg)
        self.username_entry.pack(pady=3, padx=10)

        # Frame for Change button and cancel button
        buttons_frame = Frame(self.change_username_window, bg=self.tl_bg)
        buttons_frame.pack()

    # implement username/ size
        if type == "username":
            username_command = lambda: self.change_username_main(self.username_entry.get())
        elif type == "window_size":
            username_command = lambda: self.change_window_size_main(self.username_entry.get())

        change_button = Button(buttons_frame, relief=GROOVE, text="Change", width=8, bg=self.tl_bg, bd=1,
                               fg=self.tl_fg, activebackground=self.tl_bg, activeforeground=self.tl_fg,
                               command=username_command)
        change_button.pack(side=LEFT, padx=4, pady=3)


    # cancel
        cancel_button = Button(buttons_frame, relief=GROOVE, text="Cancel", width=8, bg=self.tl_bg, bd=1,
                               fg=self.tl_fg, command=self.close_username_window,
                               activebackground=self.tl_bg, activeforeground=self.tl_fg)
        cancel_button.pack(side=RIGHT, padx=4, pady=3)

# Use default username ("You")
    def default_username(self):
        saved_username.append("You")
        self.send_message_insert("Username changed to default.")

# promps user to Clear username history (deletes usernames.txt file and clears saved_username list)
    def clear_username_history(self):
        self.error_window(error_msg="Are you sure you want to clear your username history?\n", button_msg="Clear",
                          type="username_history_error", height="120")

    def clear_username_history_confirmed(self):
         os.remove("usernames.txt")
         saved_username.clear()
         saved_username.append("You")

         self.send_message_insert("Username history cleared.")
 
# Change Default Window Size
    # called from options, creates window to input dimensions
    def change_default_window_size(self):
        self.change_username(type="window_size", label='Enter "width x height" \n'
                                                       "ex: 500x500", height=125)

    # event window, also gets input and checks if it's valid to use as dimensions
    def change_window_size_event(self, event):
        dimensions_get = self.username_entry.get()

        listed = list(dimensions_get)
        try:
            x_index = listed.index("x")

            # formats height and width into seperate int's
            num_1 = int(''.join(listed[0:x_index]))
            num_2 = int(''.join(listed[x_index + 1:]))

        except ValueError or UnboundLocalError:
            self.error_window(
                error_msg="Invalid dimensions specified. \nPlease Use the format shown in the example.",
                type="dimension_error", height='125')
            self.close_username_window()

        # checks that its not too big or too small
        try:
            if num_1 > 3840 or num_2 > 2160 or num_1 < 360 or num_2 < 200:
                self.error_window(error_msg="Dimensions you specified are invalid.\n"
                                            "Maximum dimensions are 3840 x 2160. \n"
                                            "Minimum dimensions are 360 x 200.",
                                  type="dimension_error", height="140")
            else:
                self.change_window_size_main(dimensions_get)
        except:
            pass

    # change size and saves new default into txt file to remember across sessions
    def change_window_size_main(self, window_size):
        window_size = window_size.lower().replace(" ", "")

        root.geometry(window_size)

        with open("default_win_size.txt", 'w') as file:
            print("New default window size set: " + window_size)
            file.write(window_size)

        self.close_username_window()

        self.send_message_insert("Default window size changed to " + window_size + ".")

# return to default window size
    def default_window_size(self):

        # gets custom default win size from file
        with open("default_win_size.txt", 'r') as file:
            size = file.readlines()
            default_window_size = ''.join(size)

        root.geometry(default_window_size)

        # scrolls to very bottom of textbox
        def see_end():
            self.text_box.configure(state=NORMAL)
            self.text_box.see(END)
            self.text_box.configure(state=DISABLED)
        root.after(10, see_end)

