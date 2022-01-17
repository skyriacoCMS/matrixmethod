import json
import EFTmodel1 as EFTmodel
from sample import Sample 
from numpy.random import seed
from numpy.random import randint
import numpy as np


with open('templates_vbf_fa3fa2fL1fL1Zg_morecategories_2e2mu_Untagged_190703_2018.json') as f: 
    data = json.load(f)



print("\n")
#print(data["constraints"])
#print(data["templates"][1]["binning"])
print("\n")

#print(data["constraints"])

i = 0


base = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]] 

seed(123456)

for i in range(0,31):

    a = randint(1,10)
    b = randint(1,10)
    c = randint(1,10)
    d = randint(1,10)

    
    new  = [a,b,c,d]
    base.append(new)

print(base)


#construct matrix for linear combination calculation


def pol(a,ea,b,eb,c,ec,d,ed):

    return (a**ea)*(b**eb)*(c**ec)*(d**ed)

exponents= [[4,0,0,0],[3,1,0,0],[3,0,1,0],[3,0,0,1],
            [2,2,0,0],[2,1,1,0],[2,1,0,1],[2,0,2,0],
            [2,0,1,1],[2,0,0,2],[1,3,0,0],[1,2,1,0],
            [1,2,0,1],[1,1,2,0],[1,1,1,1],[1,1,0,2],
            [1,0,3,0],[1,0,2,1],[1,0,1,2],[1,0,0,3],
            [0,4,0,0],[0,3,1,0],[0,3,0,1],[0,2,2,0],
            [0,2,1,1],[0,2,0,2],[0,1,3,0],[0,1,2,1],
            [0,1,1,2],[0,1,0,3],[0,0,4,0],[0,0,3,1],
            [0,0,2,2],[0,0,1,3],[0,0,0,4]]

#print row

def check_exp():
    for i in range (0,35):

        if sum(exponents[i]) != 4 :
            print "PROBLEM",i
            
            for j in range (0,35):
                if j == i :
                    continue
                if exponents[j] == exponents[i]:
                    print "identical!",i,j



check_exp()
m_atrix = []

for i in range (0,35):

    row = []
    for j in range(0,35): 
        #ea = 4; eb = 0; ec = 0; ed = 0
        element_ij = pol(base[i][0],exponents[j][0],base[i][1],exponents[j][1],base[i][2],exponents[j][2],base[i][3],exponents[j][3])
        print element_ij
        row.append(element_ij)
      
    m_atrix.append(row)

print m_atrix

A_m = np.array(m_atrix)
print A_m

A_m_inv = np.linalg.inv(A_m)
print A_m_inv

itemp = 0
for temp  in data["templates"] :
#    print( temp ," ", i)
    #print (temp["name"])
    name = temp["name"]
        
    if "ghzgs1prime2" in name or "0L1Zg" in name:
        continue
    
    sm = 0
    a2 = 0
    a4 = 0
    l1 = 0
    L1 = 0


    
    if "0Plus" in name:
        sm = 4 
    if "0HPlus" in name:
        a2 = 4
    if "0Minus" in name:
        a4 = 4
    if "0L1Mirror" in name:
        l1 = 4

    if "g13" in name:
        sm = 3
    if "g12" in name:
        sm = 2
    if "g11" in name:
        sm = 1

    if "g23" in name:
        a2 = 3
    if "g22" in name:
        a2 = 2
    if "g21" in name:
        a2 = 1

    if "g43" in name:
        a4 = 3
    if "g42" in name:
        a4 = 2
    if "g41" in name:
        a4 = 1
        
    if "g1prime23" in name:
        l1 = 3
        L1 = 1e4
    if "g1prime22" in name:
        l1 = 2
        L1 = 1e4
    if "g1prime21" in name:
        l1 = 1
        L1 = 1e4


    temp_exponents = [sm,a2,a4,l1]
    row_index = -1
    for indx in range(0,35):

        if temp_exponents == exponents[indx]:
            row_index = indx


   # print row_index



    #construct weight by multiplying inverse matrix row with base sample weights.
    weightt = ""
    for i in range(0,35): 

        couplings = {
            "ghv1": base[i][0],
            "ghz2": base[i][1],
            "ghw2":EFTmodel.g2WW(base[i][1],base[i][2],base[i][3]),
            "ghz4": base[i][2],
            "ghw4": EFTmodel.g4WW(base[i][1],base[i][2],base[i][3]),
            "ghz1prime2": L1*base[i][3],
	    "ghw1prime2":EFTmodel.L1W(base[i][1],base[i][2],base[i][3]),
	    "ghzgs1prime2": EFTmodel.L1Zgamma(base[i][1],base[i][2],base[i][3]),
        }
        

        #print (data["templates"][i]["weight"])
        
        w_Sample =  Sample("VBF", **couplings).weight
        if i == 0 : 
            weightt = weightt+"("+str(A_m_inv[row_index][i])+")*("+w_Sample+")"
        else:
            weightt = weightt+"+("+str(A_m_inv[row_index][i])+")*("+w_Sample+")" 
        
    weightt = "MC_weight_nominal*("+weightt+")"        
    print "\n"
#    print weightt
    print "\n"
    
    data["templates"][itemp]["weight"] = [weightt]
    itemp = itemp + 1


#remove all L1zg templates
print len(data["templates"])

itt = 0
while itt < 35 :
    it = 0
    for element in data["templates"]:
        print it
        if "ghzgs1prime2" in element["name"] or "0L1Zg" in element["name"]:
            print "here"
            del data["templates"][it]
            itt  = itt +1
            break
        it = it +1
print len(data["templates"])


'''
itt = 0
for temp  in data["templates"].keys() :
    #if temp == len(data["templates"]) -5 :
    #    break
    #data[] :
    name = temp["name"]
    if "ghzgs1prime2" in name or "0L1Zg" in name:
        del data["templates"][temp]
          
print len(data["templates"])

'''
for temp  in data["templates"] :
#    print( temp ," ", i)
    #print (temp["name"])
    print temp["name"]



print len(data["templates"])

data["constraints"][0]["type"] = "threeparameterVVHVV"

data["constraints"][0]["templates"] = ["template0PlusMirror",
"template0MinusMirror",
"template0HPlusMirror",
"template0L1Mirror",
"templateg13g41IntMirror",
"templateg13g21IntMirror",
"templateg13g1prime21IntMirror",
"templateg43g21IntMirror",
"templateg43g1prime21IntMirror",
"templateg23g1prime21IntMirror",
"templateg12g42IntMirror",
"templateg12g22IntMirror",
"templateg12g1prime22IntMirror",
"templateg42g22IntMirror",
"templateg42g1prime22IntMirror",
"templateg22g1prime22IntMirror",
"templateg11g43IntMirror",
"templateg11g23IntMirror",
"templateg11g1prime23IntMirror",
"templateg41g23IntMirror",
"templateg41g1prime23IntMirror",
"templateg21g1prime23IntMirror",
"templateg12g41g21IntMirror",
"templateg12g41g1prime21IntMirror",
"templateg12g21g1prime21IntMirror",
"templateg42g21g1prime21IntMirror",
"templateg11g42g21IntMirror",
"templateg11g42g1prime21IntMirror",
"templateg11g22g1prime21IntMirror",
"templateg41g22g1prime21IntMirror",
"templateg11g41g22IntMirror",
"templateg11g41g1prime22IntMirror",
"templateg11g21g1prime22IntMirror",
"templateg41g21g1prime22IntMirror",
"templateg11g41g21g1prime21IntMirror"]

with open("testout_VBF.json","w") as outt:
    json.dump(data,outt,indent=4)

    
