
import json
import sys
from crud import CRUD
from email_analyzer import EmailAnalyzer

#populer users.json et groups.json
#fait appel a email analyser

class RENEGE:

    """Class pour realiser le filtrage du spam en utilisant vocabular.json file et
    CRUD et EmalAnalyze classes"""

    def __init__(self):
        self.email_file = "800-mails.json" #auparavant 1000
        self.crud = CRUD()
        self.e_mail = EmailAnalyzer()


    def classify_emails(self):
        '''
        fonction deja implemente
        Description: fonction pour commencer l'analyse des e-mails.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        self.crud.clean_files()
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
        for email in new_emails:
            user_email = email["mail"]["From"]
            user_date = email["mail"]["Date"]
            Spam = email["mail"]["Spam"]
            if Spam == "true":
                Spam = True
            else:
                Spam = False
            self.update_user_info(user_email, user_date, Spam)

        # Definir liste amis et junk pour ensuite les passer en parametre a 'add_new_group'
        friend_list = []
        junk_list = []


        #CALCUL du trust pour chaque user
        for user in self.get_user_email_list():
            user_id = self.crud.get_user_id(user)
            nb_spam = self.crud.get_user_data( user_id, "Spamn")
            nb_ham = self.crud.get_user_data( user_id, "HamN")
            #verifier qu'il y a pas 0spam et 0ham pour eviter division par 0
            if (nb_spam + nb_ham) == 0:
                return False
            new_trust_level = nb_ham / (nb_ham + nb_spam)
            self.crud.update_users(user_id, "Trust", new_trust_level)
            
            #populer les listes amis et junk
            if new_trust_level > 0.7:
                friend_list.append(user)
            else:
                junk_list.append(user)
        
        #ajout des groupes
        self.crud.add_new_group("friends", 50, friend_list)
        self.crud.add_new_group("junk", 50, junk_list)

        #liste de groupes
        complete_group_list = ["default", "friends", "junk"]

        self.update_group_info(complete_group_list)

        return True


    def update_user_info(self, new_user_email, new_user_date, new_email_spam):
        '''
        Description: fonction pour modifier l'information de utilisateur (date de dernier message arrive,
        nb de spam/ham, trust level, etc).
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        user_id = self.crud.get_user_id(new_user_email)

        #si l'utilisateur n'existe pas il est ajoute
        if user_id == None:
            self.crud.add_new_user(new_user_email, new_user_date)
            return True
        
        self.crud.update_users(user_id,"Date_of_last_seen_message",new_user_date)

        if new_email_spam :
            nbSpam = self.crud.get_user_data(user_id,"Spamn") + 1
            self.crud.update_users(user_id,"Spamn", nbSpam)
        
        else :
            nbHam = self.crud.get_user_data(user_id,"HamN") + 1
            self.crud.update_users(user_id,"HamN", nbHam)

        return True


    def update_group_info(self, user_group_list):
        '''
        user_group_list: liste des groupes

        Description: fonction pour modifier l'information de groupe dans lequel 
        l'utilisater est present (trust level, etc).
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        #par chaque user verifie 
        for group_name in user_group_list:
            group_id = self.crud.get_group_id(group_name)
            user_list = self.crud.get_group_data(group_id, "List_of_members")
            #calculer moyenne des trusts de la user list
            group_trust = 0
            for user_name in user_list:
                user_id = self.crud.get_user_id(user_name)
                user_trust = self.crud.get_user_data(user_id, "Trust")
                group_trust += user_trust
            group_trust /= len(user_list)
            self.crud.update_groups(group_id, "Trust", group_trust)

        return True

    def get_user_email_list(self):
        '''
        Description: fonction pour creer le liste des e-mails (noms) 
        des utilisateurs uniques.
        Sortie: liste des uniques e-mails des utilisateurs
        '''
        emails = self.get_email()
        users_list = []
        for email in emails:
            if email["mail"]["From"] not in users_list:
                users_list.append(email["mail"]["From"])
        return users_list



    def get_email(self):
        '''
        Description: fonction pour lire le ficher json avec les mails et extraire les 
        donees necessaire.
        Sortie: dictionare de e-mails formate selon le JSON.
        '''
        with open (self.email_file, "r") as file:
            data = json.load(file)
        return data["dataset"]
