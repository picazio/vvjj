#############################
#Before running me, make sure to:
# source setup.sh
#and to have all the settings written correctly 
#To run just type:
#
#python runPvaluePlotter.py
#
##### Have fun!!!

############################# Settings area  ############################

runOverWS= False #Set to 'False' if you already have the output*.txt files
#inputPreDir="/afs/cern.ch/work/y/yygao/public/VVJJWorkspaces/28Sep2016/"
#inputName = "CxAOD_23Sep2016_13p3ifb_NoTrk"
#inputName = "CxAOD_23Sep2016_13p3ifb"
#lumitag = "13p3"

inputPreDir="/afs/cern.ch/work/y/yygao/public/VVJJWorkspaces/28July2016/"
#inputName = "CxAOD_23Sep2016_13p3ifb_NoTrk"
inputName = "CxAOD_28July2016_15p5ifb_nominal"
lumitag = "15p5"

#lumitag = ""
models_dic={
    "HVTWZ":["HVT","WZ",1,2,1,"HVT W' #rightarrow WZ"],
    "HVTWW":["HVT","WW",4,2,2,"HVT Z' #rightarrow WW"],
    "GraviWW":["Gravi","WW",7,2,3,"G_{RS} #rightarrow WW"],
    "GraviZZ":["Gravi","ZZ",6,2,4,"G_{RS} #rightarrow ZZ"],
    }
hasNtrk = True
pValuePlotName="pValueAll.pdf"
#########################################################################

#sub-settings Area - change only if strictly needed
nameMacro="calcPvalue_original.C"
tempRunningMacro="calcPvalue.C"

import os
import sys
cwd=os.getcwd()
sys.path.append(cwd)

import atlasStyleMacro
import functions

model_dic_key=models_dic.keys()

for imodeldic, modeldic in enumerate(model_dic_key) :

    cpCommand="cp "+nameMacro+" "+tempRunningMacro
    os.system(cpCommand)
    functions.replaceArguments(tempRunningMacro,inputPreDir,inputName,lumitag,models_dic[modeldic][0],models_dic[modeldic][1],hasNtrk)
    runCommand="root -l -b -q calcPvalue.C"
    if runOverWS :
        os.system(runCommand)
    outPutName="output_p0_"+inputName+"_"+models_dic[modeldic][0]+"_"+models_dic[modeldic][1]+".txt"
    models_dic[modeldic].append(outPutName)


    
functions.readOutputFilePValue(models_dic)
functions.createPValuePlot(models_dic,pValuePlotName,'.'.join(lumitag.split('p'))+" fb^{-1}")
