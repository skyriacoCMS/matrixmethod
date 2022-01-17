class tempFile:

    def __init__(self, name):
        
        self.name = name

    def GetDMode(self):
        dmode = ""
        if "2e2mu" in self.name:
            dmode = "2e2mu"
        if "4mu" in self.name:
            dmode = "4mu"
        if "4e" in self.name:
            dmode = "4e"
        return dmode

    def GetPMode(self):
        pmode = ""
        if "tth_" in self.name or "ttH_" in self.name :
            pmode = "ttH"
        if "bbh_" in self.name or "bbH_" in self.name :
            pmode = "bbH"
        if "ggh_" in self.name or "ggH_" in self.name :
            pmode = "ggH"
        if "qqh_" in self.name or "qqH_" in self.name :
            pmode  = "qqH"
        if "vh_" in self.name or "VH_" in self.name :
            pmode = "VH"
        if "vbf_" in self.name or "VBF_" in self.name:
            pmode = "VBF"
        if "background" in self.name :
            pmode = "background"
        if "Data" in self.name or "data" in self.name :
            pmode = ""
        if "Hff" in self.name :
            pmode = pmode+"_Hff0MinusHVV"
        #if "0Mff" in self.name :
        #    pmode = pmode+"_0Mff"

        return pmode
    
    def GetYearandLumi(self):
        year = ""
        lumi = 0
        if "2016" in self.name:
            year = "2016"
            lumi = 35.90
        if "2017" in self.name:
            year = "2017"
            lumi = 41.5
        if "2018" in self.name:
            year = "2018"
            lumi = 59.7  
        return year,lumi

    def GetCategory(self):
        category = ""


        if "VBFtagged" in self.name:
            category = "VBFtagged"
        if "VHHadrtagged" in self.name:
            category = "VHHadrtagged"
        if "VHLepttagged" in self.name:
            category = "VHLepttagged"
        if "Boosted" in self.name:
            category = "Boosted"
        if "Untagged" in self.name:
            category = "Untagged"
        if "VBF1jtagged" in self.name:
            category = "VBF1jtagged"
              
        return category


class tempHist (tempFile):


    def GoodPowers(self):

        goodP = True
        
        if not( "Hff" in self.name) : 

            summ = 0
            g1 = 0
            g2 = 0
            g4 = 0
            g1prime2=0
            
            if "g11" in self.name :
                g1 = 1
            if "g12" in self.name :
                g1 = 2
            if "g13" in self.name :
                g1 = 3

            if "g21" in self.name :
                g2 = 1
            if "g22" in self.name :
                g2 = 2
            if "g23" in self.name :
                g2 = 3

            if "g41" in self.name :
                g4 = 1
            if "g42" in self.name :
                g4 = 2
            if "g43" in self.name :
                g4 = 3

            if "g1prime21" in self.name :
                g1prime2 = 1
            if "g1prime22" in self.name :
                g1prime2 = 2
            if "g1prime23" in self.name :
                g1prime2 = 3
                       
                
            summ = g1 + g2 + g1prime2 + g4
            if summ < 4 and summ > 0:
                goodP = False
            
              
        return goodP

    
