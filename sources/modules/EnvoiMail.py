# coding: utf-8

""" Module qui contient la classe EnvoiMail pour l'application des comptes """


### Paramètres globaux

__author__ = "Julien LEPAIN"
__version__ = 1.0
__all__ = ["EnvoiMail"]
__documentation__ = ["https://broux.developpez.com/articles/protocoles/smtp/"]


### Import des librairies

# Import des librairies graphiques
from PyQt4 import QtGui, QtCore
import sys
import MDP

# Import des autres librairies
import smtplib                                  # SMTP pour Simple Mail Transfer Protocol
from email.mime.multipart import MIMEMultipart   # creuser ce que fait exactement cette librairie
from email.mime.text import MIMEText             # creuser ce que fait exactement cette librairie
from email.mime.base import MIMEBase             # creuser ce que fait exactement cette librairie
from email import encoders
import os
from datetime import datetime


### Définitions des classes

# class RecuperationMDP(QtGui.QDialog, MDP.Ui_Dialog):
class RecuperationMDP(QtGui.QDialog, MDP.Ui_Dialog):
    """
        Classe qui permet de récupérer le mot de passe pour la connexion à la boîte mail
    """
    
    # Signal lié au QLineEdit
    mot_de_passe = QtCore.pyqtSignal(str)
    
    def __init__(self, parent=None):
        """
            Constructeur de la classe
        """
        
        super(RecuperationMDP, self).__init__(parent)
        self.setupUi(self)
        
        ### Positionnement de la fenêtre sur l'écran
        
        self.positionnement_de_la_fenetre_sur_l_ecran()
        
        ### Connexion des es widgets
        
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
        
        # Place la fenêtre au milieu de l'écran
        self.move((taille_ecran.width() - taille_fenetre.width()) / 2, (taille_ecran.height() - taille_fenetre.height()) / 2)
        
    
    def recuperation_du_mot_de_passe(self):
        """
            Méthode qui permet de récupérer le texte du QLineEdit "LE_MDP"
        """
        
        if self.LE_MDP.text() != "":
            
            self.mot_de_passe.emit(self.LE_MDP.text())
            self.accept()
            
    
    def connections_des_widgets(self):
        """
            Méthode qui permet de connecter les widgets
        """
        
        # Permet de mettre des ronds à la place des caractères pour masquer le mot de passe
        self.LE_MDP.setEchoMode(QtGui.QLineEdit.Password)
        
        # Connexion, lors de l'appui sur la touche "Entrée", du QLineEdit à la méthode "recuperation_du_mot_de_passe"
        self.LE_MDP.returnPressed.connect(self.recuperation_du_mot_de_passe)
        

