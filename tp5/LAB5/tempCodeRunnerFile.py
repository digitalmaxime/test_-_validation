    # def test_property7(self) :
    #     print("************test7************")
    #     file = "train700_noise.json"
    #     vocab = VocabularyCreator(self.cleaning_mode, file)     
    #     vocab.create_vocab(self.vocab_counter_treshold)

    #     renege = RENEGE(file)            
    #     renege.classify_emails(self.calcul_mode, self.cleaning_mode)

    #     file = "test300.json"
    #     accuracy = evaluate(self.calcul_mode, file) 
    #     self.assertTrue( abs(accuracy - self.accuracy_main) < 0.03)
    
    # # 8. apres l’ajout du bruit dans ”test dataset”.
    # def test_property8(self) :
    #     print("************test8************")
    #     file = "train700.json"
    #     vocab = VocabularyCreator(self.cleaning_mode, file)     
    #     vocab.create_vocab(self.vocab_counter_treshold)

    #     renege = RENEGE(file)            
    #     renege.classify_emails(self.calcul_mode, self.cleaning_mode)

    #     file = "test300_noise.json"
    #     accuracy = evaluate(self.calcul_mode, file) 
    #     self.assertTrue( abs(accuracy - self.accuracy_main) < 0.03)