import os
from Registration import Registration
from Authentification import Authentification


def authentifier_choix():
    print("---------------Menu Authentification--------------")
    print("1- Se registrer")
    print("2- S'authentifier")
    print("3- Quitter")
    print("-------------------------------------------")
    choix = input("Donner le numero du choix:\n> ")
    authentifie = False
    while (not authentifie):
        if (choix == '1'):
            registration = Registration()
            authentifie, utilisateur = registration.registrer()
            return utilisateur
        if (choix == '2'):
            authentification = Authentification()
            authentifie, utilisateur = authentification.authentifier()
            return utilisateur
        if (choix == '3'):
            exit()
