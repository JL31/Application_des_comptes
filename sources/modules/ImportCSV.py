# coding: utf-8

""" Module qui contient la classe ImportCSV pour l'application des comptes """


### Paramètres globaux

__author__ = "Julien LEPAIN"
__version__ = 1.0
__all__ = ["ImportCSV"]


### Import des librairies

import os
import pandas as pd
from datetime import datetime


### Définitions des classes

class ImportCSV(object):
    """
        Classe qui permet d'importer un CSV
    """
    
    def __init__(self, fichier_CSV_a_importer, donnees_deja_chargees, liste_des_libelles_lui, liste_des_libelles_elle):
        """
            Constructeur de la classe
        """
        
        self._fichier_CSV_a_importer  = fichier_CSV_a_importer
        self._donnees_deja_chargees   = donnees_deja_chargees
        self._liste_des_libelles_lui  = liste_des_libelles_lui
        self._liste_des_libelles_elle = liste_des_libelles_elle
        
        self._separator = ';'
        self._nombre_de_lignes_a_ignorer = 7
        self._encoding = "iso-8859-1"
        self._colonnes_a_conserver = ["Date",
                                      "Libellé",
                                      "Montant(EUROS)"]
        self._donnees_importees = None
        self._extrait_des_donnees_importees = None
        self._donnees_concatenees = None
        
    
    ### Accesseurs et mutateurs
    
    def get_donnees_importees(self):
        """
            Accesseur de l'attribut _donnees_importees
        """
        
        return self._donnees_importees
        
    
    def set_donnees_importees(self, valeurs):
        """
            Mutateur de l'attribut _donnees_importees
        """
        
        self._donnees_importees = valeurs
        
    
    def get_extrait_des_donnees_importees(self):
        """
            Accesseur de l'attribut _extrait_des_donnees_importees
        """
        
        return self._extrait_des_donnees_importees
        
    
    def set_extrait_des_donnees_importees(self, valeurs):
        """
            Mutateur de l'attribut _extrait_des_donnees_importees
        """
        
        self._extrait_des_donnees_importees = valeurs
        
    
    def get_donnees_concatenees(self):
        """
            Accesseur de l'attribut _donnees_concatenees
        """
        
        return self._donnees_concatenees
        
    
    def set_donnees_concatenees(self, valeurs):
        """
            Mutateur de l'attribut _donnees_concatenees
        """
        
        self._donnees_concatenees = valeurs
        
    
    ### Méthodes
    
    def recuperation_des_donnes(self):
        """
            Méthode qui permet de récupérer les données dans un dataframe
            Toutes les options concernant la fonction de lecture du CSV (read_csv) sont définies en attribut de la classe
        """
        
        self._donnees_importees = pd.read_csv(self._fichier_CSV_a_importer, sep = self._separator, skiprows = self._nombre_de_lignes_a_ignorer, encoding = self._encoding)

        self._donnees_importees = self._donnees_importees.apply(lambda x: x.str.replace(',', '.'))
        self._donnees_importees["Montant(EUROS)"] = self._donnees_importees["Montant(EUROS)"].astype(float)
        
        self._donnees_importees = self._donnees_importees[self._colonnes_a_conserver]
        
    
    def extraction_des_donnees(self):
        """
            Méthode qui permet d'extraire, dans les données lues dans le CSV des données à importer, les données qui n'existent pas dans les données déjà chargées
        """
        
        if len(self._donnees_deja_chargees) > 0:
        # Les données déjà chargées ne sont pas vides
        
            # Récupération de la dernière ligne des données déjà chargées
            
            ligne_derniere_donnee_deja_chargee = self._donnees_deja_chargees.ix[0, :]
            
            # Conversion des dates en objet datetime.strptime avant Vérifications
            
            derniere_date_donnees_importees = datetime.strptime(self._donnees_importees["Date"].values[-1], "%d/%m/%Y")
            derniere_date_donnee_deja_chargees = datetime.strptime(ligne_derniere_donnee_deja_chargee["Date"], "%d/%m/%Y")
            
            # Vérifications 
            
            if derniere_date_donnees_importees > derniere_date_donnee_deja_chargees:
            # La dernière date des données à importer est supérieure à la première date des données déjà chargées :
            # on récupère toutes les données à importer
                
                self._extrait_des_donnees_importees = self._donnees_importees
                
            else:
            # On récupère, dans les données à importer, les lignes qui sont dans les données à importer mais pas dans celles déjà chargées
                
                liste_des_index = self._donnees_importees[(self._donnees_importees["Date"] == ligne_derniere_donnee_deja_chargee["Date"]) & \
                                                          (self._donnees_importees["Libellé"] == ligne_derniere_donnee_deja_chargee["Libellé"]) & \
                                                          (self._donnees_importees["Montant(EUROS)"] == ligne_derniere_donnee_deja_chargee["Montant"]) \
                                                         ].index
                
                indice_pour_extraction = liste_des_index[0] - 1
                
                # Il est possible qu'il y ait des cas où il y aurait deux fois la même ligne, 
                # La ligne précédente permet de s'affranchir d'un éventuel problème dans cette situation (on prend la première référence)
                
                self._extrait_des_donnees_importees = self._donnees_importees.ix[:indice_pour_extraction]
                
        else:
        # Les données déjà chargées sont vides donc on récupère toutes les données à importer
            
            self._extrait_des_donnees_importees = self._donnees_importees
            
        # On initialise les colonnes Montant lui et Montant elle
        
        self._extrait_des_donnees_importees["Montant lui"] = 0.0
        self._extrait_des_donnees_importees["Montant elle"] = 0.0
        self._extrait_des_donnees_importees["statut_export"] = False

    
    def traitement_des_donnees_importees(self):
        """
            Méthode qui permet de traiter les données importées
        """
        
        ### Traitements des donnes à importer :
        # - on renomme la colonne 'Montant(EUROS)' en 'Montant'
        # - on calcule les Montant lui et Montant elle à partir du Montant selon les cas
        
        self._extrait_des_donnees_importees = self._extrait_des_donnees_importees.rename(columns={"Montant(EUROS)": "Montant"})
        
        
        ### Traitement selon le cas : on itère sur les indices du dataframe contenant l'extrait des données importées
        for indice_ligne in self._extrait_des_donnees_importees.index:
            
            # initialisation du booléen qui permet de savoir si le libellé a été trouvé dans l'une des listes (pour lui ou pour elle)
            libelle_trouve = False
            
            # on itère sur les éléments de la liste des libellés pour lui
            for indice, element in enumerate(self._liste_des_libelles_lui):
                
                if element in self._donnees_importees.ix[indice_ligne]["Libellé"]:
                # le libellé a été trouvé dans la liste des libellés pour lui : on lui attribue la totalité du montant (et on passe le booléen libelle_trouve à True)
                    
                    self._extrait_des_donnees_importees.set_value(indice_ligne, "Montant lui", self._extrait_des_donnees_importees.ix[indice_ligne]["Montant"])
                    libelle_trouve = True
                    
            # on itère sur les éléments de la liste des libellés pour elle
            for indice, element in enumerate(self._liste_des_libelles_elle):
                
                if element in self._donnees_importees.ix[indice_ligne]["Libellé"]:
                # le libellé a été trouvé dans la liste des libellés pour elle : on lui attribue la totalité du montant (et on passe le booléen libelle_trouve à True)
                    
                    self._extrait_des_donnees_importees.set_value(indice_ligne, "Montant elle", self._extrait_des_donnees_importees.ix[indice_ligne]["Montant"])
                    libelle_trouve = True
                    
            # si le libellé n'a été trouvé dans aucune des listes alors on divise le montant en deux parts égales
            if not libelle_trouve:
                
                self._extrait_des_donnees_importees.set_value(indice_ligne, "Montant lui", self._extrait_des_donnees_importees.ix[indice_ligne]["Montant"] / 2.0)
                self._extrait_des_donnees_importees.set_value(indice_ligne, "Montant elle", self._extrait_des_donnees_importees.ix[indice_ligne]["Montant"] / 2.0)
                
        
        ### Il faut ensuite ajouter ce dataframe à celui existant : 
        
        self._donnees_concatenees = pd.concat([self._extrait_des_donnees_importees, self._donnees_deja_chargees], ignore_index=True)
        

### Utilisation

if __name__ == "__main__":
    
    print("Ce module n'est pas voué a être exécuté seul")
