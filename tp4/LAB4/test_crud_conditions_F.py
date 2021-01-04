from crud import CRUD
import unittest
from unittest.mock import patch

class TestCrudConditionsF(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_chaine_1(self):
        crud = CRUD()
        result = crud.update_users("1", "name", "newuser1@email")
        self.assertFalse(result)
    
    def test_chaine_2(self):
        crud = CRUD()
        with self.assertRaises(KeyError):
            crud.get_user_data("1","name")

    def test_chaine_3(self):
        crud = CRUD()
        result = crud.remove_user("1")
        self.assertFalse(result)

    def test_chaine_4(self):
        crud = CRUD()
        result = crud.remove_user_group("1", "default")
        self.assertFalse(result)