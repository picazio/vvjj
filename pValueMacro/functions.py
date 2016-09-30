import os
import sys
from array import array
from ROOT import *
import fileinput

from tempfile import mkstemp
from shutil import move
from os import remove, close

cwd=os.getcwd()

sys.path.append(cwd)

import atlasStyleMacro

def readOutputFilePValue(output_dic) :
    for model in output_dic :
        f = open(output_dic[model][6], 'r')
        pValueResults={}
        for line in f :
            mass=float(line.split(' ')[0])
            value=[]
            if line.split(' ')[1]=="-nan" :
                value.append(float(0.5))
            else :
                value.append(float(line.split(' ')[1]))
            pValueResults[mass]=value[0]
        output_dic[model].append(pValueResults)
    

def createPValuePlot(input_dictionary,pvalue_plot_Name,lumiOnPlot) :
        #canvas definition
        c1 =TCanvas()#"c1", "c1"),10,32,800,600)
        gStyle.SetOptStat(0)
        gStyle.SetOptTitle(0)
        
        c1.SetFillColor(0)
        c1.SetBorderMode(0)
        c1.SetBorderSize(2)
        c1.SetLogy(1)
    
        c1.SetLeftMargin(0.14)
        c1.SetRightMargin(0.07)
        c1.SetTopMargin(0.05)
        c1.SetBottomMargin(0.13)
        c1.SetFrameBorderMode(0)

        poslg_x1=0.49
        poslg_y1=0.55+0.1
        poslg_x2=poslg_x1+(0.28)
        poslg_y2=poslg_y1+(0.37-0.1)
        
        l =TLegend(poslg_x1,poslg_y1,poslg_x2,poslg_y2)
        l.SetFillStyle(0)
        l.SetTextFont(42)
        l.SetTextSize(0.045)
        l.SetBorderSize(0)

        graphs=[None for _ in range(len(input_dictionary.keys()))]
        for model in input_dictionary :
                graph=TGraph()
                graph.SetNameTitle("g_p0_"+model, "p0_"+model)
                masses=input_dictionary[model][7].keys()
                masses.sort()
                for imass,mass in enumerate(masses) :
                        graph.SetPoint(imass,mass,input_dictionary[model][7][mass])
                graph.SetLineColor(input_dictionary[model][2])
                graph.SetLineWidth(input_dictionary[model][3])
                graph.SetLineStyle(input_dictionary[model][4])
                graphs[input_dictionary[model][4]-1]=graph
                

        for igraph,graph in enumerate(graphs) :
                if igraph==0 :
                        graph.Draw("AL")
                        
                        yAxis=graph.GetYaxis()
                        xAxis=graph.GetXaxis()

                        yAxis.SetTitle("Local p_{0}")
                        yAxis.SetNdivisions(505)
                        yAxis.SetRangeUser(1 - Math.gaussian_cdf(6),1e6)

                        xAxis.SetTitle("m_{JJ} [GeV]")
                        xAxis.SetNdivisions(505)

                else :
                        graph.Draw("L")
                l.AddEntry(graph,input_dictionary[graph.GetName().split('_')[2]][5],"L")

        atl =TLatex(0.18,0.87,"ATLAS")
        atl.SetNDC()
        atl.SetTextFont(72)
        atl.SetTextSize(0.06)
        atl.SetLineWidth(2)
        atl.Draw()

        int =TLatex(0.18,0.87,"             Internal")
        int.SetNDC()
        int.SetTextFont(42)
        int.SetTextSize(0.06)
        int.SetLineWidth(2)
        int.Draw()

        lum =TLatex(0.18,0.8,"#sqrt{s} = 13 TeV, "+lumiOnPlot)
        lum.SetNDC()
        lum.SetTextFont(42)
        lum.SetLineWidth(2)
        lum.Draw()
        
        line=TLine()
        line.SetLineWidth(1)
        line.SetLineStyle(2)
        line.SetLineColor(kRed)
        xmin = graphs[0].GetXaxis().GetXmin()
        xmax = graphs[0].GetXaxis().GetXmax()
        line.SetLineColor(kBlack)
        line.DrawLine(xmin, 1, xmax, 1)

        line.SetLineColor(kRed)
        line.DrawLine(xmin, 1 - Math.gaussian_cdf(0), xmax, 1 - Math.gaussian_cdf(0))

        t=TLatex()
        delta = (xmax - xmin) * 0.02
        t.DrawLatex(xmax + delta, (1 - Math.gaussian_cdf(0)) * 0.8, "#color[2]{0#sigma}")

        minLimit = 1 - Math.gaussian_cdf(6)
        
        n = 1;
        while (minLimit < 1 - Math.gaussian_cdf(n)) :
                line.DrawLine(xmin, 1 - Math.gaussian_cdf(n), xmax, 1 - Math.gaussian_cdf(n));
                cmd = "#color[2]{"+str(n)+"#sigma}"
                t.DrawLatex(xmax + delta, (1 - Math.gaussian_cdf(n)) * 0.4, cmd)
                n=n+1
        l.Draw("same")

        c1.SaveAs(pvalue_plot_Name)
        c1.SaveAs('.C'.join(pvalue_plot_Name.split('.pdf')))

def replaceArguments(targetFile,inputDir,input,lumitag,model,sel,hasNtrk) :
        replace(targetFile,"TString inputPreDir = \"\"","TString inputPreDir = \""+inputDir+"\"")
        replace(targetFile,"TString input = \"\"","TString input = \""+input+"\"")
        replace(targetFile,"TString lumitag = \"\"","TString lumitag = \""+lumitag+"\"")
        replace(targetFile,"TString model = \"\"","TString model = \""+model+"\"")
        replace(targetFile,"TString sel = \"\"","TString sel = \""+sel+"\"")
        if hasNtrk==True :
                replace(targetFile,"bool hasNtrk = false","bool hasNtrk = true")
        elif hasNtrk==False :
                replace(targetFile,"bool hasNtrk = false","bool hasNtrk = false")
                
        

def GetKeyObjects( self, dir = "" ):
        self.cd(dir)
        return [key.ReadObj() for key in gDirectory.GetListOfKeys()]

TFile.GetKeyObjects = GetKeyObjects

def GetKeyNames( self, dir = "" ):
        self.cd(dir)
        return [key.GetName() for key in gDirectory.GetListOfKeys()]

TFile.GetKeyNames = GetKeyNames

def ensure_dir(f):
    d = os.getcwd()+"/"+f
    #print d
    if not os.path.exists(d):
        os.mkdir(f)

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

def replaceAll(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
            sys.stdout.write(line)


