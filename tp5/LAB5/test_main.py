import random
import json
import copy
import unittest
from main import evaluate
from vocabulary_creator import VocabularyCreator
from renege import RENEGE
from email_analyzer import EmailAnalyzer
from csv_reader import read_csv, write_csv 

#   CREATION DE NOUVEAUX FICHIERS POUR LES TESTS
#  Pour changement d’ordre des e-mails : fichiers ”train700 mails.json” et ”test300 mails.json”.
# — Pour changement d’ordre des mots : fichiers ”train700 words.json” et ”test300 words.json”.
# — Pour le doublement des e-mails : fichiers ”train700x2.json” et ”test300x2.json”.
# — Pour l’ajout du bruit : fichiers ”train700 noise.json” et ”test300 noise.json”.



class TestMetamorphique(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):

        cls.use_log = 1
        cls.combinaison_log = 1
        cls.vocab_counter_treshold = 1
        cls.cleaning_mode = 3
        cls.calcul_mode = 0

        #calcul de Accuracy selon le main
        file = "train700.json"
        vocab = VocabularyCreator(cls.cleaning_mode, file)     
        vocab.create_vocab(cls.vocab_counter_treshold)

        renege = RENEGE(file)            
        renege.classify_emails(cls.calcul_mode, cls.cleaning_mode)

        file = "test300.json"
        print('*' * 40)
        cls.accuracy_main = evaluate(cls.calcul_mode, file)  
        
        print('-' * 40)
    
            
        
        ###########Traitement des nouveaux fichiers#############
        
        #randomiser les courriels
        #Creation train700_mails.json
        
        with open("train700.json") as users_file: 
            train700 = json.load(users_file)

        random.shuffle(train700["dataset"])

        with open("train700_mails.json", "w") as outfile:
            json.dump(train700, outfile, indent=4)

        #Creation test300_mails.json
        with open("test300.json") as users_file:
            train300 = json.load(users_file)

        random.shuffle(train300["dataset"])

        with open("test300_mails.json", "w") as outfile:
            json.dump(train300, outfile, indent=4)

        #DOUBLER les courriels
        #Création de train700x2.json
        with open("train700.json") as users_file:
            train700 = json.load(users_file)

        newList = train700["dataset"]
        newList = newList + train700["dataset"]
        newDict = {"dataset": newList}

        with open("train700x2.json", "w") as outfile:
            json.dump(newDict, outfile, indent=4)

        #Création de test300x2.json
        with open("test300.json") as users_file:
            test300 = json.load(users_file)

        newList = test300["dataset"]
        newList = newList + test300["dataset"]
        newDict = {"dataset": newList}

        with open("test300x2.json", "w") as outfile:
            json.dump(newDict, outfile, indent=4)
        
        #Changement d’ordre des mots fichiers 
        # Creation de ”test300 words.json”.
        with open("test300.json") as users_file:
            test300 = json.load(users_file)

        for mail in test300["dataset"] :
            subject = mail["mail"]["Subject"]
            subject = subject.split()
            random.shuffle(subject)
            subject = " ".join(subject)
            mail["mail"]["Subject"] = subject
            body= mail["mail"]["Body"]
            body = body.split()
            random.shuffle(body)
            body = " ".join(body)
            mail["mail"]["Body"] = body    

        with open("test300_words.json", "w") as outfile:
            json.dump(test300, outfile, indent=4)

        # Creation de ”train700 words.json” et 
        with open("train700.json") as users_file:
            train700 = json.load(users_file)

        for mail in train700["dataset"] :
            subject = mail["mail"]["Subject"]
            subject = subject.split()
            random.shuffle(subject)
            subject = " ".join(subject)
            mail["mail"]["Subject"] = subject
            body= mail["mail"]["Body"]
            body = body.split()
            random.shuffle(body)
            body = " ".join(body)
            mail["mail"]["Body"] = body    

        with open("train700_words.json", "w") as outfile:
            json.dump(train700, outfile, indent=4)


        # Pour ajouter du 'NOISE' dans train700_noise
        with open("words.txt", 'r') as noise_words_file:
            noiselistWords = noise_words_file.read()
            noiselistWords = noiselistWords.replace('\n', '')
            noiselistWords = noiselistWords.replace(']', '')    
            noiselistWords = noiselistWords.replace('[', '')    
            noiselistWords = noiselistWords.replace('\'', '')    
            noiselistWords = noiselistWords.replace(' ', '')    
            noiselistWords = noiselistWords.split(',') # convert to list

            with open("train700.json", 'r') as trainSet:
                trainSetDic = json.load(trainSet)
                # pour chaque Subject
                for e in trainSetDic['dataset'] :
                    wordListSubject = e['mail']["Subject"].split() 
                    wordListBody = e['mail']["Body"].split() 

                    # si il y a + de 10 mots dans le subject
                    if len(wordListSubject) > 10 :
                        ten_pourcent = len(wordListSubject)//10
                        # pour chaque tranche de 10 pourcent
                        for i in range(ten_pourcent) :
                            chosenNoiseWord = random.choice(noiselistWords)
                            # ajout du mot a la liste
                            wordListSubject.append(chosenNoiseWord)
                        # modifier le texte lui-meme
                        e['mail']['Subject'] = ' '.join(wordListSubject)
                    
                    # si il y a + de 10 mots dans le Body
                    if len(wordListBody) > 10 :
                        ten_pourcent = len(wordListBody)//10
                        # pour chaque tranche de 10 pourcent
                        for i in range(ten_pourcent) :
                            chosenNoiseWord = random.choice(noiselistWords)
                            # ajout du mot a la liste
                            wordListBody.append(chosenNoiseWord)
                        # modifier le texte lui-meme
                        e['mail']['Body'] = ' '.join(wordListBody)

                with open('train700_noise.json', 'w') as writeFile :
                    json.dump(trainSetDic, writeFile, indent=4)
        
        # Pour ajouter du 'NOISE' dans test300_noise
        with open("test300.json", 'r') as testSet:
            testSetDic = json.load(testSet)
            # pour chaque Subject
            for e in testSetDic['dataset'] :
                wordListSubject = e['mail']["Subject"].split() 
                wordListBody = e['mail']["Body"].split() 
                # si il y a + de 10 mots dans le subject
                if len(wordListSubject) > 10 :
                    ten_pourcent = len(wordListSubject)//10
                    # pour chaque tranche de 10 pourcent
                    for i in range(ten_pourcent) :
                        chosenNoiseWord = random.choice(noiselistWords)
                        # ajout du mot a la liste
                        wordListSubject.append(chosenNoiseWord)
                    # modifier le texte lui-meme
                    e['mail']['Subject'] = ' '.join(wordListSubject)

                # si il y a + de 10 mots dans le Body
                if len(wordListBody) > 10 :
                    ten_pourcent = len(wordListBody)//10
                    # pour chaque tranche de 10 pourcent
                    for i in range(ten_pourcent) :
                        chosenNoiseWord = random.choice(noiselistWords)
                        # ajout du mot a la liste
                        wordListBody.append(chosenNoiseWord)
                    # modifier le texte lui-meme
                    e['mail']['Body'] = ' '.join(wordListBody)

            with open('test300_noise.json', 'w') as writeFile :
                json.dump(testSetDic, writeFile, indent=4)

    def tearDown(self):
        pass

    #    changement de l'ordre des emails dans le ”train dataset”
    def test_property1(self):
        print('*'*20, self.accuracy_main, '*'*20)
        print("************test1************")
        file = "train700_mails.json"
        vocab = VocabularyCreator(self.cleaning_mode, file)     
        vocab.create_vocab(self.vocab_counter_treshold)

        renege = RENEGE(file)            
        renege.classify_emails(self.calcul_mode, self.cleaning_mode)

        file = "test300.json"
        accuracy = evaluate(self.calcul_mode, file) 
        self.assertTrue( abs(accuracy - self.accuracy_main) < 0.03)                    

    # #changement de l'ordre des emails dans le ”test dataset”
    def test_property2(self):
        print("************test2************")
        file = "train700.json"
        vocab = VocabularyCreator(self.cleaning_mode, file)     
        vocab.create_vocab(self.vocab_counter_treshold)

        renege = RENEGE(file)            
        renege.classify_emails(self.calcul_mode, self.cleaning_mode)

        file = "test300_mails.json"
        accuracy = evaluate(self.calcul_mode, file) 
        self.assertTrue( abs(accuracy - self.accuracy_main) < 0.03)  
    
    
    # #3: changement de l’ordre des mots dans le ”train dataset”
    def test_property3(self):
        print("************test3************")
        file = "train700_words.json"
        vocab = VocabularyCreator(self.cleaning_mode, file)     
        vocab.create_vocab(self.vocab_counter_treshold)

        renege = RENEGE(file)            
        renege.classify_emails(self.calcul_mode, self.cleaning_mode)

        file = "test300.json"
        accuracy = evaluate(self.calcul_mode, file) 
        self.assertTrue( abs(accuracy - self.accuracy_main) < 0.03) 
    
    # #4: changement de l’ordre des mots dans le ”test dataset”
    def test_property4(self):
        print("************test4************")
        file = "train700.json"
        vocab = VocabularyCreator(self.cleaning_mode, file)     
        vocab.create_vocab(self.vocab_counter_treshold)

        renege = RENEGE(file)            
        renege.classify_emails(self.calcul_mode, self.cleaning_mode)

        file = "test300_words.json"
        accuracy = evaluate(self.calcul_mode, file) 
        self.assertTrue( abs(accuracy - self.accuracy_main) < 0.03) 



    # # 5:l’ajout des memes e-mails dans le ”train dataset”
    def test_property5(self):
        print("************test5************")
        file = "train700x2.json"
        vocab = VocabularyCreator(self.cleaning_mode, file)     
        vocab.create_vocab(self.vocab_counter_treshold)

        renege = RENEGE(file)            
        renege.classify_emails(self.calcul_mode, self.cleaning_mode)

        file = "test300.json"
        accuracy = evaluate(self.calcul_mode, file) 
        self.assertTrue( abs(accuracy - self.accuracy_main) < 0.03)  


    # # 6: l’ajout des memes e-mails dans le ”test dataset”
    def test_property6(self):
        print("************test6************")
        file = "train700.json"
        vocab = VocabularyCreator(self.cleaning_mode, file)     
        vocab.create_vocab(self.vocab_counter_treshold)

        renege = RENEGE(file)            
        renege.classify_emails(self.calcul_mode, self.cleaning_mode)

        file = "test300x2.json"
        accuracy = evaluate(self.calcul_mode, file) 
        self.assertTrue( abs(accuracy - self.accuracy_main) < 0.03) 

    # 7: l’ajout du ”bruit” dans le ”train dataset” 
    def test_property7(self) :
        print("************test7************")
        file = "train700_noise.json"
        vocab = VocabularyCreator(self.cleaning_mode, file)     
        vocab.create_vocab(self.vocab_counter_treshold)

        renege = RENEGE(file)            
        renege.classify_emails(self.calcul_mode, self.cleaning_mode)

        file = "test300.json"
        accuracy = evaluate(self.calcul_mode, file) 
        self.assertTrue( abs(accuracy - self.accuracy_main) < 0.03)
    
    # # 8. apres l’ajout du bruit dans ”test dataset”.
    def test_property8(self) :
        print("************test8************")
        file = "train700.json"
        vocab = VocabularyCreator(self.cleaning_mode, file)     
        vocab.create_vocab(self.vocab_counter_treshold)

        renege = RENEGE(file)            
        renege.classify_emails(self.calcul_mode, self.cleaning_mode)

        file = "test300_noise.json"
        accuracy = evaluate(self.calcul_mode, file) 
        self.assertTrue( abs(accuracy - self.accuracy_main) < 0.03)