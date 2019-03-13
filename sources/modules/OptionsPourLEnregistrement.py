# coding: utf-8

""" Module qui contient la classe OptionsPourLEnregistrement pour l'application des comptes """


### Paramètres globaux

__author__ = "Julien LEPAIN"
__version__ = 1.0
__all__ = ["OptionsPourLEnregistrement"]


### Import des librairies

# Import des librairies graphiques
from PyQt4 import QtGui, QtCore
import Options_d_enregistrement


### Définitions des classes

class OptionsPourLEnregistrement(QtGui.QDialog, Options_d_enregistrement.Ui_Dialog):
    """
        Classe qui permet de récupérer les options pour d'enregistrement
    """
    
    # Signaux liés aux CB
    option_enregistrement_copies = QtCore.pyqtSignal(bool)
    option_envoi_copies_fichiers_par_mail = QtCore.pyqtSignal(bool)
    
    def __init__(self, parent=None):
        """
            Constructeur de la classe
        """
        
        super(OptionsPourLEnregistrement, self).__init__(parent)
        self.setupUi(self)
        
        # Attributs
        
        # None
        
        ### Positionnement de la fenêtre sur l'écran
        
        # self.positionnement_de_la_fenetre_sur_l_ecran()
        
        ### Connexion des widgets
        
        self.connections_des_widgets()
        
    
    def positionnement_de_la_fenetre_sur_l_ecran(self):
        """
            Méthode qui permet de positioner la fenêtre sur l'écran, en l'occurence de la centrer
        """
        
        
        # # # # # # # # # # pas sûr que ça fonctionne correctement !!!
        
        
        # Renvoie la taille de l'écran
        taille_ecran = QtGui.QDesktopWidget().screenGeometry()
        
        # Renvoie la taille de la fenêtre de l'application
        taille_fenetre = self.geometry()
        
        # Place la fenêtre ...
        self.move((taille_ecran.width() - taille_fenetre.width()) / 2, (taille_ecran.height() - taille_fenetre.height()) / 2)
        
    
    def fermer_fenetre(self):
        """
            Méthode qui permet de fermer la fenêtre actuelle
        """
        
        self.option_enregistrement_copies.emit(self.CB_Enregistrement_copies.checkState())
        self.option_envoi_copies_fichiers_par_mail.emit(self.CB_Envoi_copies_fichiers_par_mail.checkState())
        
        self.close()
        
    
    def connections_des_widgets(self):
        """
            Méthode qui permet de connecter les widgets
        """
        
        # Connexion des QButton
        self.B_Valider_options.clicked.connect(self.fermer_fenetre)
        
    
    def main(self):
        """
            Main de la classe
        """
        
        self.show()
        

### Utilisation

if __name__ == "__main__":
    
    print("Ce module n'a pas vocation à être exécuté seul.")
