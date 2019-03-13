# coding: utf-8

""" Module qui permet de lancer l'application des comptes """


### Paramètres globaux

__author__ = "Julien LEPAIN"
__version__ = 1.0
__all__ = []


### Import des librairies

from PyQt4 import QtGui
import sys
from Controleur import Controleur


### Définitions des classes

# nothing


### Utilisation

if __name__ == "__main__":
    
    app = QtGui.QApplication(sys.argv)
    
    controleur = Controleur(app)
    controleur.main()
    
    app.exec_()
