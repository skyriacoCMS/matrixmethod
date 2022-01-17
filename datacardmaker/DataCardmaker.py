import os
import sys
import json
import ROOT
import math
import copy
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH3F
from Unroll import Unroll
from ReadJsonYields import *   #ReadJsonweights
from Class_Templatefiles import tempFile,tempHist



name = sys.argv [1]
f = ROOT.TFile.Open(name)
obs_data = 0

print name

tf = tempFile(name)
decaymode = tf.GetDMode()
category  = tf.GetCategory()
year,l_scale = tf.GetYearandLumi()
lumi = ".lumi"+str(l_scale)
binname = "hzz4l_"+decaymode+"S_"+category+"_"+year
datacardname ="./TempsandCards/hzz4l_"+decaymode+"S_"+category+"_"+year+lumi+".txt"
temp_output_name ="./TempsandCards/hzz4l_"+decaymode+"S_"+category+"_"+year+".input.root"

#Defining fields for Data card and filling the,
b_name = []
p_name = []
p_rate = []
p_index = []
p_unclist = []
#SetUp Uncertainty lists
#read from txt the type of uncertainties. 
name_sys = "./data/sys_"+category+"_"+decaymode+"_"+year+".txt"
f_sys = open(name_sys,"r")
for item in f_sys:
      p_unclist.append([item.rstrip(),"lnN"])
#print p_unclist






#Write out new template root file
f_temp_out = ROOT.TFile.Open(temp_output_name,"RECREATE")
f_temp_out.cd()

int_SM = []
nBckgr = 0
pure_n = 0
removeffVH = 0

h_names_list = []

for key in f.GetListOfKeys():
   if "TH3F" in key.GetClassName():
    h_name = key.GetName()
    h_temp = f.Get(h_name)

    if "L1Zg" in h_name or "ghzgs1prime" in h_name:
          continue

    
    
    
    if "Dn" not in h_name and "Up" not in h_name and "Down" not in h_name :
       #histograms to contruct systematics for
       h_names_list.append(h_name)
    

    

       h_name = h_name.replace("Hff0MinusHVV","Hff")
    
       if "background" in h_name: 
             nBckgr = nBckgr + 1
       if "L1" in h_name   or "0Plus" in h_name or "0Minus" in h_name  or "0HPlus" in h_name:      
             pure_n =  pure_n + 1
 
       if "0Plus" in h_name:
             integ = h_temp.Integral()
             thist = tempHist(h_name)
        
             rpoc = thist.GetPMode()
             #print "rporc",rpoc," ",h_name
             int_SM.append([rpoc,integ])

       if "VH_Hff" in h_name:
             removeffVH = removeffVH + 1

             
h_procit =  2*nBckgr + 2 + pure_n   -2*(len(f.GetListOfKeys()))   # +2 is for the Data being removed from the processes
bkg_in = 1
h_proci = 0
tot_new = 0

hist_syst = []
shape_unc = []
shape_unc_withproc = []

#############################################################################################################
#                                                                                                           #
#  Shape Systematics - construct from nominals and shapes and create lists to write to datacard and output  #
#                                                                                                           #
#############################################################################################################

