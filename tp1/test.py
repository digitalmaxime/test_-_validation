import json
from vocabulary_creator import VocabularyCreator
from renege import RENEGE
from email_analyzer import EmailAnalyzer
from crud import CRUD
from vocabulary_creator import



crud1 = CRUD()

crud1.add_new_user("max@email", "1988-12-03")
crud1.add_new_user("maude@email","1990-11-23")
crud1.add_new_user("monique@email","1990-11-23")
crud1.add_new_group("groupe_des_gentils",100 ,["max@email", "maude@email"])
#crud1.add_new_group("groupe_des_mechants",100 ,["moi@gmail234"])

#crud1.update_users("1", "name", "new")
crud1.update_users("1", "Date_of_last_seen_message", "2020-12-13")

crud1.update_groups("2", "name", "nouveau_nom_groupe")

#crud1.remove_group("2")
crud1.update_groups("2", "List_of_members","monique@email")

crud1.remove_group_member("2", "max@email")












#crud1.update_groups("2", "List_of_members", "nouveau")

#crud1.remove_user("1")

#crud1.remove_user_group("2", "default")

#crud1.remove_group("1")