class EnvoiMail(object):
    """
        Classe qui permet de gérer l'envoi d'un mail contenant, en pièce jointe, une copie des fichiers contenant les données pour les comptes et la balance entre nous
    """
    
    def __init__(self, expediteur, destinataire, liste_des_fichiers_a_envoyer):
        """
            Constructeur de la classe
        """
        
        self._expediteur = expediteur
        self._destinataire = destinataire
        self._liste_des_fichiers_a_envoyer = liste_des_fichiers_a_envoyer
        
        self._objet_du_mail = "MAJ des comptes - {}".format(datetime.now().strftime("%d/%m/%Y"))
        self._message_du_mail = ("Ce mail contient deux pièces jointes :\n\n"
                                 "- le fichier contenant les données des comptes ;\n"
                                 "- le fichier contenant les données pour la balance entre nous.\n"
                                 "\nCe mail a été généré automatiquement par l'application des comptes lors de sa fermeture.")
        
        # Objet, sous forme de dictionnaire, qui va contenir des informations comme l'expéditeur, le destinataire, l'objet du mail, etc...
        # creuser ce que fait exactement cette fonction
        self._msg = MIMEMultipart()
        
        self._message = ""
        
        self._recup_MDP = None
        self._verification_MDP = False
        
        self._mot_de_passe = ""
        
        # Si le serveur est celui de Gmail il est nécessaire, au préalable, de paramétrer la boîte mail afin d'autoriser les applications moins sécurisées
        self._serveur_d_envoi = "smtp.gmail.com"
        self._port = 587
        
        # Initialisation
        self.configurer_les_elements_du_mail()
        
    
    ### Accesseurs et mutateurs
    
    # Nothing
    
    
    ### Méthodes
    
    def configurer_les_elements_du_mail(self):
        """
            Méthode qui permet de configurer les différents éléments du mail :
            
            - expéditeur ;
            - destinataire ;
            - objet du mail ;
            - message.

        """
        
        # Expéditeur(s)
        self._msg["From"] = self._expediteur
        
        # Destinataire(s)
        self._msg["To"] = self._destinataire
        
        # Objet du mail
        self._msg["Subject"] = self._objet_du_mail
        
        # Message
        self._message = self._message_du_mail
        
        # creuser ce que fait exactement cette fonction
        # la seconde option, subtype, a pour valeur "plain" qui est celle par défaut
        # la troisième option, charset, a pour valeur "utf-8" afin d'éviter les problèmes d'encoding vis-à-vis des chaînes de caractères codées en unicode
        self._msg.attach(MIMEText(self._message, "plain", "utf-8"))
        
        # Partie du gère l'envoi de pièce jointe
        for fichier in self._liste_des_fichiers_a_envoyer:
            
            part = MIMEBase("application", "octet-stream")
            part.set_payload(open(fichier, 'rb').read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment; filename= %s" % os.path.basename(fichier))
            
        # creuser ce que fait exactemetn cette fonction
        self._msg.attach(part)
        
    
    @QtCore.pyqtSlot(str)
    def recuperation_du_MDP(self, texte):
        """
            Méthode qui permet de récupérer le mot de passe et de l'affecter à l'attribut _mot_de_passe
        """
        
        self._mot_de_passe = texte
        
    
    def affichage_de_la_fenetre_du_MDP(self):
        """
            Méthode qui permet d'ouvrir une fenêtre afin que l'utilisateur puisse entrer le mot de passe pour se connecter à la boîte mail
            Cette méthode va lancer l'IHM de récupération du MDP
        """
        
        self._instance_de_recuperation_du_MDP = RecuperationMDP()
        self._instance_de_recuperation_du_MDP.mot_de_passe.connect(self.recuperation_du_MDP)
        self._statut_fenetre_MDP = self._instance_de_recuperation_du_MDP.exec_()                # affiche la fenêtre MDP en continue tant que l'utilisateur n'a pas rentré de mot de passe (et bloque aussi l'accès à la fenêtre principale)
        
    
    def envoi_du_mail(self):
        """
            Méthode qui permet d'envoyer un mail
        """
        
        # Connection au serveur via le nom de serveur et le port
        mailserver = smtplib.SMTP(self._serveur_d_envoi, self._port)    
        
        # Commande pour tester l'établissement de la connexion
        mailserver.ehlo()
        
        # Fonction de sécurité requise par Google pour se connecter à Gmail, permet notamment de protéger l'envoi du mot de passe
        # # # # à creuser un peu plus, notamment l'aspect sécuritaire
        mailserver.starttls()
        
        # Commande pour tester l'établissement de la connexion
        mailserver.ehlo()
        
        # On itère tant que la vérification du mot de passe n'est pas à True
        while not self._verification_MDP:
            
            # Récupération du mot de passe auprès de l'utilisateur
            self.affichage_de_la_fenetre_du_MDP()
            
            # Si le statut de la fenêtre est à 0 c'est que l'utilisateur a cliqué sur la croix
            if self._statut_fenetre_MDP == 0:
                
                self._verification_MDP = True
                
            # Sinon c'est qu'il a indiqué un mot de passe
            elif self._statut_fenetre_MDP == 1:
                
                try:
                # On essaie de se connecter à la boîte mail avec le mot de passe fournit par l'utilisateur
                    
                    # Commande qui permet de se connecter à la boîte mail
                    mailserver.login(self._expediteur, self._mot_de_passe)
                    
                except smtplib.SMTPAuthenticationError:
                # Le mot de passe est incorrect
                    
                    print("Mot de passe incorrect")
                    
                else:
                # Le mot de passe est correct : on sort de la boucle
                    
                    self._verification_MDP = True
                    
                    # Commande d'envoi du mail
                    mailserver.sendmail(self._expediteur, self._destinataire, self._msg.as_string())
                    
        # Commande pour quitter la connexion
        mailserver.quit()
        

### Utilisation

if __name__ == "__main__":
    
    print("Ce module n'a pas vocation à être exécuté seul.")
