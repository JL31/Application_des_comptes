# coding: utf-8

""" Module qui contient la classe LectureDuFichierDeConfiguration pour l'application des comptes """


### Paramètres globaux

__author__ = "Julien LEPAIN"
__version__ = 1.0
__all__ = ["LectureDuFichierDeConfiguration"]


### Import des librairies

import os
import json


### Définitions des classes

class LectureDuFichierDeConfiguration(object):
    """
        Classe de lecture du cintenu du fichier de configuration de l'application des comptes
    """
    
    def __init__(self, emplacement_absolu_du_fichier_de_configuration):
        """
            Constructeur de la classe
        """
        
        self._emplacement_absolu_du_fichier_de_configuration = emplacement_absolu_du_fichier_de_configuration
        self._contenu_du_fichier_de_configuration = None
        
    
    ### Accesseurs et mutateurs
    
    def get_emplacement_absolu_du_fichier_de_configuration(self):
        """
            Accesseur de l'attribut _emplacement_absolu_du_fichier_de_configuration
        """
        
        return self._emplacement_absolu_du_fichier_de_configuration
        
    
    def set_emplacement_absolu_du_fichier_de_configuration(self, valeur):
        """
            Accesseur de l'attribut _emplacement_absolu_du_fichier_de_configuration
        """
        
        self._emplacement_absolu_du_fichier_de_configuration = valeur
        
    
    def get_contenu_du_fichier_de_configuration(self):
        """
            Accesseur de l'attribut _contenu_du_fichier_de_configuration
        """
        
        return self._contenu_du_fichier_de_configuration
        
    
    def set_contenu_du_fichier_de_configuration(self, valeur):
        """
            Accesseur de l'attribut _contenu_du_fichier_de_configuration
        """
        
        self._contenu_du_fichier_de_configuration = valeur
        
    
    ### Méthodes
    
    def lecture_du_fichier(self):
        """
            Méthode qui permet de récupérer les informations de configuration de l'appli
            Ces informations se trouvent dans le fichier Controleur.json
            Ce fichier doit se trouver au même emplacement que l'application
        """
        
        # On vérifie si le fichier de configuration existe dans le répertoire contenant l'application
        
        if not os.path.isfile(self._emplacement_absolu_du_fichier_de_configuration):
            
            raise OSError("Le fichier de configuration '{}' n'existe pas das le dossier '{}'".format(os.path.basename(self._emplacement_absolu_du_fichier_de_configuration), os.path.dirname(self._emplacement_absolu_du_fichier_de_configuration)))
            
        # Lecture du fichier de configuration
        
        with open(self._emplacement_absolu_du_fichier_de_configuration, 'r') as fichier_de_configuration:
            
            self._contenu_du_fichier_de_configuration = json.load(fichier_de_configuration)     # ATTENTION : il faut que le fichier JSON soit encodé en ANSI sinon impossible de le lire !
            

### Utilisation

if __name__ == "__main__":
    
    print("Ce module n'est pas voué à être exécuté seul")
