from crud import CRUD
import unittest
from unittest.mock import patch


class TestCRUD(unittest.TestCase):
    maxDiff = None
    def setUp(self):
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_users_file
        self.users_data = {
            "1": {
                "name": "alex@gmail.com",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596848266.0,
                "Date_of_last_seen_message": 1596848266.0,
                "Groups": ["default", "friends"]
            },
            "2": {
                "name": "mark@mail.com",
                "Trust": 65.45454,
                "Spamn": 171,
                "HamN": 324,
                "Date_of_first_seen_message": 1596855166.0,
                "Date_of_last_seen_message": 1596855166.0,
                "Groups": ["default"]
            }
        }
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_groups_file
        self.groups_data = {
            "1": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"]
            },
            "2": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"]
            }
        }

    def tearDown(self):
        pass

    #Test ajoute: @ is in the email
    def test_add_new_user_Return_false_if_no_a(self):
        crud = CRUD()
        self.assertFalse(crud.add_new_user("newEmailgmail.com","2020-10-10"))

    #Test ajoute:
    def test_add_new_user_Return_false_if_len_date_not_good(self):
        crud = CRUD()
        self.assertFalse(crud.add_new_user("newEmailgmail.com","2020-10"))

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_add_new_user_Passes_correct_data_to_modify_users_file(
        self, mock_modify_groups_file, mock_modify_users_file, mock_read_users_file, mock_read_groups_file
    ):
        """Description: il faut utiliser les mocks des fonctions "read_users_file",
        "modify_users_file", "modify_groups_file" (ou selon votre realisation) pour tester que
        l'information a ajouter pour l'utilisateur a étée formée correctement par la fonction, e.g.
        self.modify_users_file(data) -> "data" doit avoir un format et contenu expectee
        il faut utiliser ".assert_called_once_with(expected_data)"
        """

        mock_read_users_file.return_value = self.users_data
        mock_modify_groups_file.return_value = True 
        mock_modify_users_file.return_value = True
        mock_read_groups_file.return_value = self.groups_data
        
        crud = CRUD()
        crud.add_new_user("newEmail@gmail.com","2020-10-10")
        expected_data_users = {
            "1": {
                "name": "alex@gmail.com",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596848266.0,
                "Date_of_last_seen_message": 1596848266.0,
                "Groups": ["default", "friends"]
            },
            "2": {
                "name": "mark@mail.com",
                "Trust": 65.45454,
                "Spamn": 171,
                "HamN": 324,
                "Date_of_first_seen_message": 1596855166.0,
                "Date_of_last_seen_message": 1596855166.0,
                "Groups": ["default"]
            },
            "3": {
                "name": "newEmail@gmail.com",
                "Trust": 50,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1602288000.0,
                "Date_of_last_seen_message": 1602288000.0,
                "Groups": ["default"]
            }
        }
        expected_data_groups = {
            "1": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com","newEmail@gmail.com"]
            },
            "2": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"]
            }

        }
        self.assertEqual(expected_data_users, self.users_data)
        mock_modify_users_file.assert_called_once_with(self.users_data)

        self.assertEqual(expected_data_groups, self.groups_data)
        mock_modify_groups_file.assert_called_once_with(self.groups_data)

    #TEST AJOUTE POUR AMELIORER OUVERTURE
    @patch("crud.CRUD.read_groups_file")                        
    def test_add_new_group_Return_false_if_group_exist(
        self, mock_read_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.add_new_group("default",50,[]))

    @patch("crud.CRUD.get_user_id")
    @patch("crud.CRUD.update_users")
    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_add_new_group_Passes_correct_data_to_modify_groups_file(
        self, mock_modify_groups_file, mock_read_groups_file, mock_update_users, mock_get_user_id
    ):
        """Description: il faut utiliser les mocks des fonctions "read_groups_file",
        "modify_groups_file" (ou selon votre realisation) pour tester que
        l'information a ajouter pour le groupe a étée formée correctement par la fonction e.g.
        self.modify_groups_file(data) -> "data" doit avoir un format et contenu attendu
        il faut utiliser ".assert_called_once_with(expected_data)"
        """
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True
        mock_update_users.return_value = True
        mock_get_user_id.return_value = True

        expected_groups = {
            "1": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"]
            },
            "2": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"]
            },
            "3": {
                "name": "ennemies",
                "Trust": 0,
                "List_of_members": ["mark@mail.com"]
            }
        }
        crud = CRUD()
        crud.add_new_group("ennemies", 0, ["mark@mail.com"])
        self.assertEqual( self.groups_data, expected_groups)
        mock_modify_groups_file.assert_called_once_with(self.groups_data)


    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_id(self, mock_read_users_file):
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que false (ou bien une excepton)
        est returnee par la fonction si ID non-existant est utilisée
        il faut utiliser ".assertEqual()" ou ".assertFalse()"
        """
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        with self.assertRaises(Exception):
            crud.get_user_data("3","name")


    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_field(self, mock_read_users_file):
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que false (ou bien une excepton)
        est returnee par la fonction si champ non-existant est utilisée
        il faut utiliser ".assertEqual()" ou ".assertFalse()"
        """
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        with self.assertRaises(Exception):
            crud.get_user_data("1","abc")

    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_correct_value_if_field_and_id_are_valid(
        self, mock_read_users_file
    ):
        """Description: il faut utiliser le mock de fonction "read_groups_file",
        (ou selon votre realisation) pour tester que une bonne valeur est fournie
        si champ est id valide sont utilisee
        il faut utiliser ".assertEqual()"
        """
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertEqual(crud.get_user_data("1", "HamN"),20 )


    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_id(self, mock_read_groups_file):
        """"""
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.get_group_data('3', 'name'))
        

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_field(
        self, mock_read_groups_file
    ):
        """"""
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertFalse(crud.get_group_data('1', 'abcd'))

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_correct_value_if_field_and_id_are_valid(
        self, mock_read_groups_file
    ):
        """"""
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        self.assertEqual(crud.get_group_data('2', 'name'),"friends")

    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_false_for_invalid_user_name(
        self, mock_read_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertEqual(crud.get_user_id("maxime"),None)

    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_id_for_valid_user_name(self, mock_read_users_file):
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertEqual(crud.get_user_id("alex@gmail.com"),"1")

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_false_for_invalid_group_name(
        self, mock_read_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()    
        self.assertFalse(crud.get_group_id("a"))           

    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_id_for_valid_group_name(self, mock_read_groups_file):
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()   
        self.assertEqual(crud.get_group_id("default"),"1")

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_update_users_Returns_false_for_invalid_id(
        self, mock_modify_users_file, mock_read_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        """
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True 
        crud = CRUD()
        self.assertFalse(crud.update_users("10","name","Maxime"))

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_update_users_Returns_false_for_invalid_field(
        self,mock_modify_users_file, mock_read_users_file
    ):
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        """
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True 
        crud = CRUD()
        self.assertFalse(crud.update_users("1","champs_inexistant","Maxime"))

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_update_users_Passes_correct_data_to_modify_users_file(
        self,  mock_modify_users_file, mock_read_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True         
        crud = CRUD()
        crud.update_users("1","name","Maxime")
        mock_modify_users_file.assert_called_once_with(self.users_data)
        """Il faut utiliser les mocks pour 'read_users_file' et 'modify_users_file'
        (ou selon votre realisation)
        Il faut utiliser ".assert_called_once_with(expected_data)"
        """

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_update_groups_Returns_false_for_invalid_id(
        self, mock_modify_groups_file, mock_read_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True 
        crud = CRUD()
        self.assertFalse(crud.update_groups("10","name","nomgroupe"))

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_update_groups_Returns_false_for_invalid_field(
        self, mock_modify_groups_file , mock_read_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        """
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True 
        crud = CRUD()
        self.assertFalse(crud.update_groups("1","invalidField","nomgroupe"))

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_update_groups_Passes_correct_data_to_modify_groups_file(
        self, mock_modify_groups_file , mock_read_groups_file
    ):
        """Il faut utiliser les mocks pour 'read_groups_file' et 'modify_groups_file'
        (ou selon votre realisation)
        Il faut utiliser ".assert_called_once_with(expected_data)"
        """
        mock_modify_groups_file.return_value = True
        mock_read_groups_file.return_value = self.groups_data

        crud = CRUD()
        crud.update_groups("1", "name", "new_data")
        mock_modify_groups_file.assert_called_once_with(self.groups_data)


    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_remove_user_Returns_false_for_invalid_id(
        self, mock_modify_users_file , mock_read_users_file
    ):
        mock_modify_users_file.return_value = True
        mock_read_users_file.return_value = self.users_data
        crud = CRUD()
        self.assertFalse(crud.remove_user("10"))

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_user_Passes_correct_value_to_modify_users_file(
        self, mock_read_groups_file, mock_modify_users_file, mock_read_users_file
    ):
        mock_modify_users_file.return_value = True
        mock_read_users_file.return_value = self.users_data
        mock_read_groups_file.return_value = self.groups_data
        crud = CRUD()
        crud.remove_user("1")
        users_data_remove_1 = {
            "2": {
                "name": "mark@mail.com",
                "Trust": 65.45454,
                "Spamn": 171,
                "HamN": 324,
                "Date_of_first_seen_message": 1596855166.0,
                "Date_of_last_seen_message": 1596855166.0,
                "Groups": ["default"],
            }
        }
        self.assertEqual(self.users_data,users_data_remove_1)
        mock_modify_users_file.assert_called_once_with(self.users_data) 

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_remove_user_group_Returns_false_for_invalid_id(
        self, mock_modify_users_file, mock_read_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        crud = CRUD()
        self.assertEqual(crud.remove_user_group("100", "default"), False)


    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_remove_user_group_Returns_false_for_invalid_group(
        self, mock_modify_users_file, mock_read_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        crud = CRUD()
        self.assertEqual(crud.remove_user_group("1", "invalid_group"), False)


    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_users_file")
    def test_remove_user_group_Passes_correct_value_to_modify_users_file(
        self, mock_modify_users_file, mock_read_users_file
    ):
        mock_read_users_file.return_value = self.users_data
        mock_modify_users_file.return_value = True
        crud = CRUD()
        
        expected_modified_users = \
        {
            "1": {
                "name": "alex@gmail.com",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596848266.0,
                "Date_of_last_seen_message": 1596848266.0,
                "Groups": ["friends"]
            },
            "2": {
                "name": "mark@mail.com",
                "Trust": 65.45454,
                "Spamn": 171,
                "HamN": 324,
                "Date_of_first_seen_message": 1596855166.0,
                "Date_of_last_seen_message": 1596855166.0,
                "Groups": ["default"]
            }
        }
        crud.remove_user_group("1", "default")
        mock_modify_users_file.assert_called_once_with(self.users_data)
        self.assertEqual(self.users_data, expected_modified_users)        
        


    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_remove_group_Returns_false_for_invalid_id(
        self, mock_modify_groups_file, mock_read_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True
        crud = CRUD()
        self.assertFalse(crud.remove_group("100"))

    #TEST AJOUTE pourrestreindre possibilite d'enlever le groupe par default (group_id : "1")
    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_remove_group_Returns_false_for_invalid_id(
        self, mock_modify_groups_file, mock_read_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True
        crud = CRUD()
        self.assertFalse(crud.remove_group("1"))

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_remove_group_Passes_correct_value_to_modify_groups_file(
        self, mock_modify_groups_file, mock_read_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True
        crud = CRUD()
        expected_group_value = {
            "1": {      
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"]
            }
        }
        crud.remove_group("2")
        self.assertEqual(self.groups_data, expected_group_value)
        mock_modify_groups_file.assert_called_once_with(self.groups_data)


    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_remove_group_member_Returns_false_for_invalid_id(
        self, mock_modify_groups_file, mock_read_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True
        crud = CRUD()
        self.assertFalse(crud.remove_group_member("100", "alex@gmail.com"))


    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_remove_group_member_Returns_false_for_invalid_group_member(
        self, mock_modify_groups_file, mock_read_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True
        crud = CRUD()
        self.assertFalse(crud.remove_group_member("1", "invalid_name"))

    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_remove_group_member_Passes_correct_value_to_modify_groups_file(
        self, mock_modify_groups_file, mock_read_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data
        mock_modify_groups_file.return_value = True
        crud = CRUD()
        expected_group_value = {
            "1": {  
                "name": "default",
                "Trust": 50,
                "List_of_members": ["mark@mail.com"]
            },
            "2": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"]
            }
        }
        crud.remove_group_member("1", "alex@gmail.com")
        self.assertEqual(self.groups_data, expected_group_value)
        mock_modify_groups_file.assert_called_once_with(self.groups_data)


# if __name__ == "__main__":

#     unittest.main()
