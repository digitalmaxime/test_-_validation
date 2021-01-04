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
        self.data = {}

        with open(self.email_file_classify, "r") as file:
            self.data = json.load(file)
        
        spam_counter = 0
        email_counter = 0

        for email in self.data["dataset"] :
            if email["mail"]["Spam"] == "true":
                spam_counter += 1
            email_counter += 1 

        self.p_spam = spam_counter / email_counter
        self.p_ham = 1 - self.p_spam

    def is_spam(self, subject_orig, body_orig):
        '''
        Description: fonction pour verifier si e-mail est spam ou ham,
        en calculant les probabilites d'etre spam et ham, 
        donnee le sujet et le texte d'email. 
        Sortie: 'True' - si l'email est spam, 'False' - si email est ham.
        '''
        subject_orig = self.cleaning.clean_text(subject_orig)
        body_orig = self.cleaning.clean_text(body_orig)

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
        
    def spam_ham_body_prob(self, body):   
        '''  Description: fonction pour calculer la probabilite
        que le 'body' d'email est spam ou ham.
        Sortie: probabilite que email body est spam, probabilite
        que email body est ham.
        '''
        
        with open(self.vocab, "r") as file:
            dict_vocab = json.load(file)


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

            
            #calcul de P(w) pour le denominateur
            val = (prob_w_spam * dict_vocab["spam_body_counter"] + \
            prob_w_ham * dict_vocab["ham_body_counter"] )\
            / (dict_vocab["ham_body_counter"] + \
            dict_vocab["spam_body_counter"] )

            denominator_log += math.log(val)

            numerator_spam += prob_w_spam_log
            numerator_ham += prob_w_ham_log
            
        # La probabilite est calculee avec log pour eviter les underflows. 
        #La division est donc remplacee par une soustraction.
        proba_body_spam = numerator_spam - denominator_log
        proba_body_ham = numerator_ham - denominator_log

        return (proba_body_spam, proba_body_ham)

    def subject_spam_ham_prob(self, subject):
        '''
        Description: fonction pour calculer la probabilite
        que le sujet d'email est spam ou ham.
        Sortie: probabilite que email subject est spam, probabilite
        que email subject est ham.
        '''
        with open(self.vocab, "r") as file:
            dict_vocab = json.load(file)


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
 