for key in f.GetListOfKeys():
        
        #Scale Systematic plots
        if "TH3F" in key.GetClassName() :
           h_name = key.GetName()


           if "L1Zg" in h_name or "ghzgs1prime" in h_name:
                continue
           


                 
           if "Dn" in h_name or "Down" in h_name or "Up" in h_name: 
           
              h_tempp = f.Get(h_name)
              h_temp = h_tempp.Clone()
              thist = tempHist(h_name)
              process = thist.GetPMode()
              if h_temp.Integral() < 1.0e-6 :
                    continue


              #define syst name
              
              name_comp    = h_name.split("_")
              nominal_name = process+"_"+name_comp[1]
              if "ggH" in process and "Hff0MinusHVV" in h_name :
                    nominal_name = "ggH_"+name_comp[1].replace("Hff0MinusHVV","")
              if "ttH" in process and "Hff0MinusHVV" in h_name :
                    nominal_name = "ttH_"+name_comp[1].replace("Hff0MinusHVV","")
              h_nominall = f.Get(nominal_name)
              print nominal_name
              h_nominal = h_nominall.Clone()
              
              #print "nominal  : "
              #if "background" in h_temp.GetName(): 
              #      print "nominal  : ",h_nominal.GetName(), h_nominal.Integral()
              #      print "nominal  : ",h_temp.GetName(), h_temp.Integral()

              syst_name=""
               
              if "THU" not in h_name: 
                 syst_name = "CMS_"
              else:
                 #theory (?)  uncertainties for ggH
                 if "Mig01" in h_name : 
                    syst_name = "THUMig01"
                 if "Mig12" in h_name : 
                    syst_name = "THUMig12"
                 if "PT120" in h_name :
                    syst_name = "THUPT120"
                 if "PT60" in h_name :
                    syst_name = "THUPT60"
                 if "qmtop" in h_name :
                    syst_name = "THUqmtop"
                 if "Res" in h_name :
                    syst_name = "THURes"
                 if "VBF2j" in h_name :
                    syst_name = "THUVBF2j"
                 if "VBF3j" in h_name :
                    syst_name = "THUVBF3j"
                 if syst_name == "" :
                    print "new syst not listed!"
                    print h_name


                    
              if "Scale" in h_name and "THU" not in h_name: 
                 syst_name = syst_name + "scale"+decaymode
              elif "Res" in h_name and "THU" not in h_name:
                 syst_name = syst_name + "res"+decaymode
              elif "JEC" in h_name:
                 if process == "background" : 
                    syst_name = syst_name + "jec_0plus"
             
                 else :    
                    syst_name = syst_name + "jec"

              if "0Plus" in h_name and "JEC" in h_name: 
                 syst_name = syst_name +"_0plus"
                 

              if "0HPlus" in h_name and "JEC" in h_name:
                 syst_name = syst_name +"_0hplus"
                 

              if ( "_0Minus" in h_name or "HVV0Minus" in h_name ) and "JEC" in h_name: 
                 syst_name = syst_name +"_0minus"
              if "0L1" in h_name and "JEC" in h_name and "JEC" in h_name:
                    syst_name = syst_name +"_0lambda1"
                    

              # Create list of shape syst to add to datacard   
              # check if syst already in list and write if not
              pass_m = True
              #print h_name,syst_name
              
              for item in shape_unc:
                 if item[0] == syst_name :
                    pass_m = False
                    break
              if pass_m :
                 shape_unc.append([syst_name,"shape1?"])
                 shape_unc_withproc.append([syst_name])
                 
                 
                 
              syst_name_pre = syst_name

              if "Dn" in h_name or "Down" in h_name :
                 syst_name = syst_name +"Down"
              else:
                 syst_name = syst_name +"Up"

                 
              for hhist  in h_names_list  :

                 thist_pr = tempHist(hhist)
                 process_pr = thist_pr.GetPMode()
                 
                 if process_pr == process :
                       
                    #process fails to distinguish different backgrounds alone   
                    if "background" in h_name :  
                          splproc = h_name.split("_JEC") 
                          if splproc[0] != hhist :
                                continue
                                                 
                    hist_proce_s = f.Get(hhist)
                    hist_proces = hist_proce_s.Clone()
                    pr_name = hist_proces.GetName()


                    ###############################################################
                    #  need to rescale also the other inputs to the constr of the syst
                    ###############################################################

                    
                    if not ("data" in pr_name ) and not ("Data" in pr_name) : 
                 
                          if "background" in pr_name and not "ZX"  in pr_name :
                                intgr = hist_proces.Integral()
                                hist_proces.Scale(1./intgr)
                                             
                    SM_scale = -1.              
                    if not (process ==  "background"  ):     
                          for item in int_SM:
                                if item[0] == process:
                                      SM_scale = item[1]
                    if "background" in pr_name:
                        if "ZX" in pr_name: 
                              h_proci = bkg_in 
                              bkg_in =  bkg_in + 1
                              hist_proces.Scale(1./l_scale)
                              scale_p = ReadJsonweights(year,category,decaymode,"ZX") 
                        if "qqZZ" in pr_name: 
                              h_proci = bkg_in 
                              bkg_in =  bkg_in + 1
                              scale_p = ReadJsonweights(year,category,decaymode,"qqZZ") 
                              hist_proces.Scale(scale_p)

                        if "EW" in pr_name: 
                              h_proci = bkg_in 
                              bkg_in =  bkg_in + 1
                              scale_p = ReadJsonweights(year,category,decaymode,"EW") 
                              hist_proces.Scale(scale_p)
                              
                        if "ggZZ" in pr_name: 
                              h_proci = bkg_in 
                              bkg_in =  bkg_in + 1
                              scale_p = ReadJsonweights(year,category,decaymode,"ggZZ")
                              hist_proces.Scale(scale_p)
                              
                    if not( "background" in pr_name ) and  not( "data" in pr_name  ) and not( "Data" in pr_name ):
                          #print pr_name
                          scale_p = -9999.
                          scale_p = ReadJsonweights(year,category,decaymode,process)
                          
                          if (SM_scale == -1 ) or ( scale_p == -9999.):
                                print "BAD SM scale"
                          hist_proces.Scale(scale_p/SM_scale)
                          
                    ###############################################################     
                    #End of rescale nominal before constructing the systematic hist
                    ###############################################################

                    hist_proces.Scale(l_scale)
                    
                    new_sys_temp = h_temp.Clone()
                    new_sys_temp.Reset()
                    
                    cont_sys = 0
                    for item in shape_unc_withproc :
                       
                       if item[0] == syst_name_pre :                          

                          if "jec_0lambda1" in syst_name_pre:
                               pnott1 = True
                               proc_bkg1 = "qqzz"
                               pnott2 = True
                               proc_bkg2 = "ggzz"                               
                               for jtem in item :
                                     if jtem == proc_bkg1 :
                                           pnott1 = False
                                     if jtem == proc_bkg2 :
                                           pnott2 = False
                                     
                               if pnott1 :
                                     shape_unc_withproc[cont_sys].append(proc_bkg1)
                               if pnott2 :
                                     shape_unc_withproc[cont_sys].append(proc_bkg2)
                               

                          if "jec_0hplus" in syst_name_pre:
                               pnott1 = True
                               proc_bkg1 = "qqzz"                               
                               pnott2 = True
                               proc_bkg2 = "ggzz"                               
                               for jtem in item :
                                     if jtem == proc_bkg1 :
                                           pnott1 = False
                                     if jtem == proc_bkg2 :
                                           pnott2 = False
                                    
                               if pnott1 :
                                     shape_unc_withproc[cont_sys].append(proc_bkg1)
                               if pnott2 :
                                     shape_unc_withproc[cont_sys].append(proc_bkg2)
                               
                          if "jec_0minus" in syst_name_pre:
                               pnott1 = True
                               pnott2 = True
                               proc_bkg1 = "qqzz"
                               proc_bkg2 = "ggzz"                               
                               for jtem in item :
                                     if jtem == proc_bkg1 :
                                           pnott1 = False
                                     if jtem == proc_bkg2 :
                                           pnott2 = False
                               if pnott1 :
                                     shape_unc_withproc[cont_sys].append(proc_bkg1)
                               if pnott2 :
                                     shape_unc_withproc[cont_sys].append(proc_bkg2)
                               
                                     
                          pass_not = True
                          for jtem in item :
                             if jtem == process_pr :
                                pass_not =  False
                          if pass_not  :       
                                shape_unc_withproc[cont_sys].append(process_pr)
                                break

                                      

                             
                          
                        
                    
                       cont_sys = cont_sys +1    
                    has_smallvalues = False
                    ratio = h_temp.Integral()/h_nominal.Integral()
                    for x in range(1,h_nominal.GetNbinsX() +1):
                       for y in range(1,h_nominal.GetNbinsY() +1):
                          for z in range(1,h_nominal.GetNbinsZ() +1 ):
                             nominalcont  = float(h_nominal.GetBinContent(x,y,z))
                             proccont = float(hist_proces.GetBinContent(x,y,z))
                             systcont = float(h_temp.GetBinContent(x,y,z))
                             if abs(proccont) < 1e-05 or abs(systcont) < 1e-05 :
                                   has_smallvalues =  True
                                   cont = proccont #*ratio                                   
                                   if "Up" in h_name  :
                                      cont  =  cont + 0.00001
                                   if ("Dn" in h_name or "Down" in h_name  )  :
                                      cont =  cont +0.00001 
                              
                             else : 
                                   cont = float((proccont*systcont)/(nominalcont*1.0))

                             hhh = new_sys_temp.GetName()      
                             #if ("VH" in hhh and "jec_0lambda1" in syst_name_pre and "g13g1prime2" in hhist ):
                             #     print ">",cont," here :",nominalcont,proccont,systcont," ",hhist," ",syst_name     
                             new_sys_temp.SetBinContent(x,y,z,cont)

                    #if ("jec_0lambda1" in syst_name_pre and "g13" in hhist and "VH" in hhh ):
                    #      print "hist:",hhist," int:",new_sys_temp.Integral()
                          
                    #fix rediculous systematics that exceed 1000%         
                    if  h_nominal.Integral() > 0 and hist_proces.Integral() > 0 :
                          if ( new_sys_temp.Integral() /hist_proces.Integral() > 2*h_temp.Integral()/h_nominal.Integral()) :
                                new_sys_temp = hist_proces.Clone()
                                ratioN = h_temp.Integral()/h_nominal.Integral()
                                new_sys_temp.Scale(ratioN)
                                                             
                    tempname = new_sys_temp.GetName()
                    new_name = hhist+"_"+syst_name
                    new_sys_temp.SetName(new_name)

                    #check syst magnitude
                    if ( hist_proces.Integral() > 0) :
                          if ( new_sys_temp.Integral() /hist_proces.Integral() > 1.7   ):
                                print new_sys_temp.GetName(),h_nominal.GetName(), hist_proces.GetName()
                                print new_sys_temp.Integral(), h_nominal.Integral(), hist_proces.Integral(),"  ratio:", h_temp.Integral()/h_nominal.Integral(),new_sys_temp.Integral() /hist_proces.Integral()
                                print "BAD systematic scaling"
                    
                    #####################################################
                    #unroll histogram and append to write at the end.   #
                    #####################################################
                    new_temp_neg,new_temp_pos = Unroll(new_sys_temp)  #the function returns two urolled histograms and fixes their names
                    #if ("jec_0lambda1" in syst_name_pre and "g13" in hhist and "VH" in hhh ):
                    #      print "hist:",hhist," int: neg",new_temp_neg.Integral()," pos ",new_temp_pos.Integral(),
         
                    new_name = new_temp_pos.GetName()
                    if "positive" in new_name :
                       namelist = new_name.split("_")
                       newnew_name=""
                       newnew_name_negative=""

                       

                       newnew_name = namelist[0]+"_"+ namelist[1]+"_positive_"+syst_name
                       newnew_name_negative = namelist[0]+"_"+ namelist[1]+"_negative_"+syst_name
                       if "ff" in new_name:
                          lenn = len(namelist) -1
                          newnew_name = namelist[0]+"_"+ namelist[1]+"_"+namelist[2]+"_positive_"+syst_name
                          newnew_name_negative = namelist[0]+"_"+ namelist[1]+"_"+namelist[2]+"_negative_"+syst_name
                       new_temp_pos.SetName(newnew_name)
                       new_temp_neg.SetName(newnew_name_negative)
                       
                    new_name = new_temp_neg.GetName()   
                    if "negative" in new_name and not(new_temp_neg.Integral() == 0) :
                       hist_syst.append(new_temp_neg)

                    #if "ttH" in  new_temp_pos.GetName():
                       #print new_temp_pos.GetName()
                    if ("Up" not in new_temp_pos.GetName() ) and ("Down" not in new_temp_pos.GetName() ):
                          print "Warning bad systematics name"      
                    if new_temp_pos.Integral() > 0 :       
                        hist_syst.append(new_temp_pos)


