# coding: utf-8

""" Module qui contient la classe ActionsAvantDeQuitterLApplication pour l'application des comptes """


### Paramètres globaux

__author__ = "Julien LEPAIN"
__version__ = 1.0
__all__ = ["ActionsAvantDeQuitterLApplication"]


### Import des librairies

# Import des librairies qui contiennent le modèle
from EnvoiMail import EnvoiMail

# Import des autres librairies
import os
import shutil
from datetime import datetime
import pandas as pd


### Définitions des classes

class ActionsAvantDeQuitterLApplication(object):
    """
        Classe de 
    """
    
    def __init__(self, dico_des_parametres, option_enregistrement_copie_fichiers, option_enregistrement_envoi_fichiers):
        """
            Constructeur de la classe
        """
        
        self._dico_des_parametres = dico_des_parametres
        self._option_enregistrement_copie_fichiers = option_enregistrement_copie_fichiers
        self._option_enregistrement_envoi_fichiers = option_enregistrement_envoi_fichiers
        
        self._separator = ','
        self._encoding = "iso-8859-1"
        
        self._nom_de_la_copie_du_fichier_de_donnees = ""
        self._emplacement_absolu_de_la_copie_du_fichier_de_donnees = ""
        
        self._liste_des_fichiers_a_envoyer = []
        self._instance_d_envoi_de_mail = None
        
    
    ### Méthodes
    
    def mise_a_jour_d_un_fichier_de_donnees(self, element):
        """
            Méthode qui permet de mettre à jour un fichier contenant les données (pour les comptes ou pour la balance)
        """
        
        with open(self._dico_des_parametres[element]["nom_du_fichier_de_donnees"], 'w') as fichier_contenant_les_donnes:
            
            if element in ["comptes"]:
                
                fichier_contenant_les_donnes.write(datetime.now().strftime("%d/%m/%Y") + "\n")
                
            if element in ["balance"]:
                
                fichier_contenant_les_donnes.write(datetime.now().strftime("%d/%m/%Y") + ",")
                fichier_contenant_les_donnes.write(self._dico_des_parametres["total_annee_precedente_lui"] + ",")
                fichier_contenant_les_donnes.write(self._dico_des_parametres["total_annee_precedente_elle"] + "\n")
                
        
        self._dico_des_parametres[element]["donnees"].to_csv(self._dico_des_parametres[element]["nom_du_fichier_de_donnees"], sep = self._separator, encoding = self._encoding, index = False, mode  = 'a')
        
    
    def enregistrement_d_une_copie_des_fichiers_de_donnees(self, element):
        """
            Méthode qui permet de copier les fichiers contenant les données pour les comptes et la balance dans un autre répertoire
        """
        
        self._nom_de_la_copie_du_fichier_de_donnees = os.path.basename(self._dico_des_parametres[element]["nom_du_fichier_de_donnees"]).split(".")[0] + \
                                                      "_" + \
                                                      datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + \
                                                      "." + \
                                                      os.path.basename(self._dico_des_parametres[element]["nom_du_fichier_de_donnees"]).split(".")[1]
        
        self._emplacement_absolu_de_la_copie_du_fichier_de_donnees = os.path.join(self._dico_des_parametres["contenu_du_fichier_de_configuration"]["emplacement_absolu_du_dossier_de_copie"], self._nom_de_la_copie_du_fichier_de_donnees)
        
        try:
        # On essaye de déplacer le fichier renommé dans le répertoire de destination
            
            shutil.copy(self._dico_des_parametres[element]["nom_du_fichier_de_donnees"], self._emplacement_absolu_de_la_copie_du_fichier_de_donnees)
            
        except OSError:
        # Il y a eu un problème lors du déplacement du fichier renommé
            
            print("Problème lors du déplacement du fichier {} (anciennement {}) dans le dossier {}\n".format(self._nom_de_la_copie_du_fichier_de_donnees,
                                                                                                             self._dico_des_parametres[element]["nom_du_fichier_de_donnees"],
                                                                                                             self._dico_des_parametres["contenu_du_fichier_de_configuration"]["emplacement_absolu_du_dossier_de_copie"]))
            
        else:
        # Le fichier a bien été déplacé
            
            print("Le fichier {} (anciennement {}) a été déplacé dans le dossier {}\n".format(self._nom_de_la_copie_du_fichier_de_donnees,
                                                                                              self._dico_des_parametres[element]["nom_du_fichier_de_donnees"],
                                                                                              self._dico_des_parametres["contenu_du_fichier_de_configuration"]["emplacement_absolu_du_dossier_de_copie"]))
            
    
    def envoi_des_fichiers_de_donnees(self):
        """
            Méthode qui permet d'envoyer, par mail, une copie des fichiers contenant les données (pour les comptes et la balance)
        """
        
        self._instance_d_envoi_de_mail = EnvoiMail(self._dico_des_parametres["contenu_du_fichier_de_configuration"]["expediteur"], 
                                                   self._dico_des_parametres["contenu_du_fichier_de_configuration"]["destinataire"],
                                                   self._liste_des_fichiers_a_envoyer)
        
        self._instance_d_envoi_de_mail.envoi_du_mail()
        
    
    def execution_des_actions(self):
        """
            Méthode qui permet d'exécuter les différentes actions avant la fermeture de l'application
        """
        
        # Etape 1 - mise-à-jour des fichiers contenant les données des comptes et de la balance
        #   &
        # Etape 2 - Enregistrement d'une copie des fichiers des comptes et de la balance dans un autre répertoire et sous un autre nom
        
        for indice, element in enumerate(self._dico_des_parametres.keys()):
            
            if element not in ["contenu_du_fichier_de_configuration", "total_annee_precedente_lui", "total_annee_precedente_elle"]:
                
                # Etape 1
                self.mise_a_jour_d_un_fichier_de_donnees(element)
                
                # Etape 2
                if self._option_enregistrement_copie_fichiers:
                    
                    self.enregistrement_d_une_copie_des_fichiers_de_donnees(element)
                    
                
                # Préparation de la liste des fichiers à envoyer (pour l'Etape 3)
                self._liste_des_fichiers_a_envoyer.append(self._dico_des_parametres[element]["nom_du_fichier_de_donnees"])
                
        
        # Etape 3 - Envoi par mail d'une copie des fichiers contenant les données des comptes et de la balance
        
        if self._option_enregistrement_envoi_fichiers:
            
            self.envoi_des_fichiers_de_donnees()
            

### Utilisation

if __name__ == "__main__":
    
    print("Ce module n'est pas voué à être exécuté seul")

