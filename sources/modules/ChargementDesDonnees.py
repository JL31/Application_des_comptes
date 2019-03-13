# coding: utf-8

""" Module qui contient la classe ChargementDesDonnees pour l'application des comptes """


### Paramètres globaux

__author__ = "Julien LEPAIN"
__version__ = 1.0
__all__ = ["ChargementDesDonnees"]


### Import des librairies

import os
import pandas as pd


### Définitions des classes

class ChargementDesDonnees(object):
    """
        Classe de chargement des données située dans le dossier Donnees
        Le chargement se fait automatiquement à l'ouverture de l'application
    """
    
    def __init__(self, nom_absolu_du_dossier_contenant_les_donnees, fichier_de_donnees, option):
        """
            Constructeur de la classe
        """
        
        self._nom_absolu_du_dossier_contenant_les_donnees = nom_absolu_du_dossier_contenant_les_donnees
        self._fichier_de_donnees = fichier_de_donnees
        self._option = option
        
        self._nom_absolu_du_fichier_de_donnees = ""
        
        self._separator = ','
        self._encoding = "iso-8859-1"
        self._nombre_de_lignes_a_ignorer = 1
        
        self._date_de_mise_a_jour = None
        self._total_annee_precedente_lui = None
        self._total_annee_precedente_elle = None
        
        self._premiere_ligne_du_fichier = None
        
        self._donnees = None
        
        self._total = None
        self._total_lui = None
        self._total_elle = None
        
    
    ### Accesseurs et mutateurs
    
    def get_nom_absolu_du_dossier_contenant_les_donnees(self):
        """
            Accesseur de l'attribut _nom_absolu_du_dossier_contenant_les_donnees
        """
        
        return self._nom_absolu_du_dossier_contenant_les_donnees
        
    
    def get_fichier_de_donnees(self):
        """
            Accesseur de l'attribut _fichier_de_donnees
        """
        
        return self._fichier_de_donnees
        
    
    def get_nom_absolu_du_fichier_de_donnees(self):
        """
            Accesseur de l'attribut _nom_absolu_du_fichier_de_donnees
        """
        
        return self._nom_absolu_du_fichier_de_donnees
        
    
    def set_nom_absolu_du_fichier_de_donnees(self, valeur):
        """
            Accesseur de l'attribut _nom_absolu_du_fichier_de_donnees
        """
        
        self._nom_absolu_du_fichier_de_donnees = valeur
        
    
    def get_separator(self):
        """
            Accesseur de l'attribut _separator
        """
        
        return self._separator
        
    
    def get_donnees(self):
        """
            Accesseur de l'attribut _donnees
        """
        
        return self._donnees
        
    
    def set_donnees(self, valeurs):
        """
            Mutateur de l'attribut _donnees
        """
        
        self._donnees = valeurs
        
    
    def get_total(self):
        """
            Accesseur de l'attribut _total
        """
        
        return str(round(self._total, 2))
        
    
    def set_total(self, valeurs):
        """
            Mutateur de l'attribut _total
        """
        
        self._total = valeurs
        
    
    def get_total_lui(self):
        """
            Accesseur de l'attribut _total_lui
        """
        
        return str(round(self._total_lui, 2))
        
    
    def set_total_lui(self, valeurs):
        """
            Mutateur de l'attribut _total_lui
        """
        
        self._total_lui = valeurs
        
    
    def get_total_elle(self):
        """
            Accesseur de l'attribut _total_elle
        """
        
        return str(round(self._total_elle, 2))
        
    
    def set_total_elle(self, valeurs):
        """
            Mutateur de l'attribut _total_elle
        """
        
        self._total_elle = valeurs
        
    
    def get_date_de_mise_a_jour(self):
        """
            Accesseur de l'attribut _date_de_mise_a_jour
        """
        
        return self._date_de_mise_a_jour
        
    
    def set_date_de_mise_a_jour(self, valeurs):
        """
            Mutateur de l'attribut _date_de_mise_a_jour
        """
        
        self._date_de_mise_a_jour = valeurs
        
    
    def get_total_annee_precedente_lui(self):
        """
            Accesseur de l'attribut _total_annee_precedente_lui
        """
        
        return self._total_annee_precedente_lui
        
    
    def set_total_annee_precedente_lui(self, valeurs):
        """
            Mutateur de l'attribut _total_annee_precedente_lui
        """
        
        self._total_annee_precedente_lui = valeurs
        
    
    def get_total_annee_precedente_elle(self):
        """
            Accesseur de l'attribut _total_annee_precedente_elle
        """
        
        return self._total_annee_precedente_elle
        
    
    def set_total_annee_precedente_elle(self, valeurs):
        """
            Mutateur de l'attribut _total_annee_precedente_elle
        """
        
        self._total_annee_precedente_elle = valeurs        
        
    
    ### Méthodes
    
    def verification_existence_dossier_et_fichier(self):
        """
            Méthode qui permet de vérifier si le dossier et le fichier contenant les données existent
        """
        
        # On commence par vérifier si le dossier contenant les données existe
        
        if not os.path.isdir(self._nom_absolu_du_dossier_contenant_les_donnees):
            
            raise OSError("Le dossier '{}' n'existe pas".format(self._nom_absolu_du_dossier_contenant_les_donnees))
            
        # On vérifie ensuite si le fichier existe dans le répertoire de données
        
        self._nom_absolu_du_fichier_de_donnees = os.path.join(self._nom_absolu_du_dossier_contenant_les_donnees, self._fichier_de_donnees)
        
        if not os.path.isfile(self._nom_absolu_du_fichier_de_donnees):
            
            raise OSError("Le fichier '{}' n'existe pas das le dossier '{}'".format(self._fichier_de_donnees, self._nom_absolu_du_dossier_contenant_les_donnees))
            
    
    def recuperation_des_donnes(self):
        """
            Méthode qui permet de récupérer les données dans un dataframe
            Les données sont dans un fichier ASCII portant l'extension .donnees
            Les données sont séparées par le séparateur défini en attribut de la classe
        """
        
        # On commence par vérifier que le fichier existe
        
        self.verification_existence_dossier_et_fichier()
        
        # Si le fichier existe on récupère :
        # - la date de dernière mise-à-jour du fichier
        # - le contenu du fichier que l'on place dans un dataframe
        
        with open(self._nom_absolu_du_fichier_de_donnees, 'r') as fichier_contenant_les_donnes:
            
            self._premiere_ligne_du_fichier = fichier_contenant_les_donnes.readline()
            self._date_de_mise_a_jour = self._premiere_ligne_du_fichier.split(',')[0].strip()
            
            if self._option in ["balance"]:
                
                self._total_annee_precedente_lui   = self._premiere_ligne_du_fichier.split(',')[1].strip()
                self._total_annee_precedente_elle = self._premiere_ligne_du_fichier.split(',')[2].strip()
                

        self._donnees = pd.read_csv(self._nom_absolu_du_fichier_de_donnees, sep=self._separator, encoding=self._encoding, skiprows=self._nombre_de_lignes_a_ignorer)
        
    
    def calcul_du_total(self):
        """
            Méthode qui permet de calculer le montant total
        """
        
        df_donnees = self._donnees
        self._total = df_donnees["Montant"].sum()
        
    
    def calcul_du_total_lui(self):
        """
            Méthode qui permet de calculer le montant total pour lui
        """
        
        df_donnees = self._donnees
        self._total_lui = df_donnees["Montant lui"].sum()
        
    
    def calcul_du_total_elle(self):
        """
            Méthode qui permet de calculer le montant total pour elle
        """
        
        df_donnees = self._donnees
        self._total_elle = df_donnees["Montant elle"].sum()
        

### Utilisation

if __name__ == "__main__":
    
    print("Ce module n'est pas voué a être exécuté seul")
