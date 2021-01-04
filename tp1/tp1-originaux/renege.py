
import json
import sys
from crud import CRUD
from email_analyzer import EmailAnalyzer


class RENEGE:

    """Class pour realiser le filtrage du spam en utilisant vocabular.json file et
    CRUD et EmalAnalyze classes"""

    def __init__(self):
        self.email_file = "1000-mails.json"
        self.crud = CRUD()
        self.e_mail = EmailAnalyzer()

    def classify_emails(self):
        '''
        fonction deja implemente
        Description: fonction pour commencer l'analyse des e-mails.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        try:
            self.process_email(self.get_email())
            return True
        except Exception as e:
            print("Error!", e.__class__, "occurred.")
            return False


    def process_email(self, new_emails):
        '''
        Description: fonction pour analyser chaque nouvel e-mail dans le 
        dictionare. Elle gere l'ajout des nouveux utilisateurs et/ou modification
        de l'information existante sur les utilisateurs et groupes. 
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''

        raise NotImplementedError("")

    def update_user_info(self, new_user_email, new_user_date, new_email_spam):
        '''
        Description: fonction pour modifier l'information de utilisateur (date de dernier message arrive,
        numero de spam/ham, trust level, etc).
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''

        return NotImplementedError("")

    def update_group_info(self, user_group_list):
        '''
        Description: fonction pour modifier l'information de groupe dans lequel 
        l'utilisater est present (trust level, etc).
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        return NotImplementedError("")

    def get_user_email_list(self):
        '''
        Description: fonction pour creer le liste des e-mails (noms) 
        des utilisateurs uniques.
        Sortie: liste des uniques e-mails des utilisateurs
        '''
        raise NotImplementedError("")

    def get_email(self):
        '''
        Description: fonction pour lire le ficher json avec les mails et extraire les 
        donees necessaire.
        Sortie: dictionare de e-mails formate selon le JSON.
        '''
        raise NotImplementedError("")
