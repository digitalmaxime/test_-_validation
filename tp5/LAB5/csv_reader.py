import csv

def read_csv(file_name) :

    param_dict = dict()

    with open('../ACTS3.0/{}'.format(file_name)) as csvfile:
        readCSV = csv.reader(csvfile) #delimiter=','
        line_count = 0
        for row in readCSV:
            if row[0][0] == "#" :
                pass
            else :
                if line_count == 0:
                    pass # implemente something for the cols maybe, or print
                else : 
                    param_dict[line_count] = row
                line_count += 1
        return param_dict


def write_csv(dictionnaire):

    with open("results.csv","w") as csv_file:
        fieldTitles = ["use_log","combinaison_log", "vocab_counter_treshold", "cleaning_mode","calcul_mode","accuracy","precision","recall","moyenne"]
        objDictWriter = csv.DictWriter(csv_file, fieldnames=fieldTitles)
        objDictWriter.writeheader()
        for e in dictionnaire:
            objDictWriter.writerow({"use_log":dictionnaire[e][0],"combinaison_log":dictionnaire[e][1], "vocab_counter_treshold":dictionnaire[e][2],"cleaning_mode":dictionnaire[e][3],"calcul_mode":dictionnaire[e][4],"accuracy":dictionnaire[e][5],"precision":dictionnaire[e][6],"recall":dictionnaire[e][7],"moyenne":dictionnaire[e][8]})

