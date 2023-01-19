import os
from serveur import initialize_and_start_server
from client import initialize_and_start_client
from Utilisateur import Utilisateur


def chatroom_menu(utilisateur : Utilisateur):
    choix = ''
    while (choix != '3'):
        os.system('clear')
        print("---------------Menu Chatroom--------------")
        print("1- Executer autant que server")
        print("2- Executer autant que client")
        print("3- Revenir au menu principal")
        print("-------------------------------------------")
        choix = input("Donner le numero du choix:\n> ")
        if (choix == '1'):
            initialize_and_start_server()
        if (choix == '2'):
            username=''+utilisateur.prenom+' '+utilisateur.nom
            initialize_and_start_client(username)
        if (choix == '3'):
            break
