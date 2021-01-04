import json

from email_analyzer import EmailAnalyzer
import math

import unittest
from unittest.mock import patch


class TestEmailAnalyzer(unittest.TestCase):
    def setUp(self):
        self.subject = ""
        self.body = ""
        self.clean_subject = []  # données pour mocker "return_value" du "clean_text"
        self.clean_body = []  # données pour mocker "return_value" du "clean_text"
        self.spam_ham_body_prob_true = (
            0.7,
            0.3,
        )  # données pour mocker "return_value" du "spam_ham_body_prob"
        self.subject_spam_ham_prob_true = (
            0.7,
            0.3,
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.spam_ham_body_prob_false = (
            0.3,
            0.7,
        )  # données pour mocker "return_value" du "spam_ham_body_prob"
        self.subject_spam_ham_prob_false = (
            0.3,
            0.7,
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.vocab = (
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
                "spam_sub_counter": 1000,
                "ham_sub_counter": 1000,
                "spam_body_counter": 1000,
                "ham_body_counter": 1000
            }
        )  # vocabulaire avec les valeurs de la probabilité pour mocker "return_value" du "load_dict"
        self.spam_ham_body_prob_expected = 1.0 , 0  # valeurs de la probabilité attendus
        self.subject_spam_ham_prob_expected = 1, 0  # valeurs de la probabilité attendus

    def tearDown(self):
        pass

    @patch("text_cleaner.TextCleaning.clean_text")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_body_prob")
    @patch("email_analyzer.EmailAnalyzer.subject_spam_ham_prob")
    def test_is_spam_Returns_True_if_spam_prob_is_higher(
        self, mock_subject_spam_ham_prob, mock_spam_ham_body_prob, mock_clean_text
    ):
        """
        Il faut mocker les fonctions "spam_ham_body_prob" et 'subject_spam_ham_prob'.
        La sortie de la fonction doit être True si probabilité spam > probabilité ham
        (ces probabilites devron etre calcule selon l'enonce dans le TP1 )
        """
        mock_subject_spam_ham_prob.return_value = self.subject_spam_ham_prob_true
        mock_spam_ham_body_prob.return_value = self.spam_ham_body_prob_true
        mock_clean_text.return_value = self.clean_subject

        ea = EmailAnalyzer()
        self.assertTrue(ea.is_spam(self.subject,self.body))


    @patch("text_cleaner.TextCleaning.clean_text")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_body_prob")
    @patch("email_analyzer.EmailAnalyzer.subject_spam_ham_prob")
    def test_is_spam_Returns_False_if_spam_prob_is_lower(
        self, mock_subject_spam_ham_prob, mock_spam_ham_body_prob, mock_clean_text
    ):
        """
        Il faut mocker les fonctions "spam_ham_body_prob" et "subject_spam_ham_prob".
        La sortie de la fonction doit être False si probabilité spam  probabilité ham
        (ces probabilites devron etre calcule selon l'enonce dans le TP1 )
        """
        mock_subject_spam_ham_prob.return_value = self.subject_spam_ham_prob_false
        mock_spam_ham_body_prob.return_value = self.spam_ham_body_prob_false
        mock_clean_text.return_value = self.clean_subject
        ea = EmailAnalyzer()
        self.assertFalse(ea.is_spam(self.subject,self.body))

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    @patch("email_analyzer.EmailAnalyzer.calcul_pHam_pSpam")
    def test_spam_ham_body_prob_Returns_expected_probability(
        self, mock_calcul_pHam_pSpam, mock_load_dict):
        """
        Il faut mocker la fonction "load_dict"
        Il faut vérifier que probabilité est calculée correctement donner le "body" à l'entrée
        (ces probabilites devron etre calcule selon l'enonce dans le TP1 )
        """
        mock_load_dict.return_value = self.vocab
        mock_calcul_pHam_pSpam.return_value = (0.5,0.5)
        ea = EmailAnalyzer()
        proba = ea.spam_ham_body_prob({"spam_b_1"})
        prob_spam = round(math.exp(proba[0]),2)
        prob_ham = round(math.exp(proba[1]),2)        
        self.assertEqual(prob_spam,self.spam_ham_body_prob_expected[0])
        self.assertEqual(prob_ham,self.spam_ham_body_prob_expected[1])

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    @patch("email_analyzer.EmailAnalyzer.calcul_pHam_pSpam")
    def test_subject_spam_ham_prob_Returns_expected_probability(
        self, mock_calcul_pHam_pSpam, mock_load_dict):
        """
        Il faut mocker la fonction "load_dict"
        il faut vérifier que probabilité est calculée correctement donné le "sujet" a l'entrée
        (ces probabilites devron etre calcule selon l'enonce dans le TP1 )
        """
        mock_load_dict.return_value = self.vocab
        mock_calcul_pHam_pSpam.return_value = (0.5,0.5)
        ea = EmailAnalyzer()
        proba = ea.subject_spam_ham_prob({"spam_s_1"})
        prob_spam = round(math.exp(proba[0]),2)
        prob_ham = round(math.exp(proba[1]),2)        
        self.assertEqual(prob_spam,self.subject_spam_ham_prob_expected[0])
        self.assertEqual(prob_ham,self.subject_spam_ham_prob_expected[1])



#if __name__ == "__main__":

    #unittest.main()
