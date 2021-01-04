from crud import CRUD
import unittest
from unittest.mock import patch

class TestCrudMadum(unittest.TestCase):
    def setUp(self):
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_users_file
        self.users_data = {
            "1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }
        }



    def tearDown(self):
        pass


    #test du rapporteur et du constructeur d1
    def test_crud_read_users_file(self) :        
        crud = CRUD()
        self.assertEqual({}, crud.read_users_file())
        self.assertEqual({}, crud.read_groups_file())
        self.assertEqual(1, crud.group_counter)
        self.assertEqual(1, crud.user_counter)
        self.assertEqual([], crud.removed_users_ids)

    #test des transformateurs add_new_user remove_user_group update_users remove_user
    #d2
    def test_add_rmug_update_rmu(self) :
        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "default") 
        self.assertEqual({"1": {
                "name": "default",
                "Trust": 100,
                "List_of_members": []
            }}, crud.read_groups_file())
        crud.update_users("1", "name", "user1alt@email")
        crud.remove_user("1")
        self.assertEqual({}, crud.read_users_file())
            
        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "default") 
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-14")
        crud.remove_user("1")
        self.assertEqual({}, crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "default") 
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-16")
        crud.remove_user("1")
        self.assertEqual({}, crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "default") 
        crud.update_users("1", "Groups", "amis")
        crud.remove_user("1")
        self.assertEqual({}, crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "default") 
        crud.update_users("1", "Groups", "default")
        crud.remove_user("1")
        self.assertEqual({}, crud.read_users_file())

    #d3
    def test_add_rmug_rmu_update(self) :
        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "default") 
        crud.remove_user("1")
        crud.update_users("1", "name", "user1alt@email")
        self.assertEqual({},crud.read_users_file())
        
        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "default") 
        crud.remove_user("1")
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-14")
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "default") 
        crud.remove_user("1")
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-16")
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "default") 
        crud.remove_user("1")
        crud.update_users("1", "Groups", "amis")
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "default") 
        crud.remove_user("1")
        crud.update_users("1", "Groups", "default")
        self.assertEqual({},crud.read_users_file())

    
    #d4
    def test_add_update_rmu_rmug(self) :
        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "name", "user1alt@email")
        crud.remove_user("1")
        crud.remove_user_group("1", "default") #ne fait rien
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-14")
        crud.remove_user("1")
        crud.remove_user_group("1", "default") #ne fait rien
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-16")
        crud.remove_user("1")
        crud.remove_user_group("1", "default") #ne fait rien
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "Groups", "amis")
        crud.remove_user("1")
        crud.remove_user_group("1", "default") #ne fait rien
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "Groups", "default")
        crud.remove_user("1")
        crud.remove_user_group("1", "default") #ne fait rien
        self.assertEqual({},crud.read_users_file())

    #d5
    def test_add_update_rmug_rmu(self) :
        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "name", "user1alt@email")
        crud.remove_user_group("1", "default")
        crud.remove_user("1")
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-14")
        crud.remove_user_group("1", "default")
        crud.remove_user("1")
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-16")
        crud.remove_user_group("1", "default")
        crud.remove_user("1")
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "Groups", "amis")
        crud.remove_user_group("1", "default")
        crud.remove_user("1")
        self.assertEqual({},crud.read_users_file())

    #d6
    def test_add_rmu_rmug_update(self) :
        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1")
        crud.remove_user_group("1", "default")      #ne fait rien
        crud.update_users("1", "name", "user1alt@email") #ne fait rien
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1")
        crud.remove_user_group("1", "default")      #ne fait rien
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-14")
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1")
        crud.remove_user_group("1", "default")      #ne fait rien
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-16")
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1")
        crud.remove_user_group("1", "default")      #ne fait rien
        crud.update_users("1", "Groups", "amis")
        self.assertEqual({},crud.read_users_file())


    #d7
    def test_add_rmu_update_rmug(self) :
        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1")
        crud.update_users("1", "name", "user1alt@email")    #ne fait rien 
        crud.remove_user_group("1", "default")              #ne fait rien
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1")
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-14")
        crud.remove_user_group("1", "default")              #ne fait rien
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1")
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-16")
        crud.remove_user_group("1", "default")              #ne fait rien
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1")
        crud.update_users("1", "Groups", "amis")
        crud.remove_user_group("1", "default")              #ne fait rien
        self.assertEqual({},crud.read_users_file())

    #d8
    def test_rmu_update_rmug_add(self) :
        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien
        crud.update_users("1", "name", "user1alt@email")    #ne fait rien
        crud.remove_user_group("1", "default")              #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())

        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-14")
        crud.remove_user_group("1", "default")              #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())

        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-16")
        crud.remove_user_group("1", "default")              #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())

        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien
        crud.update_users("1", "Groups", "amis")
        crud.remove_user_group("1", "default")              #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())

        #Debut des validations
        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien
        crud.update_users("1", "Groups", "amis")
        crud.remove_user_group("1", "default")              #ne fait rien
        crud.add_new_user("user1email", "2020-11-15")
        self.assertEqual({},crud.read_users_file())

        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien
        crud.update_users("1", "Groups", "amis")
        crud.remove_user_group("1", "default")              #ne fait rien
        crud.add_new_user("user@1email", "2020-15-0")
        self.assertEqual({},crud.read_users_file())

    #d9
    def test_rmu_update_add_rmug(self) :
        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien
        crud.update_users("1", "name", "user1alt@email")    #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "default")
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": []
            }},crud.read_users_file())
    #d10
    def test_rmu_add_rmug_update(self) :
        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien    
        crud.add_new_user("user1@email", "2020-11-15")  
        crud.remove_user_group("1", "default")
        crud.update_users("1", "name", "user1alt@email")
        self.assertEqual({"1": {
                "name": "user1alt@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": []
            }},crud.read_users_file())

        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien    
        crud.add_new_user("user1@email", "2020-11-15")  
        crud.remove_user_group("1", "default")
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-14")
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605312000.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": []
            }},crud.read_users_file())

        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien    
        crud.add_new_user("user1@email", "2020-11-15")  
        crud.remove_user_group("1", "default")
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-16")
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605484800.0,
                "Groups": []
            }},crud.read_users_file())

        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien    
        crud.add_new_user("user1@email", "2020-11-15")  
        crud.remove_user_group("1", "default")
        crud.update_users("1", "Groups", "amis")
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": []
            }},crud.read_users_file())

        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien    
        crud.add_new_user("user1@email", "2020-11-15")  
        crud.remove_user_group("1", "default")
        crud.update_users("1", "Groups", "default") 
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())


    #d11
    def test_rmu_add_update_rmug(self) :
        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien    
        crud.add_new_user("user1@email", "2020-11-15") 
        crud.update_users("1", "name", "user1alt@email")  
        crud.remove_user_group("1", "default")
        self.assertEqual({"1": {
                "name": "user1alt@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": []
            }},crud.read_users_file())

        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien    
        crud.add_new_user("user1@email", "2020-11-15") 
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-14")
        crud.remove_user_group("1", "default")
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605312000.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": []
            }},crud.read_users_file())

        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien    
        crud.add_new_user("user1@email", "2020-11-15") 
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-16")
        crud.remove_user_group("1", "default")
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605484800.0,
                "Groups": []
            }},crud.read_users_file())

        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien    
        crud.add_new_user("user1@email", "2020-11-15") 
        crud.update_users("1", "Groups", "amis")
        crud.remove_user_group("1", "default")
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": []
            }},crud.read_users_file())
        

    #d12
    def test_rmu_rmug_add_update(self) :
        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien
        crud.remove_user_group("1", "default")              #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15") 
        crud.update_users("1", "name", "user1alt@email")
        self.assertEqual({"1": {
                "name": "user1alt@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())

        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien
        crud.remove_user_group("1", "default")              #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15") 
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-14")
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605312000.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())

        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien
        crud.remove_user_group("1", "default")              #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15") 
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-16")
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605484800.0,
                "Groups": ["default"]
            }},crud.read_users_file())

        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien
        crud.remove_user_group("1", "default")              #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15") 
        crud.update_users("1", "Groups", "amis")
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())

        #debut des validations
        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien
        crud.remove_user_group("1", "default")              #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15") 
        with self.assertRaises(AssertionError):
            crud.update_users("1", "invalid_field", "amis")

        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())


    #d13
    def test_rmu_rmug_update_add(self) :
        crud = CRUD()
        crud.remove_user("1")                               #ne fait rien
        crud.remove_user_group("1", "default")              #ne fait rien
        crud.update_users("1", "name", "user1alt@email")    #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())


    #d14 
    def test_update_rmu_rmug_add(self) :
        crud = CRUD()
        crud.update_users("1", "name", "user1alt@email")    #ne fait rien
        crud.remove_user("1")
        crud.remove_user_group("1", "default")              #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")  
        self.assertEqual({"1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())

    #d15
    def test_update_rmu_add_rmug(self) :
        crud = CRUD()
        crud.update_users("1", "name", "user1alt@email") #ne fait rien
        crud.remove_user("1") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "default") 
        self.assertEqual({
            "1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": []

            }},crud.read_users_file())

        crud = CRUD()
        crud.update_users("1", "name", "user1alt@email") #ne fait rien
        crud.remove_user("1") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "amis") 
        self.assertEqual({
            "1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]

            }},crud.read_users_file())
        crud = CRUD()
        crud.update_users("1", "name", "user1alt@email") #ne fait rien
        crud.remove_user("1") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1234", "default") 
        self.assertEqual({
            "1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]

            }},crud.read_users_file())

    #d16
    def test_update_add_rmug_rmu(self) :
        crud = CRUD()
        crud.update_users("1", "name", "user1alt@email") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "default") 
        crud.remove_user("1")
        self.assertEqual({}, crud.read_users_file())


        crud = CRUD()
        crud.update_users("1", "name", "user1alt@email") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "default") 
        crud.remove_user("1234")
        self.assertEqual({
            "1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": []
            }},crud.read_users_file())

        crud = CRUD()
        crud.update_users("1", "name", "user1alt@email") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "amis") 
        crud.remove_user("1")
        self.assertEqual({}, crud.read_users_file())

        crud = CRUD()
        crud.update_users("1", "name", "user1alt@email") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user_group("1", "amis") 
        crud.remove_user("1234")
        self.assertEqual({
            "1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())


    #d17
    def test_update_add_rmu_rmug(self) :
        crud = CRUD()
        crud.update_users("1", "name", "user1alt@email") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1")
        crud.remove_user_group("1", "default") 
        self.assertEqual({}, crud.read_users_file())

        crud = CRUD()
        crud.update_users("1", "name", "user1alt@email") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1")
        crud.remove_user_group("1", "amis") 
        self.assertEqual({}, crud.read_users_file())

        crud = CRUD()
        crud.update_users("1", "name", "user1alt@email") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1234")
        crud.remove_user_group("1", "default") 
        self.assertEqual({
            "1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": []
            }},crud.read_users_file())
        
        crud = CRUD()
        crud.update_users("1", "name", "user1alt@email") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1234")
        crud.remove_user_group("1", "amis") 
        self.assertEqual({
            "1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())

    #d18
    def test_update__rmug_add_rmu(self) :
        crud = CRUD()
        crud.update_users("1", "name", "user1alt@email") #ne fait rien
        crud.remove_user_group("1", "default") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1")
        self.assertEqual({}, crud.read_users_file())

        crud = CRUD()
        crud.update_users("1", "name", "user1alt@email") #ne fait rien
        crud.remove_user_group("1", "default") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1234")
        self.assertEqual({
            "1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())

    #d19 
    def test_update_rmug_rmu_add(self) :
        crud = CRUD()
        crud.update_users("1", "name", "user1alt@email") #ne fait rien 
        crud.remove_user_group("1", "default") #ne fait rien
        crud.remove_user("1") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        self.assertEqual(self.users_data, crud.read_users_file())
    
    #d20
    def test_rmug_add_update_rmu(self) :
        crud = CRUD()
        crud.remove_user_group("1", "default") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "name", "user1alt@email")  
        crud.remove_user("1") 
        self.assertEqual({}, crud.read_users_file())

        crud = CRUD()
        crud.remove_user_group("1", "default") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-14")
        crud.remove_user("1") 
        self.assertEqual({}, crud.read_users_file())

        crud = CRUD()
        crud.remove_user_group("1", "default") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-14")
        crud.remove_user("1234") 
        self.assertEqual({
            "1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605312000.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())

        crud = CRUD()
        crud.remove_user_group("1", "default") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-16")
        crud.remove_user("1") 
        self.assertEqual({}, crud.read_users_file())

        crud = CRUD()
        crud.remove_user_group("1", "default") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "Date_of_last_seen_message", "2020-11-16")
        crud.remove_user("1234") 
        self.assertEqual({
            "1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605484800.0,
                "Groups": ["default"]
            }},crud.read_users_file())

        crud = CRUD()
        crud.remove_user_group("1", "default") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "Groups", "amis")
        crud.remove_user("1") 
        self.assertEqual({}, crud.read_users_file())

        crud = CRUD()
        crud.remove_user_group("1", "default") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "Groups", "amis")
        crud.remove_user("1234") 
        self.assertEqual({
            "1": {
                "name": "user1@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())

    #d21
    def test_rmug_add_rmu_update(self) :
        crud = CRUD()
        crud.remove_user_group("1", "default") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1") 
        crud.update_users("1", "name", "user1alt@email")
        self.assertEqual({}, crud.read_users_file())

        crud = CRUD()
        crud.remove_user_group("1", "default") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1") 
        crud.update_users("1", "Groups", "user1alt@email")
        self.assertEqual({}, crud.read_users_file())

        crud = CRUD()
        crud.remove_user_group("1", "default") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1234") 
        crud.update_users("1", "name", "user1alt@email")
        self.assertEqual({
            "1": {
                "name": "user1alt@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]
            }},crud.read_users_file())    
    #d22
    def test_rmug_update_add_rmu(self) :
        crud = CRUD()
        crud.remove_user_group("1", "default") #ne fait rien
        crud.update_users("1", "name", "user1alt@email") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.remove_user("1") 
        self.assertEqual({}, crud.read_users_file())

    #d23
    def test_rmug_update_rmu_add(self) :
        crud = CRUD()
        crud.remove_user_group("1", "default") #ne fait rien
        crud.update_users("1", "name", "user1alt@email") #ne fait rien
        crud.remove_user("1") 
        crud.add_new_user("user1@email", "2020-11-15")
        self.assertEqual(self.users_data, crud.read_users_file())

    #d24
    def test_rmug_rmu_add_update(self) :
        crud = CRUD()
        crud.remove_user_group("1", "default") #ne fait rien
        crud.remove_user("1") #ne fait rien
        crud.add_new_user("user1@email", "2020-11-15")
        crud.update_users("1", "name", "user1alt@email")
        self.assertEqual({
            "1": {
                "name": "user1alt@email",
                "Trust": 100,
                "Spamn": 0,
                "HamN": 0,
                "Date_of_first_seen_message": 1605398400.0,
                "Date_of_last_seen_message": 1605398400.0,
                "Groups": ["default"]

            }}, crud.read_users_file())

    #d25
    def test_rmug_rmu_update_add(self) :
        crud = CRUD()
        crud.remove_user_group("1", "default") #ne fait rien
        crud.remove_user("1") #ne fait rien
        crud.update_users("1", "name", "user1alt@email") #ne fait rien 
        crud.add_new_user("user1@email", "2020-11-15")
        self.assertEqual(self.users_data, crud.read_users_file())

    