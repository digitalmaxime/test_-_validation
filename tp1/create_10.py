import json

with open("1000-mails.json","r") as file:
    thousand = json.load(file)

with open("10-mails.json","w") as file:
    smaller_dic = thousand["dataset"][:10]
    json.dump(smaller_dic,file, indent = 2)

