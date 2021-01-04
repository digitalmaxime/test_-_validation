import json
import os
from text_cleaner import TextCleaning


class VocabularyCreator:
    """Class for creating vocabulary of spam and non-spam messages"""

    def __init__(self):
        self.train_set = "800-mails.json" 
        self.cleaning = TextCleaning()
        self.vocabulary = "vocabulary.json"
        self.spam_sub_counter = 0
        self.ham_sub_counter = 0
        self.spam_body_counter = 0
        self.ham_body_counter = 0

    def load_dict(self): #pragma: no cover
        with open(self.train_set, "r") as file:
            data = json.load(file)
        return data

    def write_data_to_vocab_file(self, vocab): #pragma: no cover
        try:
            with open(self.vocabulary, "w") as outfile:
                json.dump(vocab,outfile, indent=4)
                print("Vocabulary created...")
                return True
        except:
            return False

    def clean_text(self,text): #pragma: no cover
        return self.cleaning.clean_text(text)    


    def define_vocab(self):
        '''
        Description: fonction pour creer le vocabulaire des mots presents
        dans les e-mails spam et ham et le sauvegarder dans le fichier
        vocabulary.json selon le format specifie dans la description de lab
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''       
        
        data = self.load_dict()

        cleaner = TextCleaning()

        dict_vocab = {
            "spam_sub": {},
            "ham_sub":{},
            "spam_body":{},
            "ham_body":{},
            "spam_sub_counter" : 0,
            "ham_sub_counter" : 0,
            "spam_body_counter" : 0,
            "ham_body_counter" : 0
        }

        for email in data["dataset"]:
            subject = email["mail"]["Subject"]
            body = email["mail"]["Body"]
            
            subject = cleaner.clean_text(subject)
            body = cleaner.clean_text(body)

            #compter l'occurence des mots dans les differents contextes
            if email["mail"]["Spam"] == "true" :
                for word in subject:
                    if word not in dict_vocab["spam_sub"].keys():
                        dict_vocab["spam_sub"][word] = 1
                    else:
                        dict_vocab["spam_sub"][word] += 1
                    dict_vocab["spam_sub_counter"] += 1
                for word in body:
                    if word not in dict_vocab["spam_body"].keys():
                        dict_vocab["spam_body"][word] = 1
                    else:
                        dict_vocab["spam_body"][word] += 1
                    dict_vocab["spam_body_counter"] += 1
            else:   #HAM
                for word in subject:
                    if word not in dict_vocab["ham_sub"].keys():
                        dict_vocab["ham_sub"][word] = 1
                    else:
                        dict_vocab["ham_sub"][word] += 1
                    dict_vocab["ham_sub_counter"] += 1 
                for word in body:
                    if word not in dict_vocab["ham_body"].keys():
                        dict_vocab["ham_body"][word] = 1
                    else:
                        dict_vocab["ham_body"][word] += 1
                    dict_vocab["ham_body_counter"] += 1
        
        #Faire un ratio en l'occurence d'un mot dans un contexte particulier (ex; spam body) 
        #et le compteur de tous les mots dans ce contexte
        for key,value in dict_vocab["spam_sub"].items():
            value /= dict_vocab["spam_sub_counter"]
            dict_vocab["spam_sub"][key] = value

        for key,value in dict_vocab["spam_body"].items():
            value /= dict_vocab["spam_body_counter"]
            dict_vocab["spam_body"][key] = value

        for key,value in dict_vocab["ham_sub"].items():
            value /= dict_vocab["ham_sub_counter"]
            dict_vocab["ham_sub"][key] = value

        for key,value in dict_vocab["ham_body"].items():
            value /= dict_vocab["ham_body_counter"]
            dict_vocab["ham_body"][key] = value        

        return dict_vocab 
    
    def create_vocab(self): 
        vocab = self.define_vocab()
        self.write_data_to_vocab_file(vocab)

