import json
import sys
import ntpath
import EFTmodel1 as EFTmodel
from sample import Sample 

inputfile = sys.argv[1]

#with open('templates_ggh_fa3fa2fL1fL1Zg_morecategories_2e2mu_Untagged_190703_2018.json') as f:
with open(inputfile) as f:
    data = json.load(f)



print("\n")
#print(data["constraints"])
#print(data["templates"][1]["binning"])
print("\n")

#print(data["constraints"])

i = 0 
for temp  in data["templates"] :
#    print( temp ," ", i)
    print (temp["name"])
    name = temp["name"]

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

    weightt =  Sample("ggH", **couplings).weight
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
    smweight = Sample("ggH", **couplings).weight

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
    a2weight = Sample("ggH", **couplings).weight

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
    a4weight = Sample("ggH", **couplings).weight

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
    l1weight = Sample("ggH", **couplings).weight
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
'''
itt = 0
for element in data["templates"]:
   # print it
    if "ghzgs1prime2" in element["name"] or "0L1Zg" in element["name"]:
        print "here"
        #del data["templates"][it]
        itt  = itt +1  
print itt
'''

itt = 0
while itt < 5 :
    it = 0
    for element in data["templates"]:
        print it
        if "ghzgs1prime2" in element["name"] or "0L1Zg" in element["name"]:
            print "here"
            del data["templates"][it]
            itt  = itt +1
            break
        it = it +1
#print len(data["templates"])

replace_names =[]

for element in data["templates"]:
    print element["name"] 
    replace_names.append(element["name"])

    
data["constraints"][0]["type"] = "threeparameterHVV"
data["constraints"][0]["templates"] = replace_names

#print replace_names
    


outfilename = ntpath.basename(inputfile) 

    
with open(outfilename,"w") as outt:
    json.dump(data,outt,indent=4)
 
    