#############################################################################################################
#                                                                                                           #
#  Process histograms and define datacard entries                                                           #
#                                                                                                           #
#############################################################################################################

#
print shape_unc_withproc

                    
for key in f.GetListOfKeys():
        h_name = key.GetName()
        h_temp = f.Get(h_name)

        #now loop over all process hist not the syst and unroll, write to file and datacard   
        if "TH3F" in key.GetClassName() and not("VH_Hff" in h_name)  :
                #scale to lumi
                thist = tempHist(h_name)
                
                if "L1Zg" in h_name or "ghzgs1prime" in h_name:
                      continue
                if "Dn" in h_name or "Down" in h_name or "Up" in h_name:
                   continue
                
                if not ("data" in h_name ) and not ("Data" in h_name) : 

                   if "background" in h_name and not "ZX"  in h_name :
                      intgr = h_temp.Integral()
                      h_temp.Scale(1./intgr)
                   h_temp.Scale(l_scale)


                process = thist.GetPMode()
                SM_scale = -1.    
                if not (process ==  "background"  ):     
                    for item in int_SM:
                        if item[0] == process:
                            SM_scale = item[1]
                if "background" in h_name:
                          if "ZX" in h_name: 
                                  h_proci = bkg_in 
                                  bkg_in =  bkg_in + 1
                                  h_temp.Scale(1./l_scale)
                                  scale_p = ReadJsonweights(year,category,decaymode,"ZX") 
                                 # h_temp.Scale(scale_p)

                          if "qqZZ" in h_name: 
                                  h_proci = bkg_in 
                                  bkg_in =  bkg_in + 1
                                  scale_p = ReadJsonweights(year,category,decaymode,"qqZZ") 
                                  #print scale_p
                                  h_temp.Scale(scale_p)
                          if "EW" in h_name: 
                                  h_proci = bkg_in 
                                  bkg_in =  bkg_in + 1
                                  scale_p = ReadJsonweights(year,category,decaymode,"EW") 
                                  #print scale_p
                                  h_temp.Scale(scale_p)
                          if "ggZZ" in h_name: 
                                  h_proci = bkg_in 
                                  bkg_in =  bkg_in + 1
                                  scale_p = ReadJsonweights(year,category,decaymode,"ggZZ")
                                  #print scale_p
                                  h_temp.Scale(scale_p)

                if not( "background" in h_name ) and  not( "data" in h_name  ) and not( "Data" in h_name ):

                   #print h_name
                   scale_p = ReadJsonweights(year,category,decaymode,process)
                   h_temp.Scale(scale_p/SM_scale)
                    

                    
                if "data" in h_name or "Data" in h_name:

                    h_temp.SetName("Data")
                    obs_data = h_temp.Integral()
                ###################################################
                #                                                 #
                #     Unroll histogram and fix it's name          # 
                #                                                 #
                ###################################################
                new_temp_neg,new_temp_pos = Unroll(h_temp)
                ngname = new_temp_neg.GetName()
                pname  =  new_temp_pos.GetName()


                #print pname
                if not (category == "VBFtagged" or category == "VHHadrtagged"  ) and not ( "ttH" in pname):
                   
                   ngname = ngname.replace("_0PMff_","_")
                   pname  = pname.replace("_0PMff_","_")
                   ngname = ngname.replace("_0Mff_","_")
                   pname  = pname.replace("_0Mff_","_")
                   new_temp_neg.SetName(ngname)
                   new_temp_pos.SetName(pname)
                
                
                if "data" in h_name:
                   new_temp_pos.Write()
                   
                if not "data" in h_name :
                      if not( new_temp_pos.Integral() == 0 ):  
                         new_temp_pos.Write()
                         p_rate.append(new_temp_pos.Integral())
                         p_name.append(new_temp_pos.GetName())
                         b_name.append(binname)
                         #############################################
                         #            ADD scale Systematics          #
                         #############################################
                         

                         for item in p_unclist:
                            procc_ = process
                            if process == "background" :
                               if "ZX" in h_name:
                                  procc_ = "ZX"
                               if "qqZ" in h_name:
                                  procc_ = "qqZZ"
                               if "ggZ" in h_name:
                                  procc_ = "ggZZ"
                               if "EW"  in h_name:
                                  procc_ = "ew"   
                               
                               
                            value = ReadJsonsystematics(item[0],year,category,decaymode,procc_)
                            if value is not None:
                               if isinstance( value, list):
                                  item.append(str(value[0])+'/'+str(value[1]))
                               else:                                  
                                  if value != -1 : 
                                     item.append(str(value))
                                  else :
                                     item.append("-")
                            else:
                               item.append("-") 
                      

                         tot_new = tot_new +1
                         if "background" in h_name  :
                            p_index.append(h_proci)
                         else:
                            h_procit  = h_procit + 1
                            p_index.append(h_procit)

                         ######################################################################   
                         #  check if process in shape systematic and add to list for datacard #
                         ######################################################################
                         sys_cont = 0

                         for item in shape_unc:
                               for sys_item in shape_unc_withproc :
                                     if str(sys_item[0]) == str(item[0]):

                                           has_theproc = False

                                           for jproc in sys_item:
                                                 if jproc == process :
                                                       has_theproc =  True
                                                       break 
                                           if has_theproc :
                                                 
                                                 if "ZX" in h_name and "jec" in str(item[0]):
                                                       item.append("-")
                                                 else :
                                                       item.append("1")
                                                       
                                           else :
                                                 if "qqZZ" in h_name  and "jec" in str(item[0]):
                                                       item.append("1")
                                                 elif "ggZZ" in h_name  and "jec" in str(item[0]):
                                                       item.append("1")
                                                 elif "EW" in h_name  and "jec" in str(item[0]):
                                                       item.append("1")
                                                 else :
                                                       item.append("-")
                         
                      nname = new_temp_neg.GetName()        
                      if "negative" in nname and not(new_temp_neg.Integral() == 0) :                        
                              p_rate.append(new_temp_neg.Integral())
                              p_name.append(new_temp_neg.GetName())
                              b_name.append(binname)
                              
                              for item in p_unclist:
                                 procc_ = process
                                 if process == "background" :
                                    if "ZX" in h_name:
                                       procc_ = "ZX"
                                    if "qqZ" in h_name:
                                       procc_ = "qqZZ"
                                    if "EW" in h_name:
                                       procc_ = "ew"
                                    if "ggZ" in h_name:
                                       procc_ = "ggZZ"
                               
                               
                                 value = ReadJsonsystematics(item[0],year,category,decaymode,procc_)
                                 if value is not None :
                                    if isinstance( value, list):
                                       item.append(str(value[0])+'/'+str(value[1]))
                                    else:
                                       if value != -1 : 
                                          item.append(str(value))
                                       else :
                                          item.append("-")
                                 else:
                                    item.append("-") 
                              
                              new_temp_neg.Write()
                              tot_new = tot_new +1
                              if "background" in h_name    :
                                  h_proci = bkg_in 
                                  bkg_in =  bkg_in + 1
                                  p_index.append(h_proci)
                              else:
                                  h_procit  = h_procit + 1
                                  p_index.append(h_procit)

                              ######################################################################   
                              #  check if process in shape systematic and add to list for datacard #
                              ######################################################################
                              
                              
                              for item in shape_unc:
                               for sys_item in shape_unc_withproc :
                                     if str(sys_item[0]) == str(item[0]):

                                           has_theproc = False

                                           for jproc in sys_item:
                                                 if jproc == process :
                                                       has_theproc =  True
                                                       break 
                                           if has_theproc :
                                                 if "ZX" in h_name and "jec" in str(item[0]):
                                                       item.append("-")
                                                 else :
                                                       item.append("1")

                                                 
                                           else :
                                                 if "qqZZ" in h_name  and "jec" in str(item[0]):
                                                       item.append("1")
                                                 elif "ggZZ" in h_name  and "jec" in str(item[0]):
                                                       item.append("1")
                                                 elif "EW" in h_name  and "jec" in str(item[0]):
                                                       item.append("1")
                                                 else :
                                                       item.append("-")
                               
                
                

