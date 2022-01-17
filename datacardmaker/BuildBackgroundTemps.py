from Class_Templatefiles import tempFile,tempHist
import ROOT
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH3F
import os

import sys

import re
import math


def BuildBackgroundTemps(decay, category, year):

  if year == "2016":
    inp = "offshell_2016"
  if year == "2017":
    inp = "offshell_2017"
  if year == "2018":
    inp = "offshell_2018"
  

    

  f = open(inp,"r") 
  contents = f.readlines()



  for x in contents:
    NAME = x.rstrip()
    filee = ROOT.TFile.Open(NAME)

    if( decay not in NAME):
      continue
    

    NAME_changed = os.path.relpath(NAME,'/work-zfs/lhc/heshy/anomalouscouplings/step3_withdiscriminants/200205_2018/')
    print NAME_changed
    out_name = "./ExtraBackgroundTemps/"+decay+"_"+category+"_"+str(NAME_changed)
    fout = ROOT.TFile.Open(out_name,"recreate")
    
    fout.cd()
    tf = tempFile(NAME)

    #set template hist binning etc
    ggZZ_yield = -1 
    h_name = ""
    if category == "Boosted" :
      back_file = ROOT.TFile.Open("/work-zfs/lhc/heshy/anomalouscouplings/step7_templates/200205_2018/templates_background_fa3fa2fL1fL1Zg_morecategories_"+str(decay)+"_Boosted_200205_2018.root")
      h_temp = back_file.Get("templateggZZ")
      h_name = h_temp.GetName()
      ggZZ_yield = h_temp.Integral()
      h_clone = h_temp.Clone()
      h_clone.Reset()

    if category == "VHHadrtagged" :
      back_file = ROOT.TFile.Open("/work-zfs/lhc/heshy/anomalouscouplings/step7_templates/200205_2018/templates_background_fa3fa2fL1fL1Zg_morecategories_"+str(decay)+"_VHHadrtagged_200205_2018.root")
      h_temp = back_file.Get("templateggZZMirror")
      h_name = h_temp.GetName()
      ggZZ_yield = h_temp.Integral()
      h_clone = h_temp.Clone()
      h_clone.Reset()


    if category == "VHLepttagged" :      
      back_file = ROOT.TFile.Open("/work-zfs/lhc/heshy/anomalouscouplings/step7_templates/200205_2018/templates_background_fa3fa2fL1fL1Zg_morecategories_"+str(decay)+"_VHLepttagged_200205_2018.root")
      h_temp = back_file.Get("templateggZZ")
      h_name = h_temp.GetName()
      ggZZ_yield = h_temp.Integral()
      h_clone = h_temp.Clone()
      h_clone.Reset()


    if category == "Untagged" :
      back_file = ROOT.TFile.Open("/work-zfs/lhc/heshy/anomalouscouplings/step7_templates/200205_2018/templates_background_fa3fa2fL1fL1Zg_morecategories_"+str(decay)+"_Untagged_200205_2018.root")
      h_temp = back_file.Get("templateggZZMirror")
      h_name = h_temp.GetName()
      ggZZ_yield = h_temp.Integral()
      h_clone = h_temp.Clone()
      h_clone.Reset()



    if category == "VBFtagged":
      back_file = ROOT.TFile.Open("/work-zfs/lhc/heshy/anomalouscouplings/step7_templates/200205_2018/templates_background_fa3fa2fL1fL1Zg_morecategories_"+str(decay)+"_VBFtagged_200205_2018.root")
      h_temp = back_file.Get("templateggZZMirror")
      h_name = h_temp.GetName()
      ggZZ_yield = h_temp.Integral()
      h_clone = h_temp.Clone()
      h_clone.Reset()


    if category == "VBF1jtagged":      
      back_file = ROOT.TFile.Open("/work-zfs/lhc/heshy/anomalouscouplings/step7_templates/200205_2018/templates_background_fa3fa2fL1fL1Zg_morecategories_"+str(decay)+"_VBF1jtagged_200205_2018.root")
      h_temp = back_file.Get("templateggZZ")
      h_name = h_temp.GetName()
      ggZZ_yield = h_temp.Integral()
      h_clone = h_temp.Clone()
      h_clone.Reset()


    

    events_tree = filee.Get("candTree")
    nentries = events_tree.GetEntries()
    h_m4l =  ROOT.TH1F("h_m4l","m_4l",200,100,300)
    h_m4l_pre =  ROOT.TH1F("h_m4l_pre","m_4l",200,100,300)
    for indx,event in enumerate(events_tree):
      perc = float(indx)/nentries*100
      sys.stdout.write('Analyze [%d%%]\r'%perc)
      sys.stdout.flush()
  
      leptonflavors = False
      selections = False
      weight  = event.MC_weight_nominal*event.p_Gen_GG_BKG_MCFM
      h_m4l.Fill(event.ZZMass,weight)
      h_m4l_pre.Fill(event.ZZMass)
      
      
      if decay == "4mu":
        leptonflavors = ((event.ZZMass>105 and event.ZZMass<140) and ( event.Z1Flav*event.Z2Flav == 28561) )       
      if decay == "4e":
        leptonflavors = ((event.ZZMass>105 and event.ZZMass<140) and ( event.Z1Flav*event.Z2Flav == 14641))          
      if decay == "2e2mu" :
        leptonflavors = ((event.ZZMass>105 and event.ZZMass<140) and ( event.Z1Flav*event.Z2Flav == 20449))         


      #categories   
      if category == "Boosted" :
        selection  = ( event.category_0P_or_0M_or_a2_or_L1_or_L1Zg == 8)
        if selection and leptonflavors: 
          x = event.ZZPt 
          y = event.phistarZ2 
          z = event.D_bkg
          h_clone.Fill(x,y,z,weight)


      if category == "VHHadrtagged" :
        selection  =  (event.category_0P_or_0M_or_a2_or_L1_or_L1Zg == 4)
        if selection and leptonflavors: 
          x = event.D_4couplings_HadVHdecay 
          y = event.D_CP_HadVH 
          z = event.D_bkg_HadVHdecay
          h_clone.Fill(x,y,z,weight)        

      if category == "VHLeptagged" :
        selection = (event.category_0P_or_0M_or_a2_or_L1_or_L1Zg == 3) 
        if selection and leptonflavors: 
          x = event.ZZPt 
          y = event.phistarZ2 
          z = event.D_bkg
          h_clone.Fill(x,y,z,weight)


      if category == "Untagged" :
        selection = (event.category_0P_or_0M_or_a2_or_L1_or_L1Zg == 0 or event.category_0P_or_0M_or_a2_or_L1_or_L1Zg == 5 or event.category_0P_or_0M_or_a2_or_L1_or_L1Zg == 6 or event.category_0P_or_0M_or_a2_or_L1_or_L1Zg == 7  )
        if selection and leptonflavors: 
          x  = event.D_4couplings_decay 
          y  = event.D_CP_decay
          z  = event.D_bkg
          h_clone.Fill(x,y,z,weight)


      if category == "VBFtagged":
        selection = (event.category_0P_or_0M_or_a2_or_L1_or_L1Zg == 2)
        if selection and leptonflavors: 
          x = event.D_4couplings_VBFdecay
          y = event.D_CP_VBF 
          z = event.D_bkg_VBFdecay
          h_clone.Fill(x,y,z,weight)



      if category == "VBF1jtagged":
        selection = (event.category_0P_or_0M_or_a2_or_L1_or_L1Zg == 1)
        if selection and leptonflavors: 
          x = event.ZZPt
          y = event.phistarZ2
          z = event.D_bkg
          h_clone.Fill(x,y,z,weight)

    intt = h_clone.Integral()
    if intt != 0 : 
      print decay,category, "event : ", intt
      h_clone.Scale(ggZZ_yield/intt)


    fout.cd()
    h_clone.Write(h_name,ROOT.TObject.kOverwrite)
    #h_m4l.Write("h_m4l",ROOT.TObject.kOverwrite)
    #h_m4l_pre.Write("h_m4l_pre",ROOT.TObject.kOverwrite)
    
