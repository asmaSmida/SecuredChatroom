import os
from MenuAuthentification import authentifier_choix
from Chatroom import chatroom_menu
from MenuEncodage import encodage_menu
from MenuHachage import hachage_menu
from MenuCrackage import crackage_menu
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
        print("1- Encodage et Decodage d'un message")
        print("2- Hachage d'un message")
        print("3- Crackage d'un message haché")
        print("4- Chiffrement et déchiffrement symétrique d'un message")
        print("5- Chiffrement et déchiffrement asymétrique d'un message")
        print("6- Chatroom")
        print("7- Quitter")
        print("-------------------------------------------")
        choix = input("Donner le numero du choix:\n> ")
        if (choix == '1'):
            encodage_menu()
        if (choix == '2'):
            hachage_menu()
        if (choix == '3'):
            crackage_menu()
        if (choix == '4'):
            symetrique_menu()
        if (choix == '5'):
            asymetrique_menu()
        if (choix == '6'):
            chatroom_menu(utilisateur)
        if (choix == '7'):
            exit()


if __name__ == "__main__":
    main()
