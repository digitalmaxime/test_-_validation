
import json
import sys
from crud import CRUD
from email_analyzer import EmailAnalyzer

#populer users.json et groups.json
class RENEGE:

    """Class pour realiser le filtrage du spam en utilisant vocabular.json file et
    CRUD et EmalAnalyze classes"""

    def __init__(self, file):
        self.email_file = file
        self.crud = CRUD()
        self.email_analyzer = EmailAnalyzer()


    def classify_emails(self, calcul_mode, cleaning_mode): #pragma: no cover
        '''
        fonction deja implemente
        Description: fonction pour commencer l'analyse des e-mails.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        self.crud.clean_files()
        group_dic = self.crud.read_users_file()
        assert len(group_dic) == 0, "Error le dic de group n est pas vide!!"
        users_dic = self.crud.read_groups_file()
        assert len(users_dic) == 0, "Error le dic de users n est pas vide!!"
        try:
            self.process_email(self.get_email(), calcul_mode, cleaning_mode)
            return True
        except Exception as e:
            print("Error!", e.__class__, "occurred in renege at line 32.")
            return False


    def process_email(self, new_emails, calcul_mode, cleaning_mode):     #pragma: no cover
        # clacul_mode:
        # 0: probabilite Bayes
        # 1: formule 1
        # 2: formule 2
        '''
        Description: fonction pour analyser chaque nouvel e-mail dans le 
        dictionare. Elle gere l'ajout des nouveux utilisateurs et/ou modification
        de l'information existante sur les utilisateurs et groupes. 
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        #ajout des groupes + calcul du trust 
        for email in new_emails:
            user_email = email["mail"]["From"]
            user_date = email["mail"]["Date"]
            Spam = None
            # Trouver la proba de spam (Bayes), qui equivaut  à 'P' dans les formules (1) (2)
            Spam = self.email_analyzer.is_spam(email["mail"]["Subject"], email["mail"]["Body"], 1, 1, 0)
            
            if calcul_mode > 0 :
                # Appel à is_spam1-2 ici 
                Spam = self.call_is_spam_alternate(Spam, user_email, calcul_mode)

                user_id = self.crud.get_user_id(user_email)
                if user_id == None :
                    self.crud.add_new_user(user_email, user_date)
                else :
                    nb_spam = self.crud.get_user_data( user_id, "Spamn")
                    nb_ham = self.crud.get_user_data( user_id, "HamN")

                #verifier qu'il y a pas 0spam et 0ham pour eviter division par 0
                    assert (nb_spam + nb_ham) != 0, "Attention division par zero renege line 77"
                
                #mettre trust level par defaut
                    new_trust_level = nb_ham / (nb_ham + nb_spam)
                    self.crud.update_users(user_id, "Trust", new_trust_level)                
                    self.update_group_info(["default"])

            # pour calcul_mode 0-1-2
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
        
        #ajout des groupes + calcul du trust 
        self.crud.add_new_group("friends", 50, friend_list)
        self.crud.add_new_group("junk", 50, junk_list)

        #liste de groupes
        complete_group_list = ["default", "friends", "junk"]
        
        self.update_group_info(complete_group_list)

        
        return True


    def call_is_spam_alternate(self,P, user, calcul_mode):
        assert calcul_mode == 1 or calcul_mode == 2, "le parametre calcul_mode doit etre 1 ou 2"
        
        user_id = self.crud.get_user_id(user)
        if user_id == None :
            user_trust = 100
            # Valeurs par defaut pour 1er occurence des users
            H = True
            T1 = False
            T2 = False
            T3 = True
            if calcul_mode == 1:
                S = self.email_analyzer.is_spam1(P, H, T1, T2, T3)
            if calcul_mode == 2:
                S = self.email_analyzer.is_spam2(P, T2, T3)
            return S
                
        user_trust = self.crud.get_user_data(user_id, "Trust")
        Date_of_first_seen_message = self.crud.get_user_data(user_id, "Date_of_first_seen_message")
        Date_of_last_seen_message = self.crud.get_user_data(user_id, "Date_of_last_seen_message")
        
        if Date_of_last_seen_message - Date_of_first_seen_message <2592000 :
            H = True
        else :
            H = False

        if user_trust < 60:
            T1 = True
        else:
            T1 = False
        
        if user_trust > 75:
            T3 = True
        else:
            T3 = False
        
        group_trust_total = 0
        group_list = self.crud.get_user_data(user_id, "Groups")
        
        if len(group_list) == 0:
            group_trust_total = 80      #valeur arbitraire

        else:
            for group_name in group_list:
                group_id = self.crud.get_group_id(group_name)
                #calculer moyenne des trusts de la group list
                group_trust = self.crud.get_group_data(group_id,"Trust")
                group_trust_total += group_trust
            group_trust_total /= len(group_list)
        
        if group_trust_total < 70:
            T2 = True
        else :
            T2 = False
        
        if calcul_mode == 1:
            S = self.email_analyzer.is_spam1(P, H, T1, T2, T3)

        if calcul_mode == 2:
            S = self.email_analyzer.is_spam2(P, T2, T3)
        return S



    def update_user_info(self, new_user_email, new_user_date, new_email_spam): #pragma: no cover
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


    def update_group_info(self, user_group_list): #pragma: no cover
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
            if len(user_list) != 0:
                group_trust = 0
                for user_name in user_list:
                    user_id = self.crud.get_user_id(user_name)
                    user_trust = self.crud.get_user_data(user_id, "Trust")
                    group_trust += user_trust
                group_trust /= len(user_list)
                #mettre a jour le groups.json
                self.crud.update_groups(group_id, "Trust", group_trust)

        return True


    def get_user_email_list(self): #pragma: no cover
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



    def get_email(self): #pragma: no cover
        '''
        Description: fonction pour lire le ficher json avec les mails et extraire les 
        donees necessaire.
        Sortie: dictionare de e-mails formate selon le JSON.
        '''
        with open (self.email_file, "r") as file:
            data = json.load(file)
        return data["dataset"]

    def calculate_trust_user(self, index): #pragma: no cover
        index = "{}".format(index)
        Date_of_last_seen_message = crud.get_user_data(index,"Date_of_last_seen_message")
        Date_of_first_seen_message = crud.get_user_data(index,"Date_of_first_seen_message")
        HamN = crud.get_user_data(index,"HamN")
        SpamN = crud.get_user_data(index,"Spamn")

        Trust1 = Date_of_last_seen_message/Date_of_first_seen_message * HamN/(HamN + SpamN)

        List_of_groups = Date_of_last_seen_message = crud.get_user_data(index,"Groups")
        Counter_of_groups = 0
        Total_trust = 0

        for e in List_of_groups:
            Counter_of_groups += 1
            group_id = crud.get_group_id(e)
            Total_trust += crud.get_group_data(group_id, "Trust")

        Trust2 = Total_trust / Counter_of_groups

        Trust = (Trust1 + Trust2)/2

        if Trust2 < 50:
            Trust = Trust2

        if Trust1 > 100:
            Trust = 100

        assert (Trust>=0 and Trust<=100),"error message"
        return Trust 