######################################################################   
#  Write the shape unc hists to root file                            #
###################################################################### 
for h_temp in hist_syst :
   syst_name = h_temp.GetName()
   if "Up" not in syst_name and "Down" not in syst_name:
      print syst_name
      print "Warning Systematic templates need Up or Down end-fix "

   #now duplicate the SM background CMS shape uncertainties for the anomalous couplings as when anomalous JEC is floated the background is floated too.
   #correspondigly the background index should be turned to 1 for these uncertainties to be considered in each CMS_jec_*anomaloiuscoupling*
   if "bkg" in syst_name and "CMS_jec" in syst_name:    
         
         
         h1 = h_temp.Clone()
         h2 = h_temp.Clone()
         h3 = h_temp.Clone()

         h1_name = syst_name.replace("0plus","0minus")
         h2_name = syst_name.replace("0plus","0hplus")
         h3_name = syst_name.replace("0plus","0lambda1")

         
         h1.SetName(h1_name)
         h2.SetName(h2_name)
         h3.SetName(h3_name)
         
         h1.Write()
         h2.Write()
         h3.Write()
         
         
   h_temp.Write()

f_temp_out.Close()



######################################################################   
#  Write the Datacard                                                #
######################################################################


fout = open(datacardname,"w")
fout.write("imax  1  \n")
fout.write("jmax "+str(tot_new -1)+" \n")
fout.write("kmax *   \n")
fout.write("-------- \n")
fout.write("shapes * * "+binname+".input.root $PROCESS $PROCESS_$SYSTEMATIC  \n")
fout.write("-------- \n")
fout.write("bin "+binname+"\n")
fout.write("observation ")
fout.write( str(obs_data) )
fout.write("\n")

