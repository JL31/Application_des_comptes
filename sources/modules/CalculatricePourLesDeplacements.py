# coding: utf-8

""" Module qui contient la classe CalculatricePourLesDeplacements pour l'application des comptes """


### Paramètres globaux

__author__ = "Julien LEPAIN"
__version__ = 1.0
__all__ = ["CalculatricePourLesDeplacements"]


### Import des librairies

# Import des librairies graphiques
from PyQt4 import QtGui, QtCore
import Calculatrice_trajets
import SousClassementDesQValidators

# Import des autres librairies
import os
from datetime import datetime


### Définitions des classes

# class CalculatricePourLesDeplacements(QtGui.QDialog, Calculatrice_trajets.Ui_Dialog):
class CalculatricePourLesDeplacements(QtGui.QDialog, Calculatrice_trajets.Ui_Dialog):
    """
        Classe qui permet de récupérer le mot de passe pour la connexion à la boîte mail
    """
    
    # Signal lié au total calculé : attribut _total
    total_a_envoyer = QtCore.pyqtSignal(str)
    
    def __init__(self, parent=None):
        """
            Constructeur de la classe
        """
        
        super(CalculatricePourLesDeplacements, self).__init__(parent)
        self.setupUi(self)
        
        # Attributs
        
        self._contenu_LE_Distance = ""
        self._contenu_LE_Prix_carburant = ""
        self._contenu_LE_Consommation = ""
        
        self._LE_Distance = 0.0
        self._LE_Prix_carburant = 0.0
        self._LE_Consommation = 0.0
        
        self._total = 0
        
        ### Positionnement de la fenêtre sur l'écran
        
        # self.positionnement_de_la_fenetre_sur_l_ecran()
        
        ### Connexion des widgets
        
        self.connections_des_widgets()
        
        ### Définition, paramétrage et affectation des QValidator pour les QLineEdit
        
        self.parametrage_et_affectation_des_QValidator()
        
    
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
        
    
    def parametrage_et_affectation_des_QValidator(self):
        """
            Méthode qui permet de définir, paramétrer et affecter les QValidator
        """
        
        self._QDouble_validator = SousClassementDesQValidators.SCQDoubleValidation(0.0, 10000.0)
        self._QDouble_validator.setDecimals(2)
        self.LE_Distance.setValidator(self._QDouble_validator)
        
        self._QDouble_validator = SousClassementDesQValidators.SCQDoubleValidation(0.0, 3.0)
        self._QDouble_validator.setDecimals(3)
        self.LE_Prix_carburant.setValidator(self._QDouble_validator)
        
        self._QDouble_validator = SousClassementDesQValidators.SCQDoubleValidation(0.0, 30.0)
        self._QDouble_validator.setDecimals(1)
        self.LE_Consommation.setValidator(self._QDouble_validator)
        
    
    def calcul_du_total(self):
        """
            Méthode qui permet de calculer le total en fonction :
            - de la distance parcourue (en km) ;
            - du prix du carburant (en €/L) ;
            - de la consommation (en L/100 km).
        """
        
        # Récupération du contenu des QLineEdit
        
        self._contenu_LE_Distance       = self.LE_Distance.text()
        self._contenu_LE_Prix_carburant = self.LE_Prix_carburant.text()
        self._contenu_LE_Consommation   = self.LE_Consommation.text()
        
        
        # Récupération de la distance
        
        if self._contenu_LE_Distance != "":
            
            self._LE_Distance = float(self._contenu_LE_Distance)
            
        
        # Récupération du prix carburant
        
        if self._contenu_LE_Prix_carburant != "":
            
            self._LE_Prix_carburant = float(self._contenu_LE_Prix_carburant)
            
        
        # Récupération de la consommation
        
        if self._contenu_LE_Consommation != "":
            
            self._LE_Consommation = float(self._contenu_LE_Consommation)
            
        
        # Calcul du total en fonction des élemtns défini précédemment
        
        self._total = round(self._LE_Distance * self._LE_Consommation / 100.0 * self._LE_Prix_carburant, 2)
        self._total = str(self._total)
        
        
        # Affectation du total au QLineEdit associé
        
        self.LE_Total.setText(self._total)
        
    
    def inserer_nouvelle_ligne_dans_balance(self):
        """
            Méthode qui permet d'insérer une nouvelle ligne dans la balance d'après le total calculé
        """
        
        self.total_a_envoyer.emit(self._total)
        self.fermer_fenetre()
        
    
    def fermer_fenetre(self):
        """
            Méthode qui permet de fermer la fenêtre actuelle
        """
        
        self.close()
        
    
    def connections_des_widgets(self):
        """
            Méthode qui permet de connecter les widgets
        """
        
        # Connexion des QLineEdit
        self.LE_Distance.textChanged.connect(self.calcul_du_total)
        self.LE_Prix_carburant.textChanged.connect(self.calcul_du_total)
        self.LE_Consommation.textChanged.connect(self.calcul_du_total)
        
        # Connexion des QButton
        self.B_Inserer_total.clicked.connect(self.inserer_nouvelle_ligne_dans_balance)
        self.B_Fermer.clicked.connect(self.fermer_fenetre)
        
    
    def main(self):
        """
            Main de la classe
        """
        
        self.show()
        

### Utilisation

if __name__ == "__main__":
    
    print("Ce module n'a pas vocation à être exécuté seul.")
