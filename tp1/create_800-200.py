import json

with open("1000-mails.json","r") as file:
    thousand = json.load(file)

with open("800-mails.json","w") as file:
    new_dict = {"dataset": None}
    new_dict["dataset"] = thousand["dataset"][:800]
    json.dump(new_dict,file, indent = 2)

with open("200-mails.json","w") as file:
    new_dict = {"dataset": None}
    new_dict["dataset"] = thousand["dataset"][801:]
    json.dump(new_dict,file, indent = 2) 