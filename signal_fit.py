import ROOT
import matplotlib.pyplot as plt
from scipy.optimize import leastsq
import numpy as np
'''
Code to fit waveform
1.Header of fitting class for SiPM signal anaysis
2.Main to draw some fit results
'''
inputFile=ROOT.TFile("/junofs/users/guanyuduo/fbk20_10_31/5751/PreProcess/output_waveform/rootfile/2021_11_5_140051_32_-50.root")
histBaseline=ROOT.gROOT.FindObject("average baseline")
histSignal=ROOT.gROOT.FindObject("1.pe model")
#A=ROOT.gROOT.FindObject("average signal c")
#A=ROOT.gROOT.FindObject("average signal 2pe")
histWaveform=ROOT.gROOT.FindObject("signal 2pe")

def Load(filename):
    inputFile=ROOT.TFile(filename)
    histBaseline=ROOT.gROOT.FindObject("average baseline")
    histSignal=ROOT.gROOT.FindObject("1.pe model")
    histWaveform=ROOT.gROOT.FindObject("signal 2pe")

def FUNCN(p,x):
    A0,A1,S0,T0 = p
    x=np.array(x)
    y=[]
    for i in range(len(x)):
        if x[i] > 500+T0 and x[i]<1500+T0:
            y.append(A0*B.GetBinContent(int(x[i]+1))+A1-S0*S.GetBinContent(int(x[i]+1-500-T0)))
        else:
            y.append(A0*B.GetBinContent(int(x[i]+1))+A1)
        #y.append(A0*B.GetBinContent(int(x[i]+1))+A1)
    return np.array(y)

def error(p,x,y):
    return np.array(FUNCN(p,x))-np.array(y)

if __name__=='__main__':
    x1=[]
    y1=[]
    p0 = [1.2,0,1.6,100]
    for i in range(2002):
        x1.append(i)
        y1.append(A.GetBinContent(i+1))

    plt.plot(x1,y1,'.-')
    Para=leastsq(error,p0,args=(x1,y1))

    A0,A1,S0,T0=Para[0]
    print("A0=",A0,"A1=",A1,"S0=",S0,"T0=",T0)
    print("cost : "+str(Para[1]))

    x1 = np.array(x1)
    plt.plot(x1,y1,'.-')
    y2 = FUNCN([A0,A1,S0,T0],x1)
    print("A0=",A0,"A1=",A1,"S0=",S0,"T0=",T0)
    print("cost : "+str(Para[1]))
    plt.plot(x1,y2,'r-')
    plt.show()

