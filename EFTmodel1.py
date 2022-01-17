#!/usr/bin/env python

from sample import Sample

cosW = 0.87681811112
sinW = 0.48082221247


mZ   = 91.2
L1   = 1e4

def g2WW(g2,g4,gzprime2):
    value = (cosW**2)*g2
    return value
    
def g4WW(g2,g4,gzprime2):
    value = (cosW**2)*g4
    return value

def L1W(g2,g4,gzprime2):
    value =  (L1**2)/(cosW**2 - sinW**2) * ( gzprime2/(L1**2)  - 2*g2*(sinW**2)/(mZ**2))
    return  value

def L1Zgamma(g2,g4,gzprime2):
    value = 2*cosW*sinW*(L1**2)/(cosW**2 - sinW**2)*( gzprime2/(L1**2) - g2/mZ**2) 
    return  value


if __name__ == "__main__":
    #SM 
    print "--- Pure SM ---"
    couplings = {
        "ghv1": 1,
        "ghz2": 0,
        "ghw2": 0, #0.77718144044,   # (mass_W/mass_Z)^2  = cosThetaw ^2
        "ghz4": 0,
        "ghw4": 0,
        "ghz1prime2": 0,
        "ghw1prime2": 0,
        "ghzgs1prime2": 0,
    }
    print "VBF:  "
    print Sample("VBF", **couplings).weight
    print "ZH :  "
    print Sample("ZH", **couplings).weight
    print "WH :  "
    print Sample("WH", **couplings).weight
    print "ggH :  "
    print Sample("ggH", **couplings).weight
    print "--------------------------------"
    
    #PURE a2
    print "---- Pure a2 ----"
    couplings = {
        "ghv1": 0,
        "ghz2": 1,
        "ghw2": g2WW(1,0,0),   # (mass_W/mass_Z)^2  = cosThetaw ^2
        "ghz4": 0,
        "ghw4": g4WW(1,0,0),
        "ghz1prime2": 0,
        "ghw1prime2": L1W(1,0,0),
        "ghzgs1prime2":  L1Zgamma(1,0,0),
    }
    print "VBF:  "
    print Sample("VBF", **couplings).weight
    print "ZH :  "
    print Sample("ZH", **couplings).weight
    print "WH :  "
    print Sample("WH", **couplings).weight
    print "ggH :  "
    print Sample("ggH", **couplings).weight
    print "--------------------------------"
    
    print "---- Pure a4 ----"
    #a4 only 
    couplings = {
        "ghv1": 0,
        "ghz2": 0,
        "ghw2": g2WW(0,1,0),   # (mass_W/mass_Z)^2  = cosThetaw ^2
        "ghz4": 1,
        "ghw4": g2WW(0,1,0),
        "ghz1prime2": 0,
        "ghw1prime2": L1W(0,1,0),
        "ghzgs1prime2": L1Zgamma(0,1,0),
    }
    print "VBF:  "
    print Sample("VBF", **couplings).weight
    print "ZH :  "
    print Sample("ZH", **couplings).weight
    print "WH :  "
    print Sample("WH", **couplings).weight
    print "ggH :  "
    print Sample("ggH", **couplings).weight
    print "--------------------------------"
    
    
    print "---- Pure L1 ----"
    #l1 only 
    couplings = {
        "ghv1": 0,
        "ghz2": 0,
        "ghw2": g2WW(0,0,1e4),   # (mass_W/mass_Z)^2  = cosThetaw ^2
        "ghz4": 0,
        "ghw4": g2WW(0,0,1e4),
        "ghz1prime2": 1e4,
        "ghw1prime2": L1W(0,0,1e4),
        "ghzgs1prime2": L1Zgamma(0,0,1e4),
    }
    print "VBF:  "
    print Sample("VBF", **couplings).weight
    print "ZH :  "
    print Sample("ZH", **couplings).weight
    print "WH :  "
    print Sample("WH", **couplings).weight
    print "ggH :  "
    print Sample("ggH", **couplings).weight
    print "--------------------------------"
    

    print "---- g2 L1 ----"
    #l1 only 
    couplings = {
        "ghv1": 0,
        "ghz2": 1,
        "ghw2": g2WW(1,0,1e4),   # (mass_W/mass_Z)^2  = cosThetaw ^2
        "ghz4": 0,
        "ghw4": g2WW(1,0,1e4),
        "ghz1prime2": 1e4,
        "ghw1prime2": L1W(1,0,1e4),
        "ghzgs1prime2": L1Zgamma(1,0,1e4),
    }
    print "VBF:  "
    print Sample("VBF", **couplings).weight
    print "ZH :  "
    print Sample("ZH", **couplings).weight
    print "WH :  "
    print Sample("WH", **couplings).weight
    print "ggH :  "
    print Sample("ggH", **couplings).weight
    print "--------------------------------"

    
    print "---- g4 L1 ----"
    #l1 only 
    couplings = {
        "ghv1": 0,
        "ghz2": 0,
        "ghw2": g2WW(0,1,1e4),   # (mass_W/mass_Z)^2  = cosThetaw ^2
        "ghz4": 1,
        "ghw4": g2WW(0,1,1e4),
        "ghz1prime2": 1e4,
        "ghw1prime2": L1W(0,1,1e4),
        "ghzgs1prime2": L1Zgamma(0,1,1e4),
    }
    print "VBF:  "
    print Sample("VBF", **couplings).weight
    print "ZH :  "
    print Sample("ZH", **couplings).weight
    print "WH :  "
    print Sample("WH", **couplings).weight
    print "ggH :  "
    print Sample("ggH", **couplings).weight
    print "--------------------------------"


    
    print "---- g2 g4 ----"
    #l1 only 
    couplings = {
        "ghv1": 0,
        "ghz2": 1,
        "ghw2": g2WW(1,1,0),   # (mass_W/mass_Z)^2  = cosThetaw ^2
        "ghz4": 1,
        "ghw4": g2WW(1,1,0),
        "ghz1prime2": 0,
        "ghw1prime2": L1W(1,1,0),
        "ghzgs1prime2": L1Zgamma(1,1,0),
    }
    print "VBF:  "
    print Sample("VBF", **couplings).weight
    print "ZH :  "
    print Sample("ZH", **couplings).weight
    print "WH :  "
    print Sample("WH", **couplings).weight
    print "ggH :  "
    print Sample("ggH", **couplings).weight
    print "--------------------------------"





    
    
    #
    
