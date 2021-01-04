from vocabulary_creator import VocabularyCreator
import unittest
from unittest.mock import patch

class TestVocabularyCreator(unittest.TestCase):
    def setUp(self):
        self.mails = {
            "dataset": [
                {
                "mail": {
                    "Subject": " orignial_spam_s_1 original_spam_s_1 orignialspam_s_2 original_spam_s_3",
                    "From": "GP@paris.com",
                    "Date": "2004-08-15",
                    "Body": "original_spam_b_1",
                    "Spam": "true",
                    "File": "enronds//enron4/spam/2030.2004-08-15.GP.spam.txt"
                    }
                },
                {
                "mail": {
                    "Subject": " original_ham_s_1 original_ham_s_1 original_ham_s_2 original_ham_s_3",
                    "From": "farmer@paris.com",
                    "Date": "2000-09-15",
                    "Body": "original_ham_b1 original_ham_b2 original_ham_b3 original_ham_b3",
                    "Spam": "false",
                    "File": "enronds//enron1/ham/2256.2000-09-15.farmer.ham.txt"
                    }
                }
            ]
        }  # données pour mocker "return_value" du "load_dict"

        # self.clean_subject_spam = []  # données pour mocker "return_value" du "clean_text"
        # self.clean_body_spam = []  # données pour mocker "return_value" du "clean_text"
        # self.clean_subject_ham = []  # données pour mocker "return_value" du "clean_text"
        # self.clean_body_ham = []  # données pour mocker "return_value" du "clean_text"

        self.clean_subject= [["ham_s_1", "ham_s_1", "ham_s_2", "ham_s_3"], ["spam_s_1", "spam_s_1", "spam_s_2", "spam_s_3"]]  # données pour mocker "return_value" du "clean_text"
        self.clean_body= [["ham_b_1", "ham_b_2", "ham_b_3", "ham_b_3"], ["spam_b_1"]]  # données pour mocker "return_value" du "clean_text"

        self.vocab_expected = \
            {
                "spam_sub": {
                    "spam_s_1": 0.5,
                    "spam_s_2": 0.25,
                    "spam_s_3": 0.25
                },
                "ham_sub": {
                    "ham_s_1": 0.5,
                    "ham_s_2": 0.25,
                    "ham_s_3": 0.25
                },
                "spam_body": {
                    "spam_b_1": 1,
                },
                "ham_body":{
                    "ham_b_1": 0.25,
                    "ham_b_2": 0.25,
                    "ham_b_3": 0.5
                },
                "spam_sub_counter": 4,
                "ham_sub_counter": 4,
                "spam_body_counter": 1,
                "ham_body_counter": 4
            }
        # vocabulaire avec les valuers de la probabilité calculées correctement

    def tearDown(self):
        pass

    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    # @patch("vocabulary_creator.VocabularyCreator.clean_text")
    @patch("text_cleaner.TextCleaning.clean_text")
    @patch("vocabulary_creator.VocabularyCreator.write_data_to_vocab_file")
    def test_create_vocab_Returns_vocabulary_with_correct_values(
        self, mock_write_data_to_vocab_file, mock_clean_text, mock_load_dict
    ):
        """Description: Tester qu'un vocabulaire avec les probabilités calculées
        correctement va être retourné. Il faut mocker les fonctions "load dict"
         (utiliser self.mails comme un return value simulé),"clean text"
         (cette fonction va être appelé quelques fois, pour chaque appel on
         va simuler la return_value different, pour cela il faut utiliser
         side_effect (vois l'exemple dans l'énonce)) et
         "write_data_to_vocab_file" qui va simuler "return True" au lieu
         d'écrire au fichier "vocabulary.json".
         if faut utiliser self.assertEqual(appele_a_create_vocab(), self.vocab_expected)
        """
        list_of_values = [self.clean_body[0], self.clean_subject[0], self.clean_body[1], self.clean_subject[1]]
        
        def function_side_effect(arg):
            return list_of_values.pop()

        mock_load_dict.return_value = self.mails
        mock_clean_text.side_effect = function_side_effect
        mock_write_data_to_vocab_file.return_value = True
        
        vocabulary = VocabularyCreator()
        self.assertEqual(vocabulary.define_vocab(), self.vocab_expected)


#if __name__ == "__main__":

  #  unittest.main()
