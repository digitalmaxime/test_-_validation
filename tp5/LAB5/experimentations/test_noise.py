import random
import json

with open("words_test.txt", 'r') as file:
    listWords = file.read()#.split(',')
    # print("Type of listWord ", type(listWords))
    listWords = listWords.replace('\n', '')
    listWords = listWords.replace(']', '')    
    listWords = listWords.replace('[', '')    
    listWords = listWords.replace('\'', '')    
    listWords = listWords.replace(' ', '')    
    listWords = listWords.split(',')

    with open("../train700.json", 'r') as trainSet:
        readFile = json.load(trainSet)
        # pour chaque Subject
        for e in readFile['dataset'] :
            print(e['mail']['Subject'])
            wordListSubject = e['mail']["Subject"].split() 
            # si il y a + de 10 mots
            if len(wordListSubject) > 10 :
                ten_pourcent = len(wordListSubject)//10
                print(ten_pourcent)
                # pour chaque tranche de 10 pourcent
                for i in range(ten_pourcent) :
                    motChoisi = random.choice(listWords)
                    print(motChoisi, type(motChoisi))
                    # ajout du mot a la liste
                    wordListSubject.append(motChoisi)
                    print(wordListSubject)
                # modifier le texte lui-meme
                e['mail']['Subject'] = ' '.join(wordListSubject)

        with open('test300_noise.json', 'w') as writeFile :
            json.dump(readFile, writeFile, indent=4)
            


# print(listWords)
# print(type(listWords))
# # for i in range (10):
# #     print(listWords[i])
# words.close()


# listWords2 = " la uncle rummie s hangover pills ! absolutely new ! naeyc"
# listWords2 = listWords2.split()
# print(len(listWords2))

# listWords2 = listWords2.split(',')
# # for e in listWords2:
# #     e.strip("\'")
# print(listWords2)
# print("type of list2 : ", type(listWords2))
# motChoisi = random.choice(listWords2)
# print(random.choice(listWords2))