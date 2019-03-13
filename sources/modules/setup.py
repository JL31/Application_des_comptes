# coding: utf-8

""" Module qui permet de créer un exécutable pour l'application des comptes """


### Import des librairies

from cx_Freeze import setup, Executable


### Appel de la fonction setup

setup(
    name = "Application_des_comptes",
    version = "1.0",
    description = "Application pour faire les comptes",
    executables = [Executable("Application_des_comptes.py")],
)
