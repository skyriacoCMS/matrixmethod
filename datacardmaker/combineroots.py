from Class_Templatefiles import tempFile,tempHist
import ROOT
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH3F
import os
import re


def CombineTemps(decay, category, year):



  if year == "2016":
    inp = "inp2016"
  if year == "2017":
    inp = "inp2017"
  if year == "2018":
    inp = "inp2018"
  



  f = open(inp,"r") 
  contents = f.readlines()

  out_name = "./CombinedTempFiles/templates_"+str(decay)+"_"+str(category)+"_"+str(year)+".root"

  fout = ROOT.TFile.Open(out_name,"recreate")


  for x in contents:
    #    print x
    
    NAME = x.rstrip()
    uncert_name=None
    if ( ("Down" in NAME) or ( "Dn" in NAME) or ( "Up" in NAME)  ):
      print "\n" 
      print "\n" 
      print "\n" 
      print "need to change name : "
      result =   re.search('ed_(.*)200205_2018',NAME)
      print NAME
      uncert_name = result.group(1)
      print uncert_name
      uncert_name =  uncert_name[:-1]
      print uncert_name

    if  not ("morecategories" in NAME):
        continue
    if  not year in NAME :
        continue
    if not decay in NAME :
        continue
    if not category in NAME:
        continue
    if not ".root" in NAME:
        continue
    
    #print NAME
    filee = ROOT.TFile.Open(NAME)
    fout.cd()
    tf = tempFile(NAME)
    for key in filee.GetListOfKeys():

        if "template" in key.GetName() and  "TH3F" in key.GetClassName() :
            h_name = key.GetName()
            temphist = filee.Get(h_name)
            th = tempHist(h_name)
            
            if "L1Zg" in h_name or "ghzgs1prime" in h_name:
                continue

            passPowers = True # th.GoodPowers()
            if not passPowers :
              print h_name , " ", NAME
              continue
              
            h_name = h_name.replace("template","")
            h_name =  h_name.replace("Int","")
            h_name = h_name.replace("Mirror","")
              
            temphist.SetName(tf.GetPMode()+"_"+h_name)
            temphist.SetTitle(tf.GetPMode()+"_"+h_name)
            if uncert_name is not None:
              temphist.SetName(tf.GetPMode()+"_"+h_name+"_"+uncert_name)
              temphist.SetTitle(tf.GetPMode()+"_"+h_name+"_"+uncert_name)

            temphist.Write("",ROOT.TObject.kOverwrite)



            




    
