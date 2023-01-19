import os, datetime
import json, socket, threading
from tkinter import *
from tkinter import ttk
from termcolor import colored
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64encode, b64decode
import tkinter as tk
from tkinter import messagebox



class Client(Frame):
    def __init__(self, server, port, username,root):
        Frame.__init__(self, root)
        self.server = server
        self.port = port
        self.username = username
        self.isStopped = False
        self.root = root
        lbl = Label(root, text = "Welcome to your private chatroom  "+self.username,bg="#E4F6F8", font=("Robotto",14))
        lbl.pack(ipady=10)



        
        self.notebook = ttk.Notebook(self.root)
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
                             bd=1, padx=6, pady=6, spacing3=8, wrap=WORD, bg=None, font = ("Robotto", 12), relief=GROOVE,
                             width=10, height=1)
        self.text_box.pack(expand=True, fill=BOTH)
        self.text_box_scrollbar.config(command=self.text_box.yview)

        # frame containing user entry field
        self.entry_frame = Frame(self.container, bd=0)
        self.entry_frame.pack(side=BOTTOM, fill=X, expand=False)

        # entry field
        self.entry_field = Entry(self.entry_frame, bd=0, justify=LEFT,bg="#D3DFDF",relief="solid",font = ("Robotto", 13))
        self.entry_field.pack(fill=X, ipady=10)
        self.entry_field.focus()
       #style the button
        # Create style Object
              
        # frame containing send button and emoji button
        self.send_button_frame = Frame(self.entry_frame, bd=0)
        self.send_button_frame.pack(fill=BOTH)
        self.send_button = Button(self.send_button_frame, text="Send",justify="center",
                                  bd=1, command= self.input_handler, font =('calibri', 15, 'bold'),borderwidth = '4',width=12,bg="#0695FE")
        self.send_button.pack(side=TOP, ipady=3,pady=11)

    def create_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server, self.port))
        except Exception as e:
            print(colored('[!] ' + e.__str__(), 'red'))

        self.s.send(self.username.encode())
        print(colored('[+] Connecte avec succes!', 'green'))
        print(colored('[+] Echangement de cles...', 'yellow'))

        self.create_key_pairs()
        self.exchange_public_keys()
        global secret_key
        secret_key = self.handle_secret()

        print(colored('[+] Initiation complete', 'green'))
        print(colored('[+] Vous pouvez echanger des messages', 'green'))

        message_handler = threading.Thread(target=self.handle_messages, args=())
        message_handler.start()
       # input_handler = threading.Thread(target=self.input_handler, args=())
      #  input_handler.start()
        self.root.mainloop()
        while not self.isStopped:
            continue

    def handle_messages(self):
        while not self.isStopped:
            message = self.s.recv(1024).decode()
            if message:
                key = secret_key
                decrypt_message = json.loads(message)
                iv = b64decode(decrypt_message['iv'])
                cipherText = b64decode(decrypt_message['ciphertext'])
                cipher = AES.new(key, AES.MODE_CFB, iv=iv)
                msg = cipher.decrypt(cipherText)
                current_time = datetime.datetime.now()

                self.text_box.configure(state=NORMAL)
                self.text_box.insert(END, str(current_time.strftime('%I:%M:%S ')) +  msg.decode()+'\n')

                self.text_box.see(END)
                self.text_box.configure(state=DISABLED)
                self.entry_field.delete(0, END)

                print(colored(current_time.strftime('%Y-%m-%d %H:%M:%S ') + msg.decode(), 'green'))
            else:
                print(colored('[!] Connection au serveur perdue', 'red'))
                print(colored('[!] Fermeture de connection', 'red'))
                self.s.shutdown(socket.SHUT_RDWR)
                self.isStopped = True

    def input_handler(self):
     #   while True:
        message =self.entry_field.get()
        if message != "EXIT":
            
       # else:
            key = secret_key
            cipher = AES.new(key, AES.MODE_CFB)
            message_to_encrypt = self.username + ": " + message
            msgBytes = message_to_encrypt.encode()
            encrypted_message = cipher.encrypt(msgBytes)
            iv = b64encode(cipher.iv).decode('utf-8')
            message_to_send = b64encode(encrypted_message).decode('utf-8')
            result = json.dumps({'iv': iv, 'ciphertext': message_to_send})
            current_time = datetime.datetime.now()
            self.text_box.configure(state=NORMAL)
            self.text_box.insert(END, str(current_time.strftime('%I:%M:%S ')) +'Me : ' + message+'\n')

            self.text_box.see(END)
            self.text_box.configure(state=DISABLED)
            self.entry_field.delete(0, END)
            self.s.send(result.encode())

        else:
            self.s.shutdown(socket.SHUT_RDWR)
            self.isStopped = True
            messagebox.showwarning('CONNECTION ENDED',"You have ended the connection with the server !")

    def handle_secret(self):
        secret_key = self.s.recv(1024)
        private_key = RSA.importKey(open(f'chatroom_keys/{self.username}_private_key.pem', 'r').read())
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(secret_key)

    def exchange_public_keys(self):
        try:
            print(colored('[+] Recevoir la cle publique du serveur', 'yellow'))
            server_public_key = self.s.recv(1024).decode()
            server_public_key = RSA.importKey(server_public_key)

            print(colored('[+] Envoyement de cle publique au serveur', 'yellow'))
            public_pem_key = RSA.importKey(open(f'chatroom_keys/{self.username}_public_key.pem', 'r').read())
            self.s.send(public_pem_key.exportKey())
            print(colored('[+] Echangement complete!', 'green'))

        except Exception as e:
            print(colored('[!] ERROR, you messed up something.... ' + str(e), 'red'))

    def create_key_pairs(self):
        try:
            private_key = RSA.generate(2048)
            public_key = private_key.publickey()
            private_pem = private_key.exportKey().decode()
            public_pem = public_key.exportKey().decode()
            with open(f'chatroom_keys/{self.username}_private_key.pem', 'w') as priv:
                priv.write(private_pem)
            with open(f'chatroom_keys/{self.username}_public_key.pem', 'w') as pub:
                pub.write(public_pem)

        except Exception as e:
            print(colored('[!] ERROR, you messed up something.... ' + e.__str__(), 'red'))


def initialize_and_start_client(username):
   
    root = Tk()
    root.title("Chatty Room")
    default_window_size = "600x500"
    root.geometry(default_window_size)
    root.minsize(360, 200)
    root.configure(bg="#E4F6F8")

        # start application
    
    client = Client('127.0.0.1', 8081, username,root)
        # root is your root window
   # root.protocol('WM_DELETE_WINDOW', self.on_closing)
    
  

    client.create_connection()
   