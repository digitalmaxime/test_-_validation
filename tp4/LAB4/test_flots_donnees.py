from crud import CRUD
crud = CRUD()

def calculate_trust_user(index):
    index = "{}".format(index)
    Date_of_last_seen_message = crud.get_user_data(index,"Date_of_last_seen_message")
    Date_of_first_seen_message = crud.get_user_data(index,"Date_of_first_seen_message")
    HamN = crud.get_user_data(index,"HamN")
    SpamN = crud.get_user_data(index,"Spamn")

    Trust1 = Date_of_last_seen_message/Date_of_first_seen_message * HamN/(HamN + SpamN)

    List_of_groups = crud.get_user_data(index,"Groups")
    Counter_of_groups = 0
    Total_trust = 0

    for e in List_of_groups:
        Counter_of_groups += 1
        group_id = crud.get_group_id(e)
        Total_trust += crud.get_group_data(group_id, "Trust")

    Trust2 = Total_trust / Counter_of_groups

    Trust = (Trust1 + Trust2)/2

    if Trust2 < 50:
        Trust = Trust2

    if Trust1 > 100:
        Trust = 100

    assert (Trust>=0 and Trust<=100),"error message"

    return Trust 

print(calculate_trust_user(1))
