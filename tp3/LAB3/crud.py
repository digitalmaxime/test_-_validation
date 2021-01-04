import json
from datetime import datetime
from datetime import timezone

class CRUD:
    """
    Classe pour realiser la fonctionalite CRUD.
    """

    def __init__(self):
        self.users_file = "users.json"
        self.groups_file = "groups.json"        
        data_users = self.read_users_file()
        self.user_counter = len(data_users) +1
        data_groups = self.read_groups_file()
        self.group_counter = len(data_groups) +1


    ##*************INIT EMPTY FILES**************
    def clean_files(self): #pragma: no cover
        # assurer que users.json est vide
        self.modify_users_file(dict())

        # assurer que groups.json est vide
        self.modify_groups_file(dict())
        self.group_counter = 1
        self.user_counter = 1


    ##*************CREATE**************
    def add_new_user(self, user_email, date):
        '''
        Description: fonction pour ajouter un nouvel utilisateur 
        dans le fichier 'users.json', selon le format donné dans 
        la description du lab
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        #validation du e-mail
        if "@" not in user_email:
            return False                

        #validation de la date
        year = int(date[0:4])
        month = int(date[5:7])
        day = int(date[8:10])
        if len(date) != 10:
            return False
        
        #ajouter l'utilisateur au groupe par default et creer le groupe s'il n'existe pas
        if self.user_counter == 1:    #pragma: no cover
            data = \
                {
                    "{}".format(self.group_counter): {
                        "name": "default",
                        "Trust": 100,
                        "List_of_members": [user_email]
                    }                    
                }
            self.modify_groups_file(data)
            self.group_counter += 1

        else:
            groups = self.read_groups_file()
            if user_email not in groups["1"]["List_of_members"]:
                groups["1"]["List_of_members"].append(user_email)
                self.modify_groups_file(groups)
        
        #Traitement de la date
        dt = datetime(year, month, day)
        date = dt.replace(tzinfo=timezone.utc).timestamp()

        #lire les donnees des users deja existants
        users_data = self.read_users_file()

        #verifier si user est deja la
        for user in users_data.values():
            if user["name"] == user_email:
                return False

        #rajouter l'information de l'utilisateur au fichier users.json
        data = \
            {
                "name": user_email,
                "Trust":100, 
                "Spamn":0, 
                "HamN":0,
                "Date_of_first_seen_message":date,
                "Date_of_last_seen_message":date,
                "Groups": ["default"]
            }
        
        
        users_data["{}".format(self.user_counter)] = data
        self.modify_users_file(users_data)
        self.user_counter += 1
        
        return True


    def add_new_group(self, name, trust, members_list):
        '''
        Description: fonction pour ajouter une grouppe  
        dans le fichier 'groups.json', selon le format donne dans 
        la description du lab
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''

        #verification que les membres des utilisateurs font partie de users.json
        #on doit cree les utilisateurs en premier
        for member in members_list:
            if self.get_user_id(member) == None: 
                return False

        groups_data = self.read_groups_file()

        #initialisation du groupe.json si il est vide
        if len(groups_data) == 0 and name != "default" :
            initial_data = \
            {
                "name": "default",
                "Trust": 50,
                "List_of_members": []
            }  
            groups_data["1"] = initial_data
            self.group_counter += 1
            self.modify_groups_file(groups_data)

        # verifie si groupe est deja la  
        for group in groups_data.values():
            if group["name"] == name: #group already there
                return False

        #insertion de la nouvelle information dans groups.json
        data = \
            {
                "name": name,
                "Trust": trust,
                "List_of_members": members_list
            }                    

        groups_data["{}".format(self.group_counter)] = data
        self.modify_groups_file(groups_data)
        
        #Parcourir le members_list pour appeler update_user() et leur ajouter le nouveau groupe
        for mem in members_list:
            id = self.get_user_id(mem)
            self.update_users(id, "Groups", name)
        
        self.group_counter += 1
        return True


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
        try:
            users = self.read_users_file()
            return users[user_id][field]
        except KeyError as key_error:
            raise key_error
        
        except:
            raise


    def get_group_data(self, group_id, field):
        '''
        Description: fonction qui sorte la valeur d'information specifie
        pour une grouppe specifie.
        Par example, group_trust_level = get_group_data(2, "Trust") va donner la
        valeur de "Trust" pour grouppe avec id 2.
        Sortie: la valeur d'information specifie pour le grouppe
        '''
        #Verification du group_id
        groups = self.read_groups_file()
        if group_id not in groups.keys():
            return False
        
        #Verification du field
        if field not in groups[group_id]:
            return False

        return groups[group_id][field]


    def get_user_id(self, name):
        '''
        Description: fonction sorte l'id d'utilisateur, donne le nom (email d'utilisater)
        Sortie: la valeur d'id d'utilisateur
        '''
        users = self.read_users_file()

        for user_key, user_data in users.items():
            if user_data["name"] == name:
                return user_key
        return None  
        #Si l'utilisateur ne fait pas partie de users.json   


    def get_group_id(self, name):
        '''
        Description: fonction sorte l'id de grouppe, donne le nom de grouppe
        Sortie: la valeur d'id de grouppe
        '''
        groups = self.read_groups_file()
        for group_key, group_data in groups.items():
            if group_data["name"] == name:
                return group_key
        return False


    ##*******UPDATE***************

    def modify_users_file(self, data):  #pragma: no cover
        '''
        Description: fonction qui ecrit le dictionnaire
        d'utilisateurs dans le fichiers 'users.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        with open(self.users_file, "w") as outfile:
            json.dump(data, outfile, indent = 4)
        return True


    def modify_groups_file(self, data): #pragma: no cover
        '''
        Description: fonction qui ecrit le dictionnaire
        des grouppes dans le fichiers 'groups.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        with open(self.groups_file, "w") as outfile:
            json.dump(data, outfile, indent = 4)
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
        users = self.read_users_file()
        #Validation du user_id et field
        if user_id not in users:
            return False
        if field not in users[user_id]:
            return False
        
        #Traitement et validation de la date
        if field == "Date_of_last_seen_message":
            if len(data) != 10:                         
                return False
            year = int(data[0:4])
            month = int(data[5:7])
            day = int(data[8:10])
            dt = datetime(year, month, day)
            data = dt.replace(tzinfo=timezone.utc).timestamp()

        #Traitement et verification du groupe
        if field == "Groups":
            if data not in users[user_id][field]:
                users[user_id][field].append(data)

        else:
            users[user_id][field] = data
        
        self.modify_users_file(users)
        return True


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
        #Verification de field
        if field not in ["name", "Trust", "List_of_members"]:
            return False
        
        #Verification du group_id
        groups = self.read_groups_file()
        if group_id not in groups:
            return False

        #Changer la liste de membre du groupe
        if field == "List_of_members":
            groups[group_id][field].append(data) 
            #ajouter le groupe au membre
            user_id = self.get_user_id(data)
            self.update_users(user_id, "Groups", groups[group_id]["name"])

        # pour changer nom
        elif field == "name":
            previousGroup = groups[group_id][field]
            groups[group_id][field] = data
            for mem in groups[group_id]["List_of_members"]:
                id = self.get_user_id(mem)
                self.update_users(id, "Groups", data)
                self.remove_user_group(id,previousGroup)  
        
        else:
            groups[group_id][field] = data
        self.modify_groups_file(groups)
        
        return True

    ##***********DELETE***********************

    def remove_user(self, user_id):
        '''
        Description: fonction qui suprime l'utilisateur de fichier 'users.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        
        #Verification user_id
        users = self.read_users_file()
        if user_id not in users:
            return False

        #enlever le nom du membre de chacun des groupes auquel il fait partie
        groups = self.read_groups_file()
        group_list = self.get_user_data(user_id, "Groups")
        user_name = self.get_user_data(user_id, "name")
        for group in group_list:
            group_id = self.get_group_id(group)
            groups[group_id]["List_of_members"].remove(user_name)
        self.modify_groups_file(groups)

        #supprimer l'utilisateur de users.json
        del users[user_id]
        self.modify_users_file(users)
        
        return True


    def remove_user_group(self, user_id, group_name):
        
        #remove from user a group
        '''
        Description: fonction qui suprime dans le fichier 'users.json' le groupe 
        auquel appartient un utilisateur.
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        #Verification user_id et group_name existent
        users = self.read_users_file()

        if user_id not in users:
            return False

        if group_name not in users[user_id]["Groups"]:
            return False

        users[user_id]["Groups"].remove(group_name)
        self.modify_users_file(users)

        #enlever le nom du membre du groupe auquel il fait partie
        user_name = self.get_user_data(user_id, "name")
        group_id = self.get_group_id(group_name)
        groups = self.read_groups_file()
        if user_name in groups[group_id]["List_of_members"]:
            groups[group_id]["List_of_members"].remove(user_name)
            self.modify_groups_file(groups)

        return True


    def remove_group(self, group_id):
        '''
        Description: fonction qui suprime le groupe de fichier 'groups.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        #restreindre la possibilite d'enlever le groupe par default (group_id : "1")
        if group_id == "1":
            return False

        #verifie si group_id dans le fichier groups.json
        groups = self.read_groups_file()
        
        if group_id not in groups:
            return False

        #enlever le groupe des membres dans users.json 
        for mem in groups[group_id]["List_of_members"]:
            user_id = self.get_user_id(mem)
            self.remove_user_group(user_id, groups[group_id]["name"])

        #enlever le groupe dans groups.json
        del groups[group_id]
        self.modify_groups_file(groups)

        return True


    def remove_group_member(self, group_id, member):
        '''
        Description: fonction qui enleve le membre de le liste des membres pour
        un groupe dans le 'groups.json'
        Sortie: bool, 'True' pour succes, 'False' dans le cas de failure.
        '''
        #Verification du group_id
        groups = self.read_groups_file()
        if group_id not in groups:
            return False
        
        #Verification que le membre appartient au groupe
        if member not in groups[group_id]["List_of_members"]:
            return False

        groups[group_id]["List_of_members"].remove(member)
        self.modify_groups_file(groups)

        #enleve le groupe de l'utilisateur
        id = self.get_user_id(member)
        self.remove_user_group(id,groups[group_id]["name"])

        return True
