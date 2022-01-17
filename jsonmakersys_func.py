import json
import sys
import ntpath
import EFTmodel1 as EFTmodel
from sample import Sample 


def jsonmaker_sys(inputfile):

      
    #with open('templates_ggh_fa3fa2fL1fL1Zg_morecategories_2e2mu_Untagged_190703_2018.json') as f:
     with open(inputfile) as f:
         print f 
         data = json.load(f)

     infile = inputfile    
     rfile  = infile.replace("ScaleDown_","")
     rfile1 = rfile.replace("ScaleUp_","")
     rfile2 = rfile1.replace("ResUp_","")
     rfile3 = rfile2.replace("ResDn_","")
     rfile4 = rfile3.replace("JECDn_","")
     rfile5 = rfile4.replace("JECUp_","")
     rfile6 = rfile5.replace("qmtopDn_","")
     rfile7 = rfile6.replace("qmtopUp_","")
     rfile8 = rfile7.replace("PT60Dn_","")
     rfile9 = rfile8.replace("PT60Up_","")
     rfile10 = rfile9.replace("Mig12Up_","")
     rfile12 = rfile10.replace("PT120Up_","")
     rfile13 = rfile12.replace("PT120Dn_","")
     rfile14 = rfile13.replace("THU_ggH_","")
     rfile15 = rfile14.replace("VBF3jDn_","")
     rfile16 = rfile15.replace("VBF3jUp_","")
     rfile17 = rfile16.replace("Mig01Dn_","")
     rfile18 = rfile17.replace("VBF2jDn_","")
     rfile19 = rfile18.replace("VBF2jUp_","")
     rfile20 = rfile19.replace("Mig12Dn_","")
     rfile21 = rfile20.replace("Mig01Up_","")
     rfile22 = rfile21.replace("ResDown_","")
     
     rfile11 = ntpath.basename(rfile22) 



     print("\n")
     #print(data["constraints"])
     #print(data["templates"][1]["binning"])
     print("\n")
     #print infile
     #print rfile11
     #print(data["constraints"])

     i = 0
     tot_torem = 0
     new_names =[] 
     for temp  in data["templates"] :
         #    print( temp ," ", i)
         #print (temp["name"])
         name = temp["name"]
         if "ghzgs1prime2" in temp["name"] or "0L1Zg" in temp["name"]:
              tot_torem +=1
         else :
              new_names.append(name)

         inputfile_read = rfile11
         with open(inputfile_read) as fin:
              dataread = json.load(fin)

              for tempp in dataread["templates"]:
                   name2 = tempp["name"] 
                   weightt = tempp["weight"]
                   if name ==  name2 :
                        print name , weightt
                        data["templates"][i]["weight"] = weightt
         i +=1


     outfilename = ntpath.basename(inputfile) 



     
     itt = 0
     while itt < tot_torem :
         it = 0
         for element in data["templates"]:
             print it
             if "ghzgs1prime2" in element["name"] or "0L1Zg" in element["name"]:

                 del data["templates"][it]
                 itt  = itt +1
                 break
             it = it +1
             #print len(data["templates"])


     outputf =  infile.replace(".json",".root")        
     data["outputFile"] = ntpath.basename(outputf)

     with open(outfilename,"w") as outt:
         json.dump(data,outt,indent=4)





         

'''


         


         sm = 0
         a2 = 0
         a4 = 0
         l1 = 0
         L1 = 0



         if "0Plus" in name:
             sm = 1 
         if "0HPlus" in name:
             a2 = 1
         if "0Minus" in name:
             a4 = 1
         if "0L1Mirror" in name:
             l1 = 1

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
             "ghw2":EFTmodel.g2WW(a2,a4,l1),
             "ghz4": a4,
             "ghw4": EFTmodel.g4WW(a2,a4,l1),
             "ghz1prime2": L1,
             "ghw1prime2":EFTmodel.L1W(a2,a4,l1),
             "ghzgs1prime2": EFTmodel.L1Zgamma(a2,a4,l1),
         }


         #print (data["templates"][i]["weight"])

         weightt =  Sample(type_, **couplings).weight
         #print (weightt)
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
         smweight = Sample(type_, **couplings).weight

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
         a2weight = Sample(type_, **couplings).weight

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
         a4weight = Sample(type_, **couplings).weight

         couplings = {
             "ghv1": 0,
             "ghz2": 0,
             "ghw2":EFTmodel.g2WW(0,0,l1),
             "ghz4": 0,
             "ghw4": EFTmodel.g4WW(0,0,l1),
             "ghz1prime2": L1,
             "ghw1prime2":EFTmodel.L1W(0,0,l1),
             "ghzgs1prime2": EFTmodel.L1Zgamma(0,0,l1),
         }
         l1weight = Sample(type_, **couplings).weight
         if( sm  + a2 + a4 + l1 > 1 ):
             if sm == 1 :
                 weightt = weightt+"-"+smweight
             if a2 == 1 :
                 weightt = weightt+"-"+a2weight
             if a4 == 1 :   
                 weightt = weightt+"-"+a4weight
             if l1 == 1 :
                 weight =  weightt+"-"+l1weight
                 weightt = "MC_weight_nominal*("+weightt+")"        
                 data["templates"][i]["weight"] = [weightt]
                 i = i +1

     #clear out L1Zgamma entries

     replace_names =[]

     for element in data["templates"]:
         print element["name"] 
         replace_names.append(element["name"])


     data["constraints"][0]["type"] = "threeparameterHVV"
     data["constraints"][0]["templates"] = replace_names

     #print replace_names



     
'''    
    

if __name__ == '__main__':


    input = sys.argv[1]

    jsonmaker_sys(input)
    
