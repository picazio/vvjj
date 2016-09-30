//
// author Hongtao Yang hongtao.yang@cern.ch
//        Yanyan Gao yanyan.gao (for the workspace)
// run by root -l -b calcPvalue.C 

using namespace std;
using namespace RooFit;
using namespace RooStats;
#include <iostream>

double minimize(ModelConfig *mc, RooAbsData *data, int strat){
  RooAbsReal* nll=mc->GetPdf()->createNLL(*data, Constrain(*mc->GetNuisanceParameters()), GlobalObservables(*mc->GetGlobalObservables()));
  nll->enableOffsetting(true);
  RooMinimizer minim(*nll);
  minim.setStrategy(strat);
  minim.setPrintLevel(0);
  minim.setEps(1);
  int status=minim.minimize("Minuit2");
  return nll->getVal();
}

void constSet(RooArgSet* set, bool flag, RooArgSet* snapshot=NULL){
  TIterator *iter = set -> createIterator();
  RooRealVar* parg = NULL;
//   if(snapshot!=NULL) recoverSet(set,snapshot);
  if(snapshot!=NULL) *set=*snapshot;
  while((parg=(RooRealVar*)iter->Next()) ){
    parg->setConstant(flag); 
  }
  // SafeDelete(iter);
}

void calcPvalue(TString inputPreDir = "",
    TString input = "", TString lumitag = "", TString model = "", TString sel = "", bool hasNtrk = false ) 
{
  TString modelName = model;
  if ( model == "Gravi" ) modelName = "GRAVI";

  TString hasNtrkString = "wNtrk";
  if ( ! hasNtrk ) hasNtrkString = "noNtrk"; 


  TString inputWSFileName= Form("%s/results_%s_%sfb//VVJJ_%s_%s/ws/VVJJ_%s_%s_actualWorkspaces_%s_%s_%s_obs_%s.root",
				inputPreDir.Data(), input.Data(), lumitag.Data(),  modelName.Data(), sel.Data(),  modelName.Data(), sel.Data(), input.Data(), sel.Data(), model.Data(), hasNtrkString.Data()  );
  std::cout<<inputWSFileName<<std::endl;
  //TString inputWSFileName= Form("%s/results_%s//VVJJ_%s_%s/ws/VVJJ_%s_%s_actualWorkspaces_%s_%s_%s_obs_%s.root",
  //inputPreDir.Data(), input.Data(),  modelName.Data(), sel.Data(),  modelName.Data(), sel.Data(), input.Data(), sel.Data(), model.Data(), hasNtrkString.Data()  );
  
  TFile *f=TFile::Open(inputWSFileName);
  FILE *output_p0 = fopen(Form("output_p0_%s_%s_%s.txt", input.Data(), model.Data(), sel.Data() ), "w");;

  std::vector<int> masses;
  masses.push_back(1200);
  masses.push_back(1300);
  masses.push_back(1400);
  masses.push_back(1500);
  masses.push_back(1600);
  masses.push_back(1700);
  masses.push_back(1800);
  masses.push_back(1900);
  masses.push_back(2000);
  masses.push_back(2200);
  masses.push_back(2400);
  masses.push_back(2600);
  masses.push_back(2800);
  masses.push_back(3000);

  for ( unsigned int i = 0; i < masses.size(); i++ ) {

    int mass = masses.at(i);
    cout << "*****Doing mass " << mass << "*********" << endl;
    // ------------- Change workspace, ModelConfig, and dataset names to the one you use -----------------
    RooWorkspace *w=(RooWorkspace*)f->Get(Form("ws_%ip000", mass));
    ModelConfig *mc=(ModelConfig*)w->obj("ModelConfig");
    RooAbsData *data=w->data("obsData");
    int strat=11;

    RooMsgService::instance().setGlobalKillBelow(RooFit::FATAL);

    w->var("mu")->setRange(-100,100);
    w->var("mu")->setConstant(false);
    double nllMuHat=minimize(mc, data, strat);
    double muhat=w->var("mu")->getVal();

    w->var("mu")->setVal(0);
    w->var("mu")->setConstant(true);

    double nllMuFix=minimize(mc, data, strat);

    double dnll=2*(nllMuFix-nllMuHat);
    int sign=muhat>0?1:-1;
    double pvalue =  1-ROOT::Math::normal_cdf(sign*sqrt(dnll),1,0);
    double significance = RooStats::PValueToSignificance(pvalue);
    cout<< " mass " << mass << " pvalue " << pvalue << " significance = " << significance << endl; 
    // fprintf ( output_p0, "%i %.5f %.5f\n", mass, muhat, pvalue); 
    fprintf ( output_p0, "%i %.5f %.1f\n", mass, pvalue, significance); 

  }
}

