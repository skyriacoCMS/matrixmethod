import os
from jsonmakerggH_func import jsonmaker_ggH
from jsonmakerVBF_func import jsonmaker_vbf
from jsonmakersys_func import jsonmaker_sys
from jsonmakerggHHff_func import jsonmaker_ggHHff
from jsonmakerggHttH_func import jsonmaker_ggHttH


for filename in os.listdir("/work-zfs/lhc/heshy/anomalouscouplings/step5_json/200205_2017/"):

    #print filename

    if ( "background" in filename ) :
        continue
    
    if ( "ggh" in filename ) and not( "Down" in filename ) and not("Dn" in filename) and not("Up" in filename) and not ("VBFtagged" in filename) and not("VHHadrtagged" in filename): 
        inputt = os.path.join("/work-zfs/lhc/heshy/anomalouscouplings/step5_json/200205_2017/", filename)
        jsonmaker_ggH(inputt,"ggH")

    if ( "ggh" in filename ) and not( "Down" in filename ) and not("Dn" in filename) and not("Up" in filename) and ( ("VBFtagged" in filename) or ("VHHadrtagged" in filename)): 
        print "here"
        inputt = os.path.join("/work-zfs/lhc/heshy/anomalouscouplings/step5_json/200205_2017/", filename)
        jsonmaker_ggHHff(inputt)

        
    if ( "bbh" in filename ) and not( "Down" in filename ) and not("Dn" in filename) and not("Up" in filename): 
        inputt = os.path.join("/work-zfs/lhc/heshy/anomalouscouplings/step5_json/200205_2017/", filename)
        jsonmaker_ggH(inputt,"bbH")

    if ( "tth" in filename ) and not( "Down" in filename ) and not("Dn" in filename) and not("Up" in filename): 
        inputt = os.path.join("/work-zfs/lhc/heshy/anomalouscouplings/step5_json/200205_2017/", filename)
        jsonmaker_ggHttH(inputt,"ttH")


    if ( "vbf" in filename ) and not( "Down" in filename ) and not("Dn" in filename) and not("Up" in filename):
        inputt = os.path.join("/work-zfs/lhc/heshy/anomalouscouplings/step5_json/200205_2017/", filename)
        jsonmaker_vbf(inputt,"VBF")

    if ( "vh" in filename ) and not( "Down" in filename ) and not("Dn" in filename) and not("Up" in filename):
        inputt = os.path.join("/work-zfs/lhc/heshy/anomalouscouplings/step5_json/200205_2017/", filename)
        jsonmaker_vbf(inputt,"VH")


#Now fix weights for syst templates.         
for filename in os.listdir("/work-zfs/lhc/heshy/anomalouscouplings/step5_json/200205_2017/"):

    
    if ( "background" in filename ) :
        continue

    
    if ( "Down" in filename ) or ("Dn" in filename) or ("Up" in filename):
        inputt = os.path.join("/work-zfs/lhc/heshy/anomalouscouplings/step5_json/200205_2017/", filename)
        jsonmaker_sys(inputt)











