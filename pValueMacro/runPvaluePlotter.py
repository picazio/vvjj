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

runOverWS= True #Set to 'False' if you already have the output*.txt files
inputPreDir="/afs/cern.ch/work/y/yygao/public/VVJJWorkspaces/28Sep2016/"
#inputName = "CxAOD_23Sep2016_13p3ifb_NoTrk"
inputName = "CxAOD_23Sep2016_13p3ifb"
lumitag = "13p3"
#lumitag = ""
models_dic={
    "HVT":["WZ",1,2,1,"HVT W' #rightarrow WZ"],
    #"HVT":["WW",4,2,2,"HVT Z' #rightarrow WW"],
    #"Gravi":["WW",7,2,3,"G_{RS} #rightarrow WW"],
    #"Gravi":["ZZ",6,2,4,"G_{RS} #rightarrow ZZ"],
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
    functions.replaceArguments(tempRunningMacro,inputPreDir,inputName,lumitag,modeldic,models_dic[modeldic][0],hasNtrk)
    runCommand="root -l -b -q calcPvalue.C"
    if runOverWS :
        os.system(runCommand)
    outPutName="output_p0_"+inputName+"_"+modeldic+"_"+models_dic[modeldic][0]+".txt"
    models_dic[modeldic].append(outPutName)

functions.readOutputFilePValue(models_dic)
functions.createPValuePlot(models_dic,pValuePlotName,'.'.join(lumitag.split('p'))+" fb^{-1}")
