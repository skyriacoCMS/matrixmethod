from Class_Templatefiles import tempFile,tempHist
import ROOT
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH3F
import os
import re
import math


def SmoothBackground(decay, category, year):



  if year == "2016":
    inp = "back_2016"
  if year == "2017":
    inp = "back_2017"
  if year == "2018":
    inp = "back_2018"
  

    

  f = open(inp,"r") 
  contents = f.readlines()



  for x in contents:
    NAME = x.rstrip()
    if category not in NAME or year not in NAME or decay not in NAME :
      continue


    filee = ROOT.TFile.Open(NAME)
    NAME_changed = os.path.relpath(NAME,'/work-zfs/lhc/heshy/anomalouscouplings/step7_templates/200205_2018/')
    print NAME_changed
    out_name = "./BackgroundSmoothed/"+str(NAME_changed)
    fout = ROOT.TFile.Open(out_name,"recreate")

    fout.cd()
    tf = tempFile(NAME)
    for key in filee.GetListOfKeys():
        if "template" in key.GetName() and  "TH3F" in key.GetClassName() :
            h_name = key.GetName()

            print h_name
            temphist = filee.Get(h_name)
            
            if "templateZX" in h_name:
              ZX_name = "/work-zfs/lhc/heshy/anomalouscouplings/step7_templates/200205_"+str(year)+"/templates_background_fa3fa2fL1fL1Zg_morecategories_"+str(decay)+"_"+str(category)+"_shift_pm4l_200205_"+str(year)+".root"
              fileZX = ROOT.TFile.Open(ZX_name)
              temphist = fileZX.Get(h_name)
              print "replacing ZX with mass shift template"

            h_clone  = temphist.Clone()            
            h_clone.Reset()
            h_ggzz = temphist.Clone()
            h_ggzz.Reset()

            if "gg" in h_name :
              NAME_extra = "./ExtraBackgroundTemps/"+str(decay)+"/"+str(decay)+"_"+str(category)+"_"+str(year)+".root"
              extra_file = ROOT.TFile.Open(NAME_extra)
              print NAME_extra
              for key_x in extra_file.GetListOfKeys():
                if "template" in key_x.GetName() :
                  extra_name = key_x.GetName()
                  h_extra = extra_file.Get(extra_name)
                  yield_ggZ = float( temphist.Integral() )
                  h_ggzz = temphist.Clone()
                  h_ggzz.Add(h_extra)
                  int_newzz = float(h_ggzz.Integral() )
                  h_ggzz.Scale(yield_ggZ/int_newzz)
                  print int_newzz, yield_ggZ ,h_extra.Integral()," Final:", h_ggzz.Integral()

                  if ( not (int_newzz/yield_ggZ == 2 ) ) :
                    print "Warning: ", extra_name, h_name, " ", category,decay,int_newzz/yield_ggZ




            
            th = tempHist(h_name)
            
            projx = temphist.ProjectionX()
            projy = temphist.ProjectionY()
            projz = temphist.ProjectionZ()
            proj_int = projx.Integral() 
            nbinsx = projx.GetNbinsX()
            nbinsy = projy.GetNbinsX()
            nbinsz = projz.GetNbinsX()
            #print "bins :",nbinsx," ",nbinsy," ",nbinsz," ",h_clone.GetNbinsX()," ",h_clone.GetNbinsY()," ",h_clone.GetNbinsZ()
            
            
            tmen = temphist.GetEntries()
            tmin = temphist.Integral()

            
            #fix projection errors
            nbinsx = projx.GetNbinsX()  
            for i in range(0,nbinsx+1):
              x_val = projx.GetBinContent(i)
              binentr = tmen*x_val/tmin
              binerr  = math.sqrt(binentr)
              #now scale error to correct integral :
              binerr =  binerr*tmin/tmen
              if x_val < 0.000000001 :
                binerr = 0
            
              projx.SetBinError(i,binerr)
            nbinsy = projy.GetNbinsX()  
            for i in range(0,nbinsy+1):
              x_val = projy.GetBinContent(i)
               
              binentr = tmen*x_val/tmin
              binerr  = math.sqrt(binentr)
              #now scale error to correct integral :
              binerr =  binerr*tmin/tmen
              if x_val < 0.000000001 :
                binerr = 0
              projy.SetBinError(i,binerr)
            nbinsz = projz.GetNbinsX()  
            for i in range(0,nbinsz+1):
              x_val = projz.GetBinContent(i)
              binentr = tmen*x_val/tmin
              binerr  = math.sqrt(binentr)
              #now scale error to correct integral :
              binerr =  binerr*tmin/tmen
              if x_val < 0.000000001 :
                binerr = 0
              projz.SetBinError(i,binerr)

            
            

            projx.Scale(1./proj_int)
            projy.Scale(1./proj_int)
            projz.Scale(1./proj_int)

            #print projx.Integral()," ",temphist.Integral()
            nbinsx = projx.GetNbinsX()  
            for i in range(0,nbinsx+1):
              x_c = projx.GetXaxis().GetBinCenter(i)
              x_val = projx.GetBinContent(i)
              err_x = projx.GetBinError(i)

              nbinsy = projy.GetNbinsX()
              #print "Entries :",projx.GetEntries()," ",projx.Integral()
              for j in range(0,nbinsy+1):
                y_c = projy.GetXaxis().GetBinCenter(j)
                y_val = projy.GetBinContent(j)              
                nbinsz = projz.GetNbinsX()
                err_y = projy.GetBinError(j)
                for k in range(0,nbinsz+1):
                  z_c = projz.GetXaxis().GetBinCenter(k)
                  z_val = projz.GetBinContent(k)                  
                  err_z = projz.GetBinError(k)
                  prodd = x_val*y_val*z_val
                  err = 0
                  if(not (x_val == 0  or y_val == 0 or z_val == 0) ): 
                    #print "errors :",err_x/x_val,err_y/y_val,err_z/z_val
                    err = prodd*math.sqrt( (err_x/x_val)**2 + (err_y/y_val)**2 + (err_z/z_val)**2 )
                    #print "product:",err/prodd
                  ibin = h_clone.GetBin(i,j,k)
                  ibb = h_clone.FindBin(x_c,y_c,z_c)

                  #print ibin, ibb
                  #h_clone.GetBinXYZ(ibin,ibx,iby,ibz)
                  h_clone.SetBinContent(ibin,prodd)
                  h_clone.SetBinError(ibb,err)
                  
                  #print x_c,y_c,z_c,h_clone.GetXaxis().GetBinCenter(i),h_clone.GetYaxis().GetBinCenter(j),h_clone.GetZaxis().GetBinCenter(k)
                  #print "c :",h_clone.GetBinContent(ibin),"e :",h_clone.GetBinError(i,j,k),h_clone.GetBinError(ibb),err,prodd 
            fout.cd()
            if "ggZZ" not in h_name:

              h_clone.SetName(h_name)
              integr = h_clone.Integral()
              h_clone.Scale(proj_int/integr)
              #print h_clone.Integral(),temphist.Integral()                     
	      print "writting :", h_name, h_clone
              h_clone.Write(h_name,ROOT.TObject.kOverwrite)
            else :
              h_ggzz.SetName(h_name)
              integr = h_clone.Integral()
              print "writting :", h_name, h_ggzz
              h_ggzz.Write(h_name,ROOT.TObject.kOverwrite)

      


            




    
