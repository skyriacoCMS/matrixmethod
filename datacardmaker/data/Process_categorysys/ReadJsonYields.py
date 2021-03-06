import json



def ReadJsonweights(year_,category_,decaymode_,process_):
        scale = -1
        with open("./data/yields.json") as fjson:
                weights = json.load(fjson)

                if "ff" in process_:
                        process_ = process_.split('_')[0]
                scale = weights["190821_"+year_]["fa3fa2fL1fL1Zg_morecategories"][category_][decaymode_][process_]
        return scale

def ReadJsonsystematics(year_,decaymode_):
        scale = -1
        with open("./categorysystematics.json") as fjson:
                systms = json.load(fjson)
                scale = -1

                for uncert_ in systms["190821_"+year_]:
                        for category_ in systms["190821_"+year_][uncert_]["fa3fa2fL1fL1Zg_morecategories"] :
                                print uncert_, category_
                                
                                        
                                passs  = False
                                for proc in systms["190821_"+year_][uncert_]["fa3fa2fL1fL1Zg_morecategories"][category_][decaymode_] :
                                                        
                                        scale = systms["190821_"+year_][uncert_]["fa3fa2fL1fL1Zg_morecategories"][category_][decaymode_][proc]
                                        if scale is not None :
                                                passs =  True
                                        

                                if passs:                 
                                        with open("sys_"+str(category_)+"_"+str(decaymode_)+"_"+str(year_)+".txt","a") as file:
                                                file.write(uncert_+"\n")


                                
                #if uncert_ in systms["190821_"+year_]:                        
                #        if category_ in systms["190821_"+year_][uncert_]["fa3fa2fL1fL1Zg_morecategories"] :
                #                if process_ in systms["190821_"+year_][uncert_]["fa3fa2fL1fL1Zg_morecategories"][category_][decaymode_]: 
                #                        scale =systms["190821_"+year_][uncert_]["fa3fa2fL1fL1Zg_morecategories"][category_][decaymode_][process_] 
        return scale


if __name__ == "__main__":


        res = ReadJsonsystematics("2018","2e2mu")
        res = ReadJsonsystematics("2018","4mu")
        res = ReadJsonsystematics("2018","4e")


        res = ReadJsonsystematics("2017","2e2mu")
        res = ReadJsonsystematics("2017","4mu")
        res = ReadJsonsystematics("2017","4e")


        res = ReadJsonsystematics("2016","2e2mu")
        res = ReadJsonsystematics("2016","4mu")
        res = ReadJsonsystematics("2016","4e")

        print res
        
        
#def MakeUncertFields(uncert_,year_,category_,decaymode_,process_)
