import json
from text_cleaner import TextCleaning
import math

#calcul des proba totales

class EmailAnalyzer:
    """Classe pour classifier les e-mails comme spam ou non spam (ham)"""

    def __init__(self):
        self.vocab = "vocabulary.json"
        self.cleaning = TextCleaning()
        self.p_ham = None
        self.p_spam = None
        self.email_file_classify = "800-mails.json" #ajout pour calculer P(spam) et P(ham)
        self.set_pham_pspam(self.calcul_pHam_pSpam(self.email_file_classify))


    def set_pham_pspam(self, values_tuple) :
        self.p_spam = values_tuple[0]
        self.p_ham = values_tuple[1]


    def calcul_pHam_pSpam(self,emailFile):
        data = self.load_dict(emailFile)
        spam_counter = 0
        email_counter = 0

        for email in data["dataset"] :
            if email["mail"]["Spam"] == "true":
                spam_counter += 1
            email_counter += 1 

        p_spam_result = spam_counter / email_counter
        p_ham_result = 1 - p_spam_result
        return (p_spam_result, p_ham_result)
    
    
    # parametre use_log prend soit 0 ou 1 , param combinaison_log prend 0 ou 1 
    def is_spam(self, subject_orig, body_orig, use_log, combinaison_log, cleaning_mode):
        '''
        Description: fonction pour verifier si e-mail est spam ou ham,
        en calculant les probabilites d'etre spam et ham, 
        donnee le sujet et le texte d'email. 
        Sortie: 'True' - si l'email est spam, 'False' - si email est ham.
        '''
        subject_orig = self.cleaning.clean_text(subject_orig, cleaning_mode)
        body_orig = self.cleaning.clean_text(body_orig, cleaning_mode)


        #calcul avec log
        if use_log == 1:
            if combinaison_log : 
                prob_body = self.spam_ham_body_prob_log(body_orig)
                prob_sub = self.subject_spam_ham_prob_log(subject_orig) 

            else : 
                prob_spam_body = self.spam_ham_body_prob_log(body_orig)[0]
                prob_ham_body = self.spam_ham_body_prob_log(body_orig)[1]
                prob_spam_sub = self.subject_spam_ham_prob_log(subject_orig)[0]
                prob_ham_sub = self.subject_spam_ham_prob_log(subject_orig)[1]
                if prob_spam_body > 700 :
                    prob_spam_body = 700
                if prob_ham_body > 700 :
                    prob_ham_body = 700
                if prob_spam_sub > 700:
                   prob_spam_sub = 700
                if prob_ham_sub > 700:
                    prob_ham_sub = 700
                prob_body = (math.exp(prob_spam_body), math.exp(prob_ham_body))
                prob_sub = (math.exp(prob_spam_sub), math.exp(prob_ham_sub))

        #calcul sans le log par defaut    
        else :
            if combinaison_log : 
                #si le log n'est pas utilise dans le calcul et la combinaison se fait avec le log, 
                #on considere seulement le sujet
                prob_sub = (math.log(self.subject_spam_ham_prob(subject_orig)[0]), math.log(self.subject_spam_ham_prob(subject_orig)[1]))
                prob_spam = prob_sub[0]
                prob_ham = prob_sub[1]
                if prob_spam > prob_ham:
                    return True
                else:
                    return False
            else :
                prob_body = self.spam_ham_body_prob(body_orig)
                prob_sub = self.subject_spam_ham_prob(subject_orig)
            
        alpha = 0.15
        beta = 1 - alpha        


        prob_spam = alpha * prob_body[0] + beta * prob_sub[0]
        prob_ham = alpha * prob_body[1] + beta * prob_sub[1]

        if prob_spam > prob_ham:
            return True
        else:
            return False


    def is_spam1(self, P, H, T1, T2, T3):
        return (P and (H and T1 or T2)) or (H and T2 and not T3)


    def is_spam2(self, P, T2, T3):
        return (P or (not T3 and T2))
        

    def load_dict(self, jsonFile):
        with open( jsonFile, "r") as file:
            dict_vocab = json.load(file)
        return dict_vocab


    def spam_ham_body_prob(self, body):   
        '''  Description: fonction pour calculer la probabilite
        que le 'body' d'email est spam ou ham.
        Sortie: probabilite que email body est spam, probabilite
        que email body est ham.
        '''
        dict_vocab = self.load_dict(self.vocab)
        
        numerator_spam = self.p_spam
        numerator_ham = self.p_ham

        prob_w_spam = 1
        prob_w_ham = 1
        #recuperer les p(w|spam)
        for word in body:
            if word in dict_vocab["spam_body"]:
                prob_w_spam = dict_vocab["spam_body"][word]

            else:
                prob_w_spam = 1/( dict_vocab["spam_body_counter"] + 1)

            if word in dict_vocab["ham_body"]:
                prob_w_ham = dict_vocab["ham_body"][word]

            else:
                prob_w_ham = 1/( dict_vocab["ham_body_counter"] + 1)
            
            # #calcul de P(w) pour le denominateur:  nb fois mot apparait / nb total de mot
            # val = (prob_w_spam * dict_vocab["spam_body_counter"] + \
            # prob_w_ham * dict_vocab["ham_body_counter"] )\
            # / (dict_vocab["ham_body_counter"] + \
            # dict_vocab["spam_body_counter"] )

            numerator_spam *= prob_w_spam
            numerator_ham *= prob_w_ham
            
        # La probabilite est calculee avec log pour eviter les underflows. 
        proba_body_spam = numerator_spam 
        proba_body_ham = numerator_ham

        return (proba_body_spam, proba_body_ham)


    def spam_ham_body_prob_log(self, body):   
        '''  Description: fonction pour calculer la probabilite
        que le 'body' d'email est spam ou ham.
        Sortie: probabilite que email body est spam, probabilite
        que email body est ham.
        '''     
        dict_vocab = self.load_dict(self.vocab)
        numerator_spam = math.log(self.p_spam)
        numerator_ham = math.log(self.p_ham)
        denominator_log = 0

        #recuperer les p(w|spam)
        for word in body:
            if word in dict_vocab["spam_body"]:
                prob_w_spam = dict_vocab["spam_body"][word]
                prob_w_spam_log = math.log(prob_w_spam)

            else:
                prob_w_spam = 1/( dict_vocab["spam_body_counter"] + 1)
                prob_w_spam_log = math.log(prob_w_spam)

            if word in dict_vocab["ham_body"]:
                prob_w_ham = dict_vocab["ham_body"][word]
                prob_w_ham_log = math.log(prob_w_ham)

            else:
                prob_w_ham = 1/( dict_vocab["ham_body_counter"] + 1)
                prob_w_ham_log = math.log(prob_w_ham)

            #calcul de P(w) pour le denominateur:  nb fois mot apparait / nb total de mot
            val = (prob_w_spam * dict_vocab["spam_body_counter"] + \
            prob_w_ham * dict_vocab["ham_body_counter"] )\
            / (dict_vocab["ham_body_counter"] + \
            dict_vocab["spam_body_counter"] )

            denominator_log += math.log(val)
            numerator_spam += prob_w_spam_log
            numerator_ham += prob_w_ham_log

        # La probabilite est calculee avec log pour eviter les underflows. 
        # La division est donc remplacee par une soustraction.
        proba_body_spam = numerator_spam - denominator_log
        proba_body_ham = numerator_ham - denominator_log

        return (proba_body_spam, proba_body_ham)    


    def subject_spam_ham_prob_log(self, subject):
        '''
        Description: fonction pour calculer la probabilite
        que le sujet d'email est spam ou ham.
        Sortie: probabilite que email subject est spam, probabilite
        que email subject est ham.
        '''
        dict_vocab = self.load_dict(self.vocab)
        numerator_spam = math.log(self.p_spam)
        numerator_ham = math.log(self.p_ham)
        denominator_log = 0

        #recuperer les p(w1|spam)
        for word in subject:
            if word in dict_vocab["spam_sub"]:
                prob_w_spam = dict_vocab["spam_sub"][word]
                prob_w_spam_log = math.log(prob_w_spam)
            else:
                prob_w_spam = 1/( dict_vocab["spam_sub_counter"] + 1)
                prob_w_spam_log = math.log(prob_w_spam)

            if word in dict_vocab["ham_sub"]:
                prob_w_ham = dict_vocab["ham_sub"][word]
                prob_w_ham_log = math.log(prob_w_ham)
            else:
                prob_w_ham = 1/( dict_vocab["ham_sub_counter"] + 1)
                prob_w_ham_log = math.log(prob_w_ham)

            #Calcul de P(w)
            val = (prob_w_spam * dict_vocab["spam_sub_counter"] + \
            prob_w_ham * dict_vocab["ham_sub_counter"] )\
            / (dict_vocab["ham_sub_counter"] + \
            dict_vocab["spam_sub_counter"] )

            denominator_log += math.log(val)

            numerator_spam += prob_w_spam_log
            numerator_ham += prob_w_ham_log
      
        proba_subject_spam = numerator_spam - denominator_log
        proba_subject_ham = numerator_ham - denominator_log 

        return (proba_subject_spam, proba_subject_ham)


    def subject_spam_ham_prob(self, subject):
        '''
        Description: fonction pour calculer la probabilite
        que le sujet d'email est spam ou ham.
        Sortie: probabilite que email subject est spam, probabilite
        que email subject est ham.
        '''
        dict_vocab = self.load_dict(self.vocab)

        numerator_spam = self.p_spam
        numerator_ham = self.p_ham

        #recuperer les p(w1|spam)
        for word in subject:
            if word in dict_vocab["spam_sub"]:
                prob_w_spam = dict_vocab["spam_sub"][word]
            else:
                prob_w_spam = 1/( dict_vocab["spam_sub_counter"] + 1)

            if word in dict_vocab["ham_sub"]:
                prob_w_ham = dict_vocab["ham_sub"][word]
            else:
                prob_w_ham = 1/( dict_vocab["ham_sub_counter"] + 1)

            # #Calcul de P(w)
            # val = (prob_w_spam * dict_vocab["spam_sub_counter"] + \
            # prob_w_ham * dict_vocab["ham_sub_counter"] )\
            # / (dict_vocab["ham_sub_counter"] + \
            # dict_vocab["spam_sub_counter"] )

            numerator_spam *= prob_w_spam
            numerator_ham *= prob_w_ham   

        proba_subject_spam = numerator_spam 
        proba_subject_ham = numerator_ham 

        return (proba_subject_spam, proba_subject_ham)