fout.write("-------- \n")
fout.write("bin ")



if len(b_name) != len(p_name):
   print "wrong sizes"

if len(p_name) != len(p_rate):
   print "wrong sizes"


for item in b_name:
        fout.write(str(item)+" ")
fout.write("\n")
fout.write("process ")
for item in p_name:
        fout.write(str(item)+" ")
fout.write("\n")
fout.write("process ")
for item in p_index:
        fout.write(str(item)+" ")
fout.write("\n")
fout.write("rate ")
for item in p_rate:
        fout.write(str(item)+" ")
fout.write("\n")
fout.write("-------- \n")



########################################################################
#     
#     Write scale systematic to data card but need
#     to merge with shape if they are mixed (THU)
#     
########################################################################


#print "scale unc"
skip_shapeunc = []


for item in p_unclist:
   typpe =  str(item[0])
   match_ = False
   shape_unn = []

   if len(item) >  len(p_name) + 2:
         print len(item), len(p_name), len(b_name)
         print "BIG issue ", item[0]
         

   
   if "THU_ggH" in typpe :
      
      write_= str(item[0])
      write_= write_.replace("THU_ggH_","THU")
      shcont = 0
      for shape_item in shape_unc:
          
          if write_ == str(shape_item[0]):
            
            match_ = True
            shape_unn = shape_item
            skip_shapeunc.append(shcont)
          shcont = shcont + 1

   cont_scale = 0   
   for sitem in item: 
      
      if "THU" in str(sitem) :
         write_= str(sitem)
         write_= write_.replace("THU_ggH_","THU")
      else :
         write_ = str(sitem)
      if cont_scale == 1 and match_ :
         
         write_="shape1?"   
      if match_  :
         if str(sitem) ==  "-":
            if shape_unn[cont_scale] == "1" :
               write_ = "1"
         elif "/" in str(sitem):
               write_ = "1"
      #if cont_scale == 1 and match_ :
      #      print  "THIS :", write_   
      fout.write(write_+" ")
      cont_scale = cont_scale +1
   fout.write("\n")
########################################################################
#     write shape syst to Datacard
#     also skip if the shape systematic
#     has been introduced as a mixed syst.
########################################################################

shcont = 0
print "shape unc",len(shape_unc)


for item in shape_unc:

   if len(item) > len(p_name) +2:
         print len(item), len(p_name), len(b_name)
         print "BIG issue ", item[0]
   pass_num = True
   for numm in skip_shapeunc :
      if shcont == int(numm) :
         pass_num = False 
   if pass_num :
      for sitem in item: 
         fout.write(str(sitem)+" ")
      fout.write("\n")
   shcont = shcont +1
      

  
fout.write("shapesystematics group = ")
for item in shape_unc:
   fout.write(str(item[0])+" ")
   
fout.write("\n")








