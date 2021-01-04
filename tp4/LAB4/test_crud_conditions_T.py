from crud import CRUD
import unittest
from unittest.mock import patch

class TestCrudConditionsT(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_chaine_1(self):
        crud = CRUD()
        result = crud.add_new_user("user1@email", "2020-11-15")
        self.assertTrue(result)
        result = crud.add_new_user("user2@email", "2020-11-15")
        self.assertTrue(result)
        result = crud.update_users("2", "name", "newuser2@email")
        self.assertTrue(result)
        result = crud.get_user_data("1","name")
        self.assertTrue(result)
        result = crud.update_users("1", "name", "newuser1@email")
        self.assertTrue(result)
        result = crud.add_new_user("user3@email", "2020-11-15")
        self.assertTrue(result)
        result = crud.get_user_data("1","name")
        self.assertTrue(result)
        result = crud.get_user_data("1","name")
        self.assertTrue(result)
        result = crud.add_new_user("user4@email", "2020-11-15")
        self.assertTrue(result)
        result = crud.remove_user("4")
        self.assertTrue(result)
        result = crud.add_new_user("user4@email", "2020-11-15")
        self.assertTrue(result)
        #with self.assertRaises(AssertionError):
        result = crud.remove_user_group("4", "default")
        self.assertTrue(result)
        result = crud.add_new_user("user5@email", "2020-11-15")
        self.assertTrue(result)
        result = crud.remove_user("5")
        self.assertTrue(result)
        result = crud.remove_user("4")
        self.assertTrue(result)
        result = crud.update_users("1", "name", "newnewuser1@email")
        self.assertTrue(result)
        result = crud.remove_user("3")
        self.assertTrue(result)
        result = crud.get_user_data("1","name")
        self.assertTrue(result)
        result = crud.remove_user("2")
        self.assertTrue(result)
        result = crud.remove_user_group("1", "default")
        self.assertTrue(result)

    def test_chaine_2(self):
        crud = CRUD()
        result = crud.add_new_user("user1@email", "2020-11-15")
        self.assertTrue(result)
        result = crud.update_users("1", "name", "newuser1@email")
        self.assertTrue(result)
        result = crud.update_users("1", "name", "newnewuser1@email")
        self.assertTrue(result)
        result = crud.remove_user("1")
        self.assertTrue(result)

    def test_chaine_3(self):
        crud = CRUD()
        result = crud.add_new_user("user1@email", "2020-11-15")
        self.assertTrue(result)
        result = crud.update_users("1", "name", "newuser1@email")
        self.assertTrue(result)
        result = crud.remove_user_group("1", "default")
        self.assertTrue(result)
    
    def test_chaine_4(self):
        crud = CRUD()
        result = crud.add_new_user("user1@email", "2020-11-15")
        self.assertTrue(result)
        result = crud.get_user_data("1","name")
        self.assertTrue(result)
        result = crud.remove_user_group("1", "default")
        self.assertTrue(result)



