# coding: utf-8

""" Module qui contient le Controleur pour l'application des comptes """


### Paramètres globaux

__author__ = "Julien LEPAIN"
__version__ = 1.0


### Import des librairies

# Import des librairies graphiques
from PyQt4 import QtGui, QtCore
import Appli_comptes

# Import des librairies qui contiennent le modèle
from LectureDuFichierDeConfiguration import LectureDuFichierDeConfiguration
from ChargementDesDonnees import ChargementDesDonnees
from ModeleComptes import ModeleComptes
from ModeleBalance import ModeleBalance
from ImportCSV import ImportCSV
from ActionsAvantDeQuitterLApplication import ActionsAvantDeQuitterLApplication
from CalculatricePourLesDeplacements import CalculatricePourLesDeplacements
import SousClassementDesQValidators
from OptionsPourLEnregistrement import OptionsPourLEnregistrement

# Import des autres librairies
import sys
import os
from datetime import datetime
import shutil
import webbrowser
import numpy as np
import pandas as pd
import json


### Définitions des classes

class Controleur(QtGui.QMainWindow, Appli_comptes.Ui_MainWindow):
    """
        Classe de lien entre la Vue et le Modèle
    """
    
    def __init__(self, app, parent=None):
        """
            Constructeur de la classe
        """
        
        super(Controleur, self).__init__(parent)
        self.setupUi(self)
        
        ### Attributs
        
        self._app = app
        
            # Instances des classes
        
        self._instance_de_lecture_du_fichier_de_configuration = None
        self._instance_de_chargement_comptes = None
        self._instance_de_chargement_balance = None
        self._instance_des_actions_avant_de_quitter_l_application = None
        self._calculatrice_pour_les_trajets = None
        self._modification_des_options_d_enregistrement = None
        
            # Attributs
        
        self._nom_du_fichier_de_configuration = "Configuration.json"
        self._emplacement_absolu_du_fichier_de_configuration = os.path.abspath("../../Donnees/" + self._nom_du_fichier_de_configuration)
        self._contenu_du_fichier_de_configuration = []
        
        self._emplacement_absolu_des_fichiers_de_donnees = os.path.abspath("../../Donnees")

        self._filtre_fichier_a_importer = "csv (*.csv)"
        
        self._emplacement_absolu_de_la_copie_du_fichier_de_donnees_des_comptes = ""
        self._emplacement_absolu_de_la_copie_du_fichier_de_donnees_de_la_balance = ""
        
        self._dico_des_parametres = {}
        
        self._donnees_comptes = None
        self._modele_comptes = None
        
        self._donnees_balance = None
        self._modele_balance = None
        
        self._total = None
        self._total_lui = None
        self._total_elle = None
        
        self._TVB_date = None
        self._TVB_libelle = None
        self._TVB_montant = None
        self._TVB_payeur = None
        
        self._dico_donnees_a_ajouter = None
        self._donnees_a_concatener = None
        
        self._montant_pour_ajout_balance = None
        
        self._total_calculatrice = 0.0
        
        self._message_box_pour_sauvegarde_donnees = None
        self._choix_sauvegarde_donnees = None
        
        self._menu_contextuel = None
        self._actionCalculatricePourLesTrajets = None
        self._actionModificationDesOptionsDEnregistrement = None
        
        self._option_enregistrement_copie_fichiers = False
        self._option_enregistrement_envoi_fichiers = False
        
        ### Positionnement de la fenêtre sur l'écran
        
        self.positionnement_de_la_fenetre_sur_l_ecran()
        
        ### Initialisation de l'application (via la méthode actions_d_initialisation)
        
        self.actions_d_initialisation()
        
    
    ### Accesseurs et mutateurs
    
    # Nothing
    
    
    ### Méthodes
    
    def positionnement_de_la_fenetre_sur_l_ecran(self):
        """
            Méthode qui permet de positioner la fenêtre sur l'écran, en l'occurence de la centrer
        """
        
        
        # # # # # # # # # # pas sûr que ça fonctionne correctement !!!
        
        
        # Renvoie la taille de l'écran
        taille_ecran = QtGui.QDesktopWidget().screenGeometry()
        
        # Renvoie la taille de la fenêtre de l'application
        taille_fenetre = self.geometry()
        
        # Place la fenêtre au milieu de l'écran
        self.move((taille_ecran.width() - taille_fenetre.width()) / 2, (taille_ecran.height() - taille_fenetre.height()) / 2)
        
    
    def actions_d_initialisation(self):
        """
            Méthode qui permet d'effectuer certaines actions d'initialisations 
        """
        
        # Récupération des informations de configuration, i.e. lecture du fichier de configuration nommé configuration.json
        self.recuperation_des_informations_de_configuration()
        
        # Récupération et remplissage du TV Comptes + mise-à-jour des totaux
        self.recuperation_des_donnees_comptes()
        self.remplissage_du_TV_Comptes()
        self.remplissage_des_totaux_comptes()
        
        # Récupération et remplissage du TV balance + mise-à-jour des totaux
        self.recuperation_des_donnees_balance()
        self.remplissage_du_TV_Balance()
        self.remplissage_des_totaux_balance()
        
        # Remplissage des totaux des années précédentes
        self.remplissage_des_totaux_des_annees_precedentes()
        
        # Remplissage des labels date et fichiers chargés
        self.remplissage_des_labels_date_et_fichiers_charges()
        
        # Mise en forme de certains labels (les couleurs du texte)
        self.mise_en_forme_de_labels()
        
        # Connexion des widgets
        self.connections_des_widgets()
        
        # Définition, paramétrage et affectation des QValidator
        self.parametrage_et_affectation_des_QValidator()
        
    
    def recuperation_des_informations_de_configuration(self):
        """
            Méthode qui permet de récupérer les informations de configuration de l'appli
            Ces informations se trouvent dans le fichier Configuration.json
            Ce fichier doit se trouver au même emplacement que l'application
        """
        
        # Création de l'instance de la classe LectureDuFichierDeConfiguration
        self._instance_de_lecture_du_fichier_de_configuration = LectureDuFichierDeConfiguration(self._emplacement_absolu_du_fichier_de_configuration)
        
        # Lecture du fichier de configuration
        self._instance_de_lecture_du_fichier_de_configuration.lecture_du_fichier()
        
        # Affectation du contenu du fichier de configuration à l'attribut correspondant
        self._contenu_du_fichier_de_configuration = self._instance_de_lecture_du_fichier_de_configuration.get_contenu_du_fichier_de_configuration()
        
    
    def recuperation_des_donnees_comptes(self):
        """
            Méthode qui permet de récupérer les données pour l'onglet des comptes
        """
        
        # Création de l'instance de la classe ChargementDesDonnees pour les comptes
        self._instance_de_chargement_comptes = ChargementDesDonnees(self._emplacement_absolu_des_fichiers_de_donnees, self._contenu_du_fichier_de_configuration["fichier_de_donnees_pour_les_comptes"], "comptes")
        
        # Récupération des données des comptes
        self._instance_de_chargement_comptes.recuperation_des_donnes()
        
        # Affectation des données récupérées à l'attribut correspondant
        self._donnees_comptes = self._instance_de_chargement_comptes.get_donnees()
        
    
    def recuperation_des_donnees_balance(self):
        """
            Méthode qui permet de récupérer les données pour l'onglet de la balance
        """
        
        # Création de l'instance de la classe ChargementDesDonnees pour la balance
        self._instance_de_chargement_balance = ChargementDesDonnees(self._emplacement_absolu_des_fichiers_de_donnees, self._contenu_du_fichier_de_configuration["fichier_de_donnees_pour_la_balance"], "balance")
        
        # Récupération des données de la balance
        self._instance_de_chargement_balance.recuperation_des_donnes()
        
        # Affectation des données récupérées à l'attribut correspondant
        self._donnees_balance = self._instance_de_chargement_balance.get_donnees()
        
    
    def remplissage_du_TV_Comptes(self):
        """
            Méthode qui permet de remplir le TV Comptes
        """
        
        # Création de l'instance de la classe ModeleComptes
        self._modele_comptes = ModeleComptes(self._donnees_comptes)
        
        # Permet de connecter le signal 'dataChanged' émis par l'instance du modèle (ici '_modele_comptes') à la méthode chargée de mettre à jour les totaux (ici 'remplissage_des_totaux_comptes')
        self._modele_comptes.dataChanged.connect(self.remplissage_des_totaux_comptes)
        
        # Affectation du modèle au TV Comptes
        self.TV_Comptes.setModel(self._modele_comptes)
        self.TV_Comptes.hideColumn(self._modele_comptes.columnCount() - 1)

        # Définition, paramétrage et affectation des QValidator pour les cellules
        self.TV_Comptes.setItemDelegate(SousClassementDesQValidators.SCItemDelegateTVComptes())
        
        # Sizing automatique des colonnes
        # # # # # à retravailler !!!
        
        self.TV_Comptes.setColumnWidth(1, 394)
        
    
    def remplissage_du_TV_Balance(self):
        """
            Méthode qui permet de remplir le TV Balance
        """
        
        # Création de l'instance de la classe ModelModeleBalanceeComptes
        self._modele_balance = ModeleBalance(self._donnees_balance)
        
        # Permet de connecter le signal 'dataChanged' émis par l'instance du modèle (ici '_modele_balance') à la méthode chargée de mettre à jour les totaux (ici 'remplissage_des_totaux_comptes')
        self._modele_balance.dataChanged.connect(self.remplissage_des_totaux_balance)     
        
        # Affectation du modèle au TV balance
        self.TV_Balance.setModel(self._modele_balance)
        self.TV_Balance.hideColumn(self._modele_balance.columnCount() - 1)

        # Définition, paramétrage et affectation des QValidator pour les cellules
        self.TV_Balance.setItemDelegate(SousClassementDesQValidators.SCItemDelegateTVBalance())
        
        # Sizing automatique des colonnes
        # # # # # à retravailler !!!
        
        self.TV_Balance.setColumnWidth(1, 494)
        
    
    def remplissage_des_totaux_comptes(self):
        """
            Méthode qui permet de remplir les totaux des comptes
        """
        
        # Appel, via l'instance de chargement des comptes, des méthodes pour le calcul des différents totaux
        self._instance_de_chargement_comptes.calcul_du_total()
        self._instance_de_chargement_comptes.calcul_du_total_lui()
        self._instance_de_chargement_comptes.calcul_du_total_elle()
        
        # Affectation des totaux pour lui et elle par la récupération des totaux calculés précédemment
        self.L_total_comptes_lui.setText(self._instance_de_chargement_comptes.get_total_lui())
        self.L_total_comptes_elle.setText(self._instance_de_chargement_comptes.get_total_elle())
        
        # Appel de la méthode qui calcule les totaux pour affichage dans la fenêtre de l'appli
        self.calcul_des_totaux()
        
        # Appel de la méthode pour la mise en forme totaux
        self.mise_en_forme_des_totaux()
        
    
    def remplissage_des_totaux_balance(self):
        """
            Méthode qui permet de remplir les totaux de la balance
        """
        
        # Appel, via l'instance de chargement de la balance, des méthodes pour le calcul des différents totaux
        self._instance_de_chargement_balance.calcul_du_total_lui()
        self._instance_de_chargement_balance.calcul_du_total_elle()
        
        # Affectation des totaux pour lui et elle par la récupération des totaux calculés précédemment
        self.L_total_balance_lui.setText(self._instance_de_chargement_balance.get_total_lui())
        self.L_total_balance_elle.setText(self._instance_de_chargement_balance.get_total_elle())
        
        # Appel de la méthode qui calcule les totaux pour affichage dans la fenêtre de l'appli
        self.calcul_des_totaux()
        
        # Appel de la méthode pour la mise en forme totaux
        self.mise_en_forme_des_totaux()
        
    
    def remplissage_des_totaux_des_annees_precedentes(self):
        """
            Méthode qui permet de remplir les totaux des années précédentes
        """
        
        # Affectation des totaux des années précédentes pour lui et elle par la récupération de ces valeurs dans l'instance de chargement de la balance
        self.L_total_annee_precedente_lui.setText(self._instance_de_chargement_balance.get_total_annee_precedente_lui())
        self.L_total_annee_precedente_elle.setText(self._instance_de_chargement_balance.get_total_annee_precedente_elle())
        
        # Appel de la méthode qui calcule les totaux pour affichage dans la fenêtre de l'appli
        self.calcul_des_totaux()
        
        # Appel de la méthode pour la mise en forme totaux
        self.mise_en_forme_des_totaux()
        
    
    def calcul_des_totaux(self):
        """
            Méthode qui permet de calculer les totaux (L_Total, L_Total_lui et L_Total_elle)
        """
        
        # Calcul des différents totaux à partir des informations des QLabels
        self._total_lui = float(self.L_total_comptes_lui.text()) + float(self.L_total_balance_lui.text()) + float(self.L_total_annee_precedente_lui.text())
        self._total_elle = float(self.L_total_comptes_elle.text()) + float(self.L_total_balance_elle.text()) + float(self.L_total_annee_precedente_elle.text())
        self._total = self._total_lui + self._total_elle
        
        # Mise-à-jour des valeurs dans la fenêtre de l'appli
        self.L_Total.setText(str(round(self._total, 2)))
        self.L_Total_lui.setText(str(round(self._total_lui,2)))
        self.L_Total_elle.setText(str(round(self._total_elle,2)))

    
    def mise_en_forme_des_totaux(self):
        """
            Méthode qui permet de mettre en forme les totaux (couleur de police)
        """
        
        # Mise en forme du TOTAL sur le compte
        
        if float(self._total) > 0.0:
            
            self.L_Total.setStyleSheet("color: rgb(0,170,0)")
            
        else:
            
            self.L_Total.setStyleSheet("color: rgb(255,0,0)")
            
        # Mise en forme du Total lui
        
        if float(self._total_lui) > 0.0:
            
            self.L_Total_lui.setStyleSheet("color: rgb(0,170,0)")
            
        else:
            
            self.L_Total_lui.setStyleSheet("color: rgb(255,0,0)")
            
        # Mise en forme du Total elle
        
        if float(self._total_elle) > 0.0:
            
            self.L_Total_elle.setStyleSheet("color: rgb(0,170,0)")
            
        else:
            
            self.L_Total_elle.setStyleSheet("color: rgb(255,0,0)")
            
    
    def mise_en_forme_de_labels(self):
        """
            Méthode qui permet de mettre en forme certains labels (couleur de police)
        """
        
        # Mise en forme des Totaux comptes
        
        self.L_total_comptes_lui.setStyleSheet("color: rgb(0,0,0)")
        self.L_total_comptes_elle.setStyleSheet("color: rgb(0,0,0)")
        
        # Mise en forme des Totaux balance
        
        self.L_total_balance_lui.setStyleSheet("color: rgb(0,0,0)")
        self.L_total_balance_elle.setStyleSheet("color: rgb(0,0,0)")
        
        # Mise en forme des Totaux annéée précédente
        
        self.L_total_annee_precedente_lui.setStyleSheet("color: rgb(0,0,0)")
        self.L_total_annee_precedente_elle.setStyleSheet("color: rgb(0,0,0)")
        
        # Mise en forme de la date de la dernière mise-à-jour
        
        self.L_Date_update.setStyleSheet("color: rgb(0,0,0)")
        
        # Mise en forme du fichier de comptes chargé
        
        self.L_Nom_du_fichier_de_comptes_charge.setStyleSheet("color: rgb(0,0,0)")
        
        # Mise en forme du fichier de balance chargé
        
        self.L_Nom_du_fichier_de_balance_charge.setStyleSheet("color: rgb(0,0,0)")
        
    
    def remplissage_des_labels_date_et_fichiers_charges(self):
        """
           Méthode qui permet de remplir les labels de la date de mise-à-jour des comptes ainsi que ceux concernant les fichiers de données chargés     
        """
        
        # Mise-à-jour du label de la date en récupérant cette info dans l'instance de chargement des comptes
        self.L_Date_update.setText(self._instance_de_chargement_comptes.get_date_de_mise_a_jour())
        
        # Mise-à-jour des labels des fichiers chargés en récupérant ces informations dans celles récupérées dans le fichier de configuration
        self.L_Nom_du_fichier_de_comptes_charge.setText(self._contenu_du_fichier_de_configuration["fichier_de_donnees_pour_les_comptes"])
        self.L_Nom_du_fichier_de_balance_charge.setText(self._contenu_du_fichier_de_configuration["fichier_de_donnees_pour_la_balance"])
        
    
    def importer_un_fichier_CSV(self):
        """
            Méthode qui permet, à travers la classe ImportCSV, d'importer un fichier CSV pour ajouter ses données à celles déjà chargées
        """
        
        # Création d'une instance QFileDialog pour demander à l'utilisateur de choisir l'emplacement du fichier
        fichier_CSV = str(QtGui.QFileDialog.getOpenFileName(filter=self._filtre_fichier_a_importer))
        
        # Vérification que l'utilisateur a bien rentré un nom pour le fichier
        if fichier_CSV:
            
            # Création d'une instance de la classe ImportCSV puis utilisation des méthodes de la classe
            import_du_CSV = ImportCSV(fichier_CSV, self._donnees_comptes, self._contenu_du_fichier_de_configuration["liste_des_libelles_lui"], self._contenu_du_fichier_de_configuration["liste_des_libelles_elle"])
            import_du_CSV.recuperation_des_donnes()
            import_du_CSV.extraction_des_donnees()
            import_du_CSV.traitement_des_donnees_importees()
            self._donnees_comptes = import_du_CSV.get_donnees_concatenees()
            
            # Mise-à-jour des données dans l'instance de chargement des comptes
            self._instance_de_chargement_comptes.set_donnees(self._donnees_comptes)
            
            # Remplissage du TV Comptes
            self.remplissage_du_TV_Comptes()
            
            # Mise-à-jour des totaux
            self.remplissage_des_totaux_comptes()
        
    
    def actions_avant_de_quitter_l_application(self):
        """
            Méthode qui permet d'exécuter certaines actions avant de fermer l'application :
                
                1 - Mise-à-jour des fichiers contenant les données (pour les comptes et la balance) ;
                2 - Enregistrement d'une copie de ces fichiers à l'emplacement défini dans le fichier de configuration (Configuration.json).
                    Ces copies porteront un nom différent qui sera constitué de la sorte : nom_du_fichier_initial__jj_mm_aaaa_hh_mm_ss.donnees ;
                3 - Envoi, par mail, d'un copie de ces fichiers (sur la boîte définie dans le fichier de configuration (Configuration.json)).
        """
        
        # Remplissage de l'attribut _dico_des_parametres
        
        self._dico_des_parametres["contenu_du_fichier_de_configuration"] = self._contenu_du_fichier_de_configuration
        self._dico_des_parametres["total_annee_precedente_lui"] = self.L_total_annee_precedente_lui.text()
        self._dico_des_parametres["total_annee_precedente_elle"] = self.L_total_annee_precedente_elle.text()
        
        self._dico_des_parametres["comptes"] = {}
        self._dico_des_parametres["comptes"]["nom_du_fichier_de_donnees"] = self._instance_de_chargement_comptes.get_nom_absolu_du_fichier_de_donnees()
        self._dico_des_parametres["comptes"]["donnees"] = self._donnees_comptes
        
        self._dico_des_parametres["balance"] = {}
        self._dico_des_parametres["balance"]["nom_du_fichier_de_donnees"] = self._instance_de_chargement_balance.get_nom_absolu_du_fichier_de_donnees()
        self._dico_des_parametres["balance"]["donnees"] = self._donnees_balance
        
        # Création de l'instance de la classe "ActionsAvantDeQuitterLApplication" puis exécution des actions via la méthode "execution_des_actions"
        
        self._instance_des_actions_avant_de_quitter_l_application = ActionsAvantDeQuitterLApplication(self._dico_des_parametres, self._option_enregistrement_copie_fichiers, self._option_enregistrement_envoi_fichiers)
        self._instance_des_actions_avant_de_quitter_l_application.execution_des_actions()
        
    
    def sauvegarde_des_donnees(self):
        """
            Méthode qui permet de demander à l'utilisateur s'il souhaite sauvegarder les données avant de quitter l'application
        """
        
        # On créé une instance de la classe QMessageBox
        
        self._message_box_pour_sauvegarde_donnees = QtGui.QMessageBox()
        
        # On configure l'instance créée (titre, icône, message, types de boutons et actiosn par défaut)
        
        self._message_box_pour_sauvegarde_donnees.setWindowTitle("Sauvegarde des données ?")
        self._message_box_pour_sauvegarde_donnees.setIcon(QtGui.QMessageBox.Question)
        self._message_box_pour_sauvegarde_donnees.setText("Voulez-vous sauvegarder les données avant de quitter l'application ?")
        self._message_box_pour_sauvegarde_donnees.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        self._message_box_pour_sauvegarde_donnees.setDefaultButton(QtGui.QMessageBox.Yes)
        self._message_box_pour_sauvegarde_donnees.setEscapeButton(QtGui.QMessageBox.No)
        
        # On lance la fenêtre et on récupère le résultat du clic sur l'un des boutons via l'attribut "_choix_sauvegarde_donnees"
        
        self._choix_sauvegarde_donnees = self._message_box_pour_sauvegarde_donnees.exec_()
        
        # Traitement du choix de l'utilisateur
        # --- Si L'utilisateur a souhaité sauvegarder les données : on fait appel à la méthode "actions_avant_de_quitter_l_application"
        # --- Sinon on ne fait rien et l'application se ferme
        
        if self._choix_sauvegarde_donnees == QtGui.QMessageBox.Yes:
        # L'utilisateur a souhaité sauvegardé les données
            
            self.actions_avant_de_quitter_l_application()
            
    
    def quitter_l_application(self):
        """
            Méthode qui permet de quitter l'application
        """
        
        QtGui.qApp.quit()
        
    
    def aller_sur_le_site_de_la_banque(self):
        """
            Méthode qui permet d'aller sur le site de la banque dont l'URL est précisée en attribut de la classe
        """
        
        webbrowser.open(self._contenu_du_fichier_de_configuration["url_banque"])
        
    
    def ajouter_entree_TV_Balance(self, option = False):
        """
            Méthode qui permet d'ajouter une entrée dans le TV Balance
        """
        
        # Si l'option est à False c'est que l'utilisateur a renseigné toutes les entrées dans la GUI
        
        if not option:
            # Récupération des données dans la GUI
            
            self._TVB_date = self.CW_Choix_de_la_date.selectedDate().toString("dd/MM/yyyy")
            self._TVB_libelle = self.LE_Libelle.text()
            self._TVB_montant = np.float64(self.LE_Montant.text()) / 2.0
            self._TVB_payeur = self.CB_payeur.currentText()
            
        else:
            # Sinon c'est que l'utilisateur souhaite ajouter une nouvelle entrée via la calculatrice pour les trajets
            # Dans ce cas certaines valeurs seront renseignées par défaut
            
            self._TVB_date = datetime.now().strftime("%d/%m/%Y")
            self._TVB_libelle = "A/R x-x"
            self._TVB_montant = np.float64(self._total_calculatrice)
            self._TVB_payeur = "lui"
            
        
        # Selon la valeur du ComboBox on définit la valeur du montant à ajouter
        
        if self._TVB_payeur in ["lui"]:
            
            self._montant_pour_ajout_balance = self._TVB_montant
            
        elif self._TVB_payeur in ["elle"]:
            
            self._montant_pour_ajout_balance = -1 * self._TVB_montant
            
        # Dictionnaire contenant les données qui seront ajoutées
        
        self._dico_donnees_a_ajouter = {
                                        "Date": str(self._TVB_date),
                                        "Libellé": str(self._TVB_libelle),
                                        "Montant lui": self._montant_pour_ajout_balance,
                                        "Montant elle": (-1 * self._montant_pour_ajout_balance),
                                        "statut_export": False
                                       }
        
        # Concaténation des données à ajouter avec les données existantes
        
        self._donnees_a_concatener = []
        self._donnees_a_concatener.insert(0, self._dico_donnees_a_ajouter)
        
        self._donnees_balance = pd.concat([pd.DataFrame(self._donnees_a_concatener), self._donnees_balance], ignore_index=True)
        
        # Mise-à-jour du modèle avec les données concaténées
        
        self._modele_balance.set_donnees(self._donnees_balance)
        self._modele_balance.layoutChanged.emit()                   # prendre des infos sur cette ligne pour expliquer le fonctionnement
        
        # Mise-à-jour des données dans l'instance de chargement des données de la balance
        
        self._instance_de_chargement_balance.set_donnees(self._donnees_balance)
        
        # Mise-à-jour des totaux de la balance
        
        self.remplissage_des_totaux_balance()
        
    
    @QtCore.pyqtSlot(str)
    def recuperation_du_total(self, texte):
        """
            Méthode qui permet de récupérer le total calculé via la calculatrice pour les trajets
        """
        
        self._total_calculatrice = float(texte) / 2.0
        self.ajouter_entree_TV_Balance(option=True)
        
    
    def lancement_calculatrice(self):
        """
            Méthode qui permet d'afficher la calculatrice pour les trajets
        """
        
        # Création de l'instance de la classe CalculatricePourLesDeplacements
        self._calculatrice_pour_les_trajets = CalculatricePourLesDeplacements()
        
        # Connexion de l'attribut total_a_envoyer de l'instance de la classe CalculatricePourLesDeplacements à la méthode recuperation_du_total
        self._calculatrice_pour_les_trajets.total_a_envoyer.connect(self.recuperation_du_total)
        
        # Lancement de la fenêtre
        self._calculatrice_pour_les_trajets.main()
        
    
    @QtCore.pyqtSlot(bool)
    def recuperation_option_enregistrement_copies(self, value):
        """
            Méthode qui permet de récupérer l'état de la CB associée à l'option d'enregistrement de copies
        """
        
        self._option_enregistrement_copie_fichiers = value
        
    
    @QtCore.pyqtSlot(bool)
    def recuperation_option_envoi_copies_fichiers_par_mail(self, value):
        """
            Méthode qui permet de récupérer l'état de la CB associée à l'option d'envoi de copies par mail
        """
        
        self._option_enregistrement_envoi_fichiers = value
        
    
    def lancement_options_d_enregistrement(self):
        """
            Méthode qui permet d'afficher la fenêtre qui permet de modifier les options d'enregistrements
        """
        
        # Création de l'instance de la classe CalculatricePourLesDeplacements
        self._modification_des_options_d_enregistrement = OptionsPourLEnregistrement()
        
        # Connexion de l'attribut option_enregistrement_copies de l'instance de la classe OptionsPourLEnregistrement à la méthode recuperation_option_enregistrement_copies
        self._modification_des_options_d_enregistrement.option_enregistrement_copies.connect(self.recuperation_option_enregistrement_copies)
        
        # Connexion de l'attribut option_envoi_copies_fichiers_par_mail de l'instance de la classe OptionsPourLEnregistrement à la méthode z
        self._modification_des_options_d_enregistrement.option_envoi_copies_fichiers_par_mail.connect(self.recuperation_option_envoi_copies_fichiers_par_mail)
        
        # Lancement de la fenêtre
        self._modification_des_options_d_enregistrement.main()
        
    
    @staticmethod
    def ecriture_des_donnees_a_exporter(liste_des_donnees_a_exporter, provenance):
        """
            Méthode qui permet d'écrire le fichier JSON qui contient les données exportées
        """
        
        if liste_des_donnees_a_exporter:
            
            dico_a_exporter = {}
            
            dico_a_exporter["provenance"] = provenance
            dico_a_exporter["date_de_creation"] = datetime.now().strftime("%d/%m/%Y")
            dico_a_exporter["donnees"] = liste_des_donnees_a_exporter
            
            nom_du_fichier_d_export = "export_{}_{}.json".format(provenance, datetime.now().strftime("%d_%m_%Y__%H_%M_%S"))
            emplacement_du_dossier_d_export = os.path.abspath("../../Exports")
            fichier_d_export = os.path.join(emplacement_du_dossier_d_export, nom_du_fichier_d_export)
            
            with open(fichier_d_export, 'w') as fichier_a_exporter:
            
                json.dump(dico_a_exporter, fichier_a_exporter, indent=4)
                
    
    @staticmethod
    def analyse_moyen_de_paiement(element_a_analyser):
        """
            Méthode statique qui permet d'analyser le libéllé à exporter pour retourner la chaîne de caractère adéquate selon les cas
        """
        
        if "ACHAT CB" in element_a_analyser:
            
            return "CB"
            
        elif "PRELEVEMENT DE" in element_a_analyser or "VIREMENT DE" in element_a_analyser:
            
            return "virement bancaire"
            
        elif "CHEQUE N" in element_a_analyser:
            
            # numero_du_cheque = element_a_analyser.split()[-1].strip()
            # chaine_a_retourner = "chèque %s" % numero_du_cheque
            # return chaine_a_retourner
            
            return "chèque"
            
        else:
            
            return "CB"
            
    
    def exportation_des_lignes(self, provenance, cellules_selectionnees, donnees):
        """
            Méthode qui permet d'extraire, parmi les données, les lignes à exporter sélectionnées par l'utilisateur
        """
        
        # On itère sur la liste des cellules sélectionnées et on modifie le statut de la ligne associée
        liste_des_donnees_a_exporter = []
        lignes_ajoutees = []
        
        for indice, cellule in enumerate(cellules_selectionnees):
            
            ligne_selectionnee = cellule.row()
            
            if ligne_selectionnee not in lignes_ajoutees:
            # si la ligne associée à la cellule actuelle ne figure pas dans la liste des lignes dont le statut a déjà été modifié
                
                statut_donnees_exportee = donnees["statut_export"][ligne_selectionnee]
                
                # vérifier que la donnée associée possède le statut d'export à True/False
                if not statut_donnees_exportee:
                    
                    if provenance in ["Comptes"]:
                        
                        valeur_du_moyen_de_paiement = self.analyse_moyen_de_paiement(donnees["Libellé"][ligne_selectionnee])
                        
                    elif provenance in ["Balance"]:
                        
                        valeur_du_moyen_de_paiement = "elle"

                    dico_de_la_donnee_a_exporter = { "date": donnees[u"Date"][ligne_selectionnee],
                                                     "titre": donnees[u"Libellé"][ligne_selectionnee],
                                                     "montant": donnees[u"Montant lui"][ligne_selectionnee],
                                                     "moyen_de_paiement": valeur_du_moyen_de_paiement,
                                                     "statut": True
                                                   }
                    
                    liste_des_donnees_a_exporter.append(dico_de_la_donnee_a_exporter)
                    
                    donnees["statut_export"][ligne_selectionnee] = True
                    
                    lignes_ajoutees.append(ligne_selectionnee)
                    
        self.ecriture_des_donnees_a_exporter(liste_des_donnees_a_exporter, provenance)
        
    
    def traitement_des_lignes_selectionnees(self):
        """
            Méthode qui permet de traiter les lignes sélectionnées
        """
        
        index_de_l_onglet_affiche = self.TW_Donnees.currentIndex()
        nom_de_l_onglet_affiche = self.TW_Donnees.tabText(index_de_l_onglet_affiche)
        
        if nom_de_l_onglet_affiche in ["Comptes"]:
            
            cellules_selectionnees = self.TV_Comptes.selectedIndexes()
            donnees = self._donnees_comptes
            self.exportation_des_lignes("Comptes", cellules_selectionnees, donnees)
            self.TV_Comptes.clearSelection()
            
        elif nom_de_l_onglet_affiche in ["Balance"]:
            
            cellules_selectionnees = self.TV_Balance.selectedIndexes()
            donnees = self._donnees_balance
            self.exportation_des_lignes("Balance", cellules_selectionnees, donnees)
            self.TV_Balance.clearSelection()
            
    
    def impressions(self):
        """
            Méthode qui permet de traiter les impressions
        """
        
        pass
        
    
    def parametrage_et_affectation_des_QValidator(self):
        """
            Méthode qui permet de définir, paramétrer et affecter les QValidator
        """
        
        self._QDouble_validator = SousClassementDesQValidators.SCQDoubleValidation(-1000.0, 1000.0)
        self._QDouble_validator.setDecimals(2)
        self.LE_Montant.setValidator(self._QDouble_validator)
        
    
    def menu_contextuel(self):
        """
            Méthode qui permet de définir et de lancer le menu contextuel associé au TableWidget Donnees
            afin de lancer la calculatrice pour les comptes
        """
        
        ### Création d'une instance de menu QMenu
        
        self._menu_contextuel = QtGui.QMenu()
        
        
        ### Création de l'action liée à la calculatrice pour les trajets, action qui va être liée au menu contextuel
        
        # Création de l'action intitulée "Calculatrice pour les trajets"
        self._actionCalculatricePourLesTrajets = QtGui.QAction("Calculatrice pour les trajets", self)
        
        # Assignation du raccourci clavier "Ctrl+T" à cette action
        self._actionCalculatricePourLesTrajets.setShortcut(QtGui.QKeySequence("Ctrl+T"))
        
        # Connection de l'action à la méthode "lancement_calculatrice"
        self._actionCalculatricePourLesTrajets.triggered.connect(self.lancement_calculatrice)
        
        # Ajout de l'action à un widget : ici c'est l'application elle-même
        # --- en effet, chaque action doit être ajoutée à un widget avant de pouvoir être utilisée
        # -- dans le cas présent, i.e. l'utilisation d'un raccourci clavier, c'est nécessaire
        self.addAction(self._actionCalculatricePourLesTrajets)
        
        # Ajout de l'action dans le menu contextuel
        self._menu_contextuel.addAction(self._actionCalculatricePourLesTrajets)
        
        
        ### Création de l'action liée à la calculatrice pour les trajets, action qui va être liée au menu contextuel
        
        # Création de l'action intitulée "modification_des_options_d_enregistrement"
        self._actionModificationDesOptionsDEnregistrement = QtGui.QAction("Options d'enregistrement", self)
        
        # Assignation du raccourci clavier "Ctrl+O" à cette action
        self._actionModificationDesOptionsDEnregistrement.setShortcut(QtGui.QKeySequence("Ctrl+O"))
        
        # Connection de l'action à la méthode "lancement_options_d_enregistrement"
        self._actionModificationDesOptionsDEnregistrement.triggered.connect(self.lancement_options_d_enregistrement)
        
        # Ajout de l'action à un widget : ici c'est l'application elle-même
        self.addAction(self._actionModificationDesOptionsDEnregistrement)
        
        # Ajout de l'action dans le menu contextuel
        self._menu_contextuel.addAction(self._actionModificationDesOptionsDEnregistrement)
        
        
        ### Lancement du menu contextuel
        
        # Lancement du menu contextuel
        # --- l'option QtGui.QCursor.pos() permet d'ouvrir le menu contextuel à l'emplacement du pointeur
        self._menu_contextuel.exec_(QtGui.QCursor.pos())     
        
    
    def connections_des_widgets(self):
        """
            Méthode qui permet de connecter les widgets
        """
        
        ### Connexion des boutons
        
        self.B_Import_CSV.clicked.connect(self.importer_un_fichier_CSV)
        self.B_Traiter_lignes.clicked.connect(self.traitement_des_lignes_selectionnees)
        self.B_Impression.clicked.connect(self.impressions)
        self.B_Internet.clicked.connect(self.aller_sur_le_site_de_la_banque)
        self.B_Ajouter_dans_balance.clicked.connect(self.ajouter_entree_TV_Balance)
        self.B_Quitter.clicked.connect(self.quitter_l_application)
        
        
        ### Désactivation de certains boutons
        
        self.B_Traiter_lignes.setEnabled(True)
        self.B_Impression.setEnabled(False)
        self.B_Internet.setEnabled(True)
        
        
        ### Connexion de l'icône de fermeture (la croix blanche sur fond rouge en haut à droite de la fenêtre)
        ### Pour rappel self._app est le nom de l'instance QtGui.QApplication passé en argument à la classe (voir le module lancement.py)
        
        self._app.aboutToQuit.connect(self.sauvegarde_des_donnees)                    
        
        
        ### Connexion du menu contextuel qui permet de lancer l'action associée à la calculatrice pour les trajets
        
        # Permet de spécifier que le menu contextuel sera un menu personnalisé
        self.TW_Donnees.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        
        # Permet de lier l'action du clic droit à l'appel du menu contextuel qui sera défini via la méthode "menu_contextuel"
        self.TW_Donnees.customContextMenuRequested.connect(self.menu_contextuel)
        
    
    def main(self):
        """
            Main de la classe
        """
        
        self.show()
        

### Utilisation

if __name__ == "__main__":
    
    print("Ce module n'est pas voué a être exécuté seul")
