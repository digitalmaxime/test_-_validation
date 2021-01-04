import json
from vocabulary_creator import VocabularyCreator
from renege import RENEGE
from email_analyzer import EmailAnalyzer
from csv_reader import read_csv, write_csv 



#evaluate_spam equivalent a P dans la formule 1 et 2
def evaluate(calcul_mode, file):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
       
    analyzer = EmailAnalyzer()
    with open(file) as email_file:       #200 emails verification
        new_emails = json.load(email_file)

    for e_mail in new_emails["dataset"]:  #dans le cas du 1000-mails      
        new_email = e_mail["mail"]
        subject = new_email["Subject"]
        body = new_email["Body"]
        spam = new_email["Spam"]
        user = new_email["From"]

        use_log = 1
        combinaison_log = 1
        vocab_counter_treshold = 1
        cleaning_mode = 3
        calcul_mode = 0
        
        evaluate_spam = analyzer.is_spam(subject, body, use_log, combinaison_log, cleaning_mode)

        if calcul_mode == 1:
            evaluate_spam = renege.call_is_spam_alternate(evaluate_spam, user, 1)
        
        if calcul_mode == 2:
            evaluate_spam = renege.call_is_spam_alternate(evaluate_spam, user, 2)
            
        if ((evaluate_spam )) and (spam == "true"):
            tp += 1
        if (not (evaluate_spam)) and (spam == "false"):
            tn += 1
        if ((evaluate_spam)) and (spam == "false"):
            fp += 1
        if (not (evaluate_spam)) and (spam == "true"):
            fn += 1

    accuracy = (tp + tn) / (tp + tn + fp + fn)
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    moyenne = (accuracy + precision +recall)/3
    
    print("Accuracy: ", accuracy)
    print("Precision: ", precision)
    print("Recall: ", recall)
   
    return accuracy


if __name__ == "__main__":
    # colonnes du csv
    # 0:use_log	1:combinaison_log	2:vocab_counter_treshold	3:cleaning_mode	4:calcul_mode
    # dict_csv = read_csv("interaction3.csv")
    # dict_result = {}
    # count_line = 8
    # for key in dict_csv:
    #Nous gardons notre meilleure combinaison retenue au tp3 
    use_log = 1
    combinaison_log = 1
    vocab_counter_treshold = 1
    cleaning_mode = 3
    calcul_mode = 0

#    # 1. Creation de vocabulaire.
    file = "800-mails.json"
    vocab = VocabularyCreator(cleaning_mode, file)     #800 mails
    vocab.create_vocab(vocab_counter_treshold)

#     # 2. Classification des emails et initialisation de utilisateurs et groupes.
    renege = RENEGE(file)             #800 mails
    renege.classify_emails(calcul_mode, cleaning_mode)

#     #3. Evaluation de performance du modele avec la fonction evaluate()
    file = "200-mails.json"
    results = evaluate(calcul_mode, file)                      #200 mails
