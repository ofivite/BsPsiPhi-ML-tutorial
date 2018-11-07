import ROOT
from ROOT import RooFit as RF


var_discr = ROOT.RooRealVar('BU_mass_Cjp', 'm(J/#psi#pi^{+}#pi^{#font[122]{\55}}K^{+}K^{#font[122]{\55}}) [GeV]',
                            sig_window['BU_mass_Cjp'][0], sig_window['BU_mass_Cjp'][1])
var_control = ROOT.RooRealVar('psi_mass_Cjp', 'm(J/#psi#pi^{+}#pi^{#font[122]{\55}}) [GeV]',
                            sig_window['psi_mass_Cjp'][0], sig_window['psi_mass_Cjp'][1])
PHI_mass_Cjp = ROOT.RooRealVar('PHI_mass_Cjp', 'm(K^{+}K^{#font[122]{\55}}) [GeV]',
                         sig_window['PHI_mass_Cjp'][0], sig_window['PHI_mass_Cjp'][1])

mean_Bs = ROOT.RooRealVar("mean_Bs", "", 5.37, 5.25, 5.45)
sigma_Bs_1 = ROOT.RooRealVar("sigma_Bs_1", "", 0.013, 0.001, 0.05)
sigma_Bs_2 = ROOT.RooRealVar("sigma_Bs_2", "", 0.006, 0.001, 0.05)

a1 = ROOT.RooRealVar('a1', 'a1', 0.01, 0., 1.)
a2 = ROOT.RooRealVar('a2', 'a2', 0.01, 0., 1.)
a3 = ROOT.RooRealVar('a3', 'a3', 0.01, 0., 1.)
a4 = ROOT.RooRealVar('a4', 'a4', 0.01, 0., 1.)

N_sig_Bs = ROOT.RooRealVar('N_sig_Bs', '', 300., 0., 4000)
N_bkgr_Bs = ROOT.RooRealVar('N_bkgr_Bs', '', 3000., 0., 40000)
fr_Bs = ROOT.RooRealVar('fr_Bs', 'fr_Bs', 0.46, 0., 1.)

sig_Bs_1 = ROOT.RooGaussian("sig_Bs_1", "", var_discr, mean_Bs, sigma_Bs_1)
sig_Bs_2 = ROOT.RooGaussian("sig_Bs_2", "", var_discr, mean_Bs, sigma_Bs_2)

signal_Bs = ROOT.RooAddPdf("signal_Bs", "signal_Bs", ROOT.RooArgList(sig_Bs_1, sig_Bs_2), ROOT.RooArgList(fr_Bs))
# signal_Bs = sig_Bs_1
bkgr_Bs = ROOT.RooBernstein('bkgr_Bs', '', var_discr, ROOT.RooArgList(a1, a2, a3))

model_1D_Bs = ROOT.RooAddPdf('model_1D_Bs', 'model_1D_Bs', ROOT.RooArgList(signal_Bs, bkgr_Bs), ROOT.RooArgList(N_sig_Bs, N_bkgr_Bs))



f = ROOT.TFile(fname, 'R')
roodata = ROOT.RooDataHist('data', '', ROOT.RooArgSet(var_discr), f.Get('predicted_mass'))


# mean_Bs.setConstant(1); sigma_Bs_1.setConstant(1); sigma_Bs_2.setConstant(1); fr_Bs.setConstant(1)
rrr = model_1D_Bs.fitTo(roodata, RF.Extended(ROOT.kTRUE), RF.Save())
# rrr = model_1D_Bs.fitTo(data, RF.Extended(ROOT.kTRUE), RF.Save())
# rrr = model_1D_Bs.fitTo(data, RF.Extended(ROOT.kTRUE), RF.Save())
# model_1D_Bs.fitTo(data, RF.Extended(ROOT.kTRUE), RF.Save())

a1.setConstant(1); a2.setConstant(1); a3.setConstant(1);  a4.setConstant(1);
rrr = model_1D_Bs.fitTo(roodata, RF.Extended(ROOT.kTRUE), RF.Save())
rrr = model_1D_Bs.fitTo(roodata, RF.Extended(ROOT.kTRUE), RF.Save())
# a1.setConstant(0); a2.setConstant(0); a3.setConstant(0); a4.setConstant(0);
rrr.Print()


c = ROOT.TCanvas()
frame = ROOT.RooPlot('', '', var_discr, var_discr.getMin(), var_discr.getMax(), 40);
roodata.plotOn(frame)
model_1D_Bs.plotOn(frame)
model_1D_Bs.paramOn(frame, RF.Layout(0.7, 0.96, 0.9))

frame.Draw()
c.Draw()
