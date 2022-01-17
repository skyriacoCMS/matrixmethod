import os


year=["2016","2017","2018"]
category = ["Untagged","Boosted","VBFtagged","VBF1jtagged","VHHadrtagged","VHLepttagged"]
decay=["2e2mu","4mu","4e"]

for y in year:
    for cat in category:
        for dec in decay:
            cmnd = "cp "+cat+".txt sys_"+cat+"_"+dec+"_"+y+".txt"
            os.system(cmnd)

