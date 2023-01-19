import os
from MenuAuthentification import authentifier_choix
from Chatroom import chatroom_menu
from MenuHachage import hachage_menu
from MenuSymetrique import symetrique_menu
from MenuAsymetrique import asymetrique_menu
from art import *
def main():
    os.system('cls')
    tprint("Welcome")
    utilisateur = authentifier_choix()
    choix = ''
    while True:
        tprint("Security Project")
        utilisateur.afficher()
        print()
        print("---------------Menu Principal--------------")
        print("1- Hachage d'un message")
        print("2- Chiffrement et déchiffrement symétrique d'un message")
        print("3- Chiffrement et déchiffrement asymétrique d'un message")
        print("4- Chatroom")
        print("5- Quitter")
        print("-------------------------------------------")
        choix = input("Donner le numero du choix:\n> ")
       
        if (choix == '1'):
            hachage_menu()
        if (choix == '2'):
            symetrique_menu()
        if (choix == '3'):
            asymetrique_menu()
        if (choix == '4'):
            chatroom_menu(utilisateur)
        if (choix == '5'):
            exit()


if __name__ == "__main__":
    main()
