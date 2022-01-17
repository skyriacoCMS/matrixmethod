import json
import sys
import ntpath
import EFTmodel1 as EFTmodel
from sample import Sample 


def jsonmaker_ggHttH(inputfile, type_):

      
    #with open('templates_ggh_fa3fa2fL1fL1Zg_morecategories_2e2mu_Untagged_190703_2018.json') as f:
     with open(inputfile) as f:
         data = json.load(f)



     #print("\n")
     ##print(data["constraints"])
     ##print(data["templates"][1]["binning"])
     #print("\n")

     ##print(data["constraints"])

     i = 0 
     itemp = -1
     added_String = ""
     for temp  in data["templates"] :
         #    #print( temp ," ", i)
         #print (temp["name"])
         name = temp["name"]
         itemp = itemp +1
         if "Mirror" in name and itemp == 0 :
              print "has mirror"
              added_String = "Mirror"

         
         sm = 0
         a2 = 0
         a4 = 0
         l1 = 0
         L1 = 0
         hff = 0
         
         if "Hff" in name:
             hff = 1
         if "0Plus" in name:
             sm = 1 
         if "0HPlus" in name:
             a2 = 1
         if ("0Minus" in name and not ( "Hff" in name )  ) or ("HVV0Minus" in name and ( "Hff" in name ) ) :
             a4 = 1
         if "0L1" in name:
             l1 = 1
             L1 = 1e4
             
         if "g11" in name:
             sm = 1
         if "g2" in name:
             a2 = 1
         if "g4" in name:
             a4 = 1
         if "g1prime2" in name:
             l1 = 1
             L1 = 1e4
             #call functions to calculate the couplings. 
         couplings = {
             "ghv1": sm,
             "ghz2": a2,
             "ghw2":EFTmodel.g2WW(a2,a4,L1),
             "ghz4": a4,
             "ghw4": EFTmodel.g4WW(a2,a4,L1),
             "ghz1prime2": L1,
             "ghw1prime2":EFTmodel.L1W(a2,a4,L1),
             "ghzgs1prime2": EFTmodel.L1Zgamma(a2,a4,L1),
         }


         ##print (data["templates"][i]["weight"])
         weightt =""
         if hff == 1 : 
              weightt =  Sample(type_,useHJJ=True,kappa=1,kappa_tilde=0, **couplings).weight
         else :
              weightt =  Sample(type_,useHJJ=True,kappa=0,kappa_tilde=1, **couplings).weight
         ##print (weightt)
         couplings = {
             "ghv1": sm,
             "ghz2": 0,
             "ghw2":EFTmodel.g2WW(0,0,0),
             "ghz4": 0,
             "ghw4": EFTmodel.g4WW(0,0,0),
             "ghz1prime2": 0,
             "ghw1prime2":EFTmodel.L1W(0,0,0),
             "ghzgs1prime2": EFTmodel.L1Zgamma(0,0,0),
         }
         smweight = ""
         if hff == 1 : 
              smweight =  Sample(type_,useHJJ=True,kappa=1,kappa_tilde=0, **couplings).weight
         else :
              smweight =  Sample(type_,useHJJ=True,kappa=0,kappa_tilde=1, **couplings).weight
       



         couplings = {
             "ghv1": 0,
             "ghz2": a2,
             "ghw2":EFTmodel.g2WW(a2,0,0),
             "ghz4": 0,
             "ghw4": EFTmodel.g4WW(a2,0,0),
             "ghz1prime2": 0,
             "ghw1prime2":EFTmodel.L1W(a2,0,0),
             "ghzgs1prime2": EFTmodel.L1Zgamma(a2,0,0),
         }
         a2weight =""
         if hff == 1 : 
              a2weight =  Sample(type_,useHJJ=True,kappa=1,kappa_tilde=0, **couplings).weight
         else :
              a2weight =  Sample(type_,useHJJ=True,kappa=0,kappa_tilde=1, **couplings).weight
       

         couplings = {
             "ghv1": 0,
             "ghz2": 0,
             "ghw2":EFTmodel.g2WW(0,a4,0),
             "ghz4": a4,
             "ghw4": EFTmodel.g4WW(0,a4,0),
             "ghz1prime2": 0,
             "ghw1prime2":EFTmodel.L1W(0,a4,0),
             "ghzgs1prime2": EFTmodel.L1Zgamma(0,a4,0),
         }
         a4weight = ""
         if hff == 1 : 
              a4weight =  Sample(type_,useHJJ=True,kappa=1,kappa_tilde=0, **couplings).weight
         else :
              a4weight =  Sample(type_,useHJJ=True,kappa=0,kappa_tilde=1, **couplings).weight
       
         couplings = {
             "ghv1": 0,
             "ghz2": 0,
             "ghw2":EFTmodel.g2WW(0,0,L1),
             "ghz4": 0,
             "ghw4": EFTmodel.g4WW(0,0,L1),
             "ghz1prime2": L1,
             "ghw1prime2":EFTmodel.L1W(0,0,L1),
             "ghzgs1prime2": EFTmodel.L1Zgamma(0,0,L1),
         }

         l1weight =""
         if hff == 1 : 
              l1weight =  Sample(type_,useHJJ=True,kappa=1,kappa_tilde=0, **couplings).weight
         else :
              l1weight =  Sample(type_,useHJJ=True,kappa=0,kappa_tilde=1, **couplings).weight




         if( sm  + a2 + a4 + l1 > 1 ):
             if sm == 1 :
                 weightt = weightt+"-"+smweight
             if a2 == 1 :
                 weightt = weightt+"-"+a2weight
             if a4 == 1 :   
                 weightt = weightt+"-"+a4weight
             if l1 == 1 :
                 weightt =  weightt+"-"+l1weight
         weightt = "MC_weight_nominal*("+weightt+")"        
         data["templates"][i]["weight"] = [weightt]
         i = i +1


     #fix parameter 
     if "Untagged" in f.name : 
          data["constraints"][0]["type"] = "threeparameterHVV"
     else :
          data["constraints"][0]["type"] = "twoparameterHVV"
          data["constraints"][1]["type"] = "twoparameterHVV"

                 
     #clear out L1Zgamma entries and arrange constraints list 
     #remove  L1Zg always   and a3 in case twoparameters are used
     new_list =	[]
     for element in data["templates"]:
          if not ("ghzgs1prime2" in element["name"] )  and not( "0L1Zg" in element["name"] ):
              new_list.append(element)
     data["templates"] = new_list

     print "done "


     '''
     itt = 0
     while itt < 5 :
         it = 0
         for element in data["templates"]:
             #print it
             if "ghzgs1prime2" in element["name"] or "0L1Zg" in element["name"]:
                 #print "here"
                 del data["templates"][it]
                 itt  = itt +1
                 break
             it = it +1

     if data["constraints"][0]["type"] == "twoparameterHVV" : 
          itt = 0
          while itt < 4 :
               it = 0
               for element in data["templates"]:
                    if "g4" in element["name"] or "0Minus" in element["name"]:
                         del data["templates"][it]
                         itt  = itt +1
                         break
                    it = it +1

     '''



     #rearrangenames
                    
     replace_names =[]
     sm_t = []
     g2_t = []

     iic = 0
     for iconst in data["constraints"]:
          if iconst["type"] == "threeparameterHVV" and iic == 0 :
               #print "here"                                            
	       replace_names =["template0Plus","templateg11g21Int","templateg11g41IntMirror","templateg11g1prime21Int",
                          "template0HPlus","templateg41g21IntMirror","templateg21g1prime21Int",
                          "template0Minus","templateg41g1prime21IntMirror",
                          "template0L1"]
               
          elif iconst["type"] == "threeparameterHVV" and iic != 0  :
               replace_names =["templateHff0MinusHVV0Plus","templateHff0MinusHVVg11g21Int","templateHff0MinusHVVg11g41IntMirror","templateHff0MinusHVVg11g1prime21Int",
                          "templateHff0MinusHVV0HPlus","templateHff0MinusHVVg41g21IntMirror","templateHff0MinusHVVg21g1prime21Int",
                          "templateHff0MinusHVV0Minus","templateHff0MinusHVVg41g1prime21IntMirror",
                          "templateHff0MinusHVV0L1"]
         

          elif iconst["type"] == "twoparameterHVV" and iic == 0 :
               #print "there"                                           
               replace_names =["template0Plus","templateg11g21Int","templateg11g1prime21Int",
                              "template0HPlus","templateg21g1prime21Int",
                              "template0L1"]

               
          elif iconst["type"] == "twoparameterHVV" and iic != 0  :
               replace_names =["templateHff0MinusHVV0Plus","templateHff0MinusHVVg11g21Int","templateHff0MinusHVVg11g1prime21Int","templateHff0MinusHVV0HPlus","templateHff0MinusHVVg21g1prime21Int","templateHff0MinusHVV0L1"]
         

               
          data["constraints"][iic]["templates"] = replace_names
          iic =  iic +1


    
     outputf =  inputfile.replace(".json",".root")
     data["outputFile"] = ntpath.basename(outputf)


     ##print    replace_names
     for iiconst in range(0,len(data["constraints"])):

           for itemp in range(0,len( data["constraints"][iiconst]["templates"])) :
                if not ( added_String in data["constraints"][iiconst]["templates"][itemp]) :
                     data["constraints"][iiconst]["templates"][itemp] = data["constraints"][iiconst]["templates"][itemp]+added_String



     outfilename = ntpath.basename(inputfile) 


     with open(outfilename,"w") as outt:
         json.dump(data,outt,indent=4)
    
    

if __name__ == '__main__':


    input = sys.argv[1]

    jsonmaker_ggH(input,"ggH")
    
