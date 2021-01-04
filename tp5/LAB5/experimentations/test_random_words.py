import random
import json

mots = "La vie est belle"
mots = mots.split()
print(mots)
random.shuffle(mots)
print(mots)
mots = " ".join(mots)
print(mots)

# with open("test300copy.json") as users_file:
#     test300 = json.load(users_file)

# for mail in test300["dataset"] :
#     subject = mail["mail"]["Subject"]
#     subject = subject.split()
#     random.shuffle(subject)
#     subject = " ".join(subject)
#     mail["mail"]["Subject"] = subject
#     body= mail["mail"]["Body"]
#     body = body.split()
#     random.shuffle(body)
#     body = " ".join(body)
#     mail["mail"]["Body"] = body    

# with open("test300copy.json", "w") as outfile:
#     json.dump(test300, outfile, indent=4)
