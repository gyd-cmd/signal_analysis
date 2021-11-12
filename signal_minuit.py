import ROOT
import matplotlib.pyplot as plt
import numpy as np
from iminuit import Minuit
'''
Code to fit waveform
1.Header of fitting class for SiPM signal anaysis
2.Main to draw some fit results
3.By iminuit
'''
inputFile=ROOT.TFile("/junofs/users/guanyuduo/fbk20_10_31/5751/PreProcess/output_waveform/rootfile/2021_11_5_140051_32_-50.root")
Baseline=ROOT.gROOT.FindObject("average baseline")
Signal=ROOT.gROOT.FindObject("1.pe model")
#A=ROOT.gROOT.FindObject("average signal c")
#A=ROOT.gROOT.FindObject("average signal 2pe")
Waveform=ROOT.gROOT.FindObject("signal 2pe")

amp_max_c = 0
amp_max_bin_c = 9999
for i in range(1000):
    if amp_max_c < Signal.GetBinContent(i+1):
        amp_max_c = Signal.GetBinContent(i+1)
        amp_max_bin_c = i+1

def Load(filename):
    inputFile=ROOT.TFile(filename)
    Baseline=ROOT.gROOT.FindObject("average baseline")
    Signal=ROOT.gROOT.FindObject("1.pe model")
    Waveform=ROOT.gROOT.FindObject("signal 2pe")
def func(i,p0,p1,p2):
    if i > p2 and i < 1000+p2:
        y = (Baseline.GetBinContent(int(i+1))+p0-p1*Signal.GetBinContent(int(i-p2+1)))
    else:
        y = (Baseline.GetBinContent(int(i+1))+p0)
    return y
def FitFunc(p0,p1,p2):
    chisq = 0
    delta = 0
    for i in range(2002):
        delta = Waveform.GetBinContent(i+1)-func(i,p0,p1,p2)
        chisq = chisq + delta*delta
    return chisq

if __name__=='__main__':
    par = [0,1,600]
    amp_max = 9999
    amp_max_bin = 9999

    for i in range(100):
        if amp_max > Waveform.GetBinContent(i+1050):
            amp_max = Waveform.GetBinContent(i+1050)
            amp_max_bin = i+1050

    par[2] = amp_max_bin-amp_max_bin_c
    m = Minuit(FitFunc,p0=par[0],p1=par[1],p2=par[2],name=("p0","p1","p2"))
    m.errordef = Minuit.LIKELIHOOD
    m.fixed["p2"] = True
    m.migrad()
    m.hesse()
    m.minos()
    par_fit = m.values
    print("Print rsults")
    print(m.params)

    #Draw waveform and fit curve
    t = []
    y = []
    y2 = []
    for i in range(2002):
        t.append(i)
        y.append(Waveform.GetBinContent(i+1))
        y2.append(func(i,par_fit[0],par_fit[1],par_fit[2]))
    plt.plot(t,y,'.-')
    plt.plot(t,y2,'r.-')
    plt.show()

