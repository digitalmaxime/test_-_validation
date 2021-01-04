import json


class CRUD:
    """
    Classe pour realiser la fonctionalite CRUD.
    """

    def __init__(self):
        self.users_file = "users.json"
        self.groups_file = "groups.json"

    ##*************CREATE**************

    def add_new_user(self, user_email, date):
        '''
        Description: fonction pour ajouter un nouvel utilisateur 
        dans le fichier 'users.json', selon le format donné dans 
        la description du lab
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''

        raise NotImplementedError("")

    def add_new_group(self, name, trust, members_list):
        '''
        Description: fonction pour ajouter une grouppe  
        dans le fichier 'groups.json', selon le format donne dans 
        la description du lab
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        raise NotImplementedError("")

    ###***********READ****************
    def read_users_file(self):
        '''
        fonction deja implemente
        Description: fonction qui lit le fichier 'users.json'
        et retourne le dictionaire
        Sortie: dictionare avec les utilisateurs 
        '''
        with open(self.users_file) as users_file:
            return json.load(users_file)

    def read_groups_file(self):
        '''
        fonction deja implemente
        Description: fonction qui lit le fichier 'users.json'
        et retourne le dictionaire
        Sortie: dictionare avec les groupes
        '''
        with open(self.groups_file) as group_file:
            return json.load(group_file)

    def get_user_data(self, user_id, field):
        '''
        Description: fonction qui sorte la valeur d'information specifie
        pour une utilisateur specifie.
        Par example, spam_number = get_user_data(2, "SpamN") va donner le
        numero de messages spam pour utilisateur avec id 2.
        Sortie: la valeur d'information specifie pour utilisateur
        '''
        raise NotImplementedError("")

    def get_group_data(self, group_id, field):
        '''
        Description: fonction qui sorte la valeur d'information specifie
        pour une grouppe specifie.
        Par example, group_trust_level = get_group_data(2, "Trust") va donner la
        valeur de "Trust" pour grouppe avec id 2.
        Sortie: la valeur d'information specifie pour le grouppe
        '''

        raise NotImplementedError("")

    def get_user_id(self, name):
        '''
        Description: fonction sorte l'id d'utilisateur, donne le nom (email d'utilisater)
        Sortie: la valeur d'id d'utilisateur
        '''
        raise NotImplementedError("")

    def get_group_id(self, name):
        '''
        Description: fonction sorte l'id de grouppe, donne le nom de grouppe
        Sortie: la valeur d'id de grouppe
        '''

        raise NotImplementedError("")

    ##*******UPDATE******************

    def modify_users_file(self, data):
        '''
        Description: fonction qui ecrit le dictionnaire
        d'utilisateurs dans le fichiers 'users.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        with open(self.users_file, "w") as outfile:
            json.dump(data, outfile)
        return True

    def modify_groups_file(self, data):
        '''
        Description: fonction qui ecrit le dictionnaire
        des grouppes dans le fichiers 'groups.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        with open(self.groups_file, "w") as outfile:
            json.dump(data, outfile)
        return True

    def update_users(self, user_id, field, data):
        '''
        Description: fonction qui modifie les donnes d'utilisateur
        Par example, update_users(3, "Trust", 60) va changer le valeur de "Trust"
        pour utilisateur avec id 3 au 60.
        update_users(3, "Groups", "friends") va ajouter le grouppe 'friends'
        pour utilisater avec id 3.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        raise NotImplementedError("")

    def update_groups(self, group_id, field, data):
        '''
        Description: fonction qui modifie les donnes du groupe
        Par example, update_groups(2, "Trust", 30) va changer le valeur de "Trust"
        pour le grouppe avec id 2 au 30.
        update_groups(3, "List_of_members", "test@mail.com") va ajouter l'utilisateur
        avec email test@mail.com dans le liste des membres de groupe
        avec id 3.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        raise NotImplementedError("")

    ##***********DELETE***********************

    def remove_user(self, user_id):
        '''
        Description: fonction qui suprime l'utilisateur de fichier 'users.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        raise NotImplementedError("")

    def remove_user_group(self, user_id, group_name):
        '''
        Description: fonction qui suprime de le fichier 'users.json' le groupe 
        auquel appartient un utilisateur.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        raise NotImplementedError("")

    def remove_group(self, group_id):
        '''
        Description: fonction qui suprime le groupe de fichier 'groups.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        raise NotImplementedError("")

    def remove_group_member(self, group_id, member):
        '''
        Description: fonction qui enleve le membre de le liste des membres pour
        un groupe dans le 'groups.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        raise NotImplementedError("")
