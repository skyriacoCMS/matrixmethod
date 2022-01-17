import json



def ReadJsonweights(year_,category_,decaymode_,process_):
        scale = -1
        with open("./data/yields.json") as fjson:
                weights = json.load(fjson)

                if "ff" in process_:
                        process_ = process_.split('_')[0]
                scale = weights["200205_"+year_]["fa3fa2fL1fL1Zg_morecategories"][category_][decaymode_][process_]
        return scale

def ReadJsonsystematics(uncert_,year_,category_,decaymode_,process_):
        scale = -1
        with open("./data/categorysystematics.json") as fjson:
                systms = json.load(fjson)
                scale = -1
                
                if uncert_ in systms["200205_"+year_]:                        
                        if category_ in systms["200205_"+year_][uncert_]["fa3fa2fL1fL1Zg_morecategories"] :
                                if process_ in systms["200205_"+year_][uncert_]["fa3fa2fL1fL1Zg_morecategories"][category_][decaymode_]: 
                                        scale =systms["200205_"+year_][uncert_]["fa3fa2fL1fL1Zg_morecategories"][category_][decaymode_][process_] 
        return scale


if __name__ == "__main__":


        res = ReadJsonsystematics("CMS_btag_comb","2018","VBFtagged","4mu","VBF")
        print res
        
#def MakeUncertFields(uncert_,year_,category_,decaymode_,process_)
