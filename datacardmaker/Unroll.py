from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH3F
from Class_Templatefiles import tempFile,tempHist


def  Unroll(hist):
    xbins = hist.GetNbinsX()
    ybins = hist.GetNbinsY()
    zbins = hist.GetNbinsZ()


    temp_pos = TH1F("temp_pos","",xbins*ybins*zbins,0,xbins*ybins*zbins)
    temp_neg = TH1F("temp_neg","dif",xbins*ybins*zbins,0,xbins*ybins*zbins)

    #Unroll Hists
    indk = 0
    has_negative = False 
    for y in range (1,ybins+1):
        for x in range (1,xbins+1):
            for z in range (1,zbins+1):


                binx_c = hist.GetXaxis().GetBinCenter(x)
                biny_c = hist.GetYaxis().GetBinCenter(y)
                binz_c = hist.GetZaxis().GetBinCenter(z)
                ibin =  hist.FindBin(binx_c,biny_c,binz_c)
                cont  = hist.GetBinContent(ibin)
                if cont  < 0 :
                    has_negative = True

                    
    for y in range (1,ybins+1):
        for x in range (1,xbins+1):
            for z in range (1,zbins+1):
                binx_c = hist.GetXaxis().GetBinCenter(x)
                biny_c = hist.GetYaxis().GetBinCenter(y)
                binz_c = hist.GetZaxis().GetBinCenter(z)
                ibin =  hist.FindBin(binx_c,biny_c,binz_c)
                cont  = hist.GetBinContent(ibin)
                if cont  < 0 :
                    temp_neg.Fill(indk,-1*cont)
                else :
                    temp_pos.Fill(indk,cont)
                indk = indk +1
    temp_name = hist.GetName()
    
    tpname = temp_name
    tnname = temp_name

    tnname = tnname.replace("Hff0MinusHVV","0Xff_")
    tpname = tpname.replace("Hff0MinusHVV","0Xff_")
      
    tnname = tnname.replace("0HPlus","0PH")
    tnname = tnname.replace("0Plus","0PM")
    tnname = tnname.replace("0Minus","0M")

    tpname = tpname.replace("0HPlus","0PH")
    tpname = tpname.replace("0Plus","0PM")
    tpname = tpname.replace("0Minus","0M")

    tnname = tnname.replace("background","bkg")
    tpname = tpname.replace("background","bkg")

    tpname = tnname.replace("qqZZ","qqzz")
    tpname = tpname.replace("ggZZ","ggzz")
    tpname = tpname.replace("ZX","zjets")
    tpname = tpname.replace("EW","ew")

    tnname = tpname.replace("VBF","qqH")
    tpname = tpname.replace("VBF","qqH")

    

    
    if (has_negative or not ( "bkg" in tnname or "Data" in tnname  or "0PH" in tnname or "0PM" in tnname or "L1" in tnname or "0M" in tnname) ):
    
        tnname = tnname.replace("0Xff_","0Mff_")
        tpname = tpname.replace("0Xff_","0Mff_")
        tnname = tnname+"_negative"
        tpname = tpname+"_positive"
        temp_neg.SetName(tnname)
	temp_pos.SetName(tpname)
    else:
    
        tnname = tnname.replace("0Xff_","0Mff_")
        tpname = tpname.replace("0Xff_","0Mff_")

        if ( not ( "0Mff" in tnname )  )  and ("ggH" in tnname or "ttH" in tnname): 

     #       print tpname
        
            tnsplit =tnname.split("_") 
            tpsplit =tpname.split("_")
            
            tpname = tpsplit[0] + "_0PMff_"
            tnname = tnsplit[0] + "_0PMff_"             
            #take care of syst by adding all the full ending 
            for nitem in range(1,len(tpsplit)):
                tpname = tpname+"_"+tpsplit[nitem]
            for nitem in range(1,len(tnsplit)):
                tnname = tnname+"_"+tnsplit[nitem]
            tpname = tpname.replace("__","_")
            tnname = tpname.replace("__","_")
                
        
        temp_neg.SetName(tnname)
        temp_pos.SetName(tpname)

    if "data" in  tnname or "Data" in tnname : 
        

        temp_neg.SetName("data_obs")
        temp_pos.SetName("data_obs")

    th = tempHist(temp_name)
    if not th.GoodPowers() and not "ff" in temp_name  and not "bbH" in temp_name:
        tnsplit =tnname.split("_") 
        tpsplit =tpname.split("_") 
        tpname = tpsplit[0] + "_0PMff_"+tpsplit[1]
        tnname = tnsplit[0] + "_0PMff_"+tnsplit[1]

        for it in range(2,len(tnsplit)):
            tpname = tpname+"_"+tpsplit[it]
            tnname = tnname+"_"+tnsplit[it]
                    
        temp_neg.SetName(tnname)
        temp_pos.SetName(tpname)
        
    #print temp_neg.GetName() , temp_pos.GetName()
    return temp_neg,temp_pos
