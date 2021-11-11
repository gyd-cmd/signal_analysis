''' This python script is a basis processing for FADC TXT data ,input file is a txt file saved the waveform data ,through this script a root file with waveform information is created '''
import os
import numpy as np
import sys
import scipy.signal as sgn
import ROOT
import scipy.fftpack as fpk
from array import array
import argparse

parser = argparse.ArgumentParser()
parser.description = "Please enter input path  and output path"
parser.add_argument("-i","--inputPath",help="this is pareameter for input")
parser.add_argument("-o","--outputPath",help="this is pareameter for output")
parser.add_argument("-T","--T",help="this is pareameter for tempeature")
parser.add_argument("-V","--V",help="SiPM Voltage")
args = parser.parse_args()
print("inputpath : "+args.inputPath)
print("outputpath : "+args.outputPath)
print("voltage : "+args.V)
print("Temperature : "+args.T)
print("Argument loading...")

fileName = args.inputPath
ROOT_FILE = ROOT.TFile.Open(args.outputPath,"recreate")

#Set and Save argument
ROOT_TREE = ROOT.TTree("evt","evt")
V = array("f",[0])
T = array("f",[0])
bkgQ = array("f",[0])
sigQ = array("f",[0])
ROOT_TREE.Branch("V",V,"V/F")
ROOT_TREE.Branch("T",T,"T/F")
ROOT_TREE.Branch("bkgQ",bkgQ,"bkgQ/F")
ROOT_TREE.Branch("sigQ",sigQ,"sigQ/F")
threshold = 5
thredhold2 = 7
threshold3 =10
#Set and process signal information
TIME_WINDOW = int(2002)
'''
'''
V[0] = float(args.V)
T[0] = float(args.T)
baseline_waveform = ROOT.TH2F("wo signal","all signal",2002,0,2002,400,600,1000)
signal_waveform_1 = ROOT.TH2F("wi 1.pe signal","1.pe signal",2002,0,2002,400,600,1000)
signal_waveform_1c = ROOT.TH2F("wi 1.pe signal c","1.pe signal c",2002,0,2002,400,600,1000)
signal_waveform_2 = ROOT.TH2F("wi 2.pesignal","2.pe signal",2002,0,2002,400,600,1000)
signal_waveform_3 = ROOT.TH2F("wi 3.pe signal","3.pe signal",2002,0,2002,400,600,1000)
signal_waveform_average= ROOT.TH1F("average signal","average 1.pe signal",2002,0,2002)
signal_waveform_average_c= ROOT.TH1F("average signal c","average 1.pe signal c",2002,0,2002)
signal_waveform_average_2pe= ROOT.TH1F("average signal 2pe","average 2.pe signal",2002,0,2002)
signal_waveform_2pe= ROOT.TH1F("signal 2pe"," signal 2pe",2002,0,2002)
baseline_waveform_average= ROOT.TH1F("average baseline","baseline",2002,0,2002)
signal_waveform_model= ROOT.TH1F("1.pe model","model",1000,0,1000)

with open(fileName,'r',encoding='gbk') as file_to_read:
    j = 0
    m = 0
    m2 =0
    m3 =0
    b,a = sgn.butter(8,0.1,"lowpass")
    for lines in file_to_read:
        waveform = (lines.split())
        waveform = list(map(float,waveform))
        waveform = np.array(waveform[0:2002])
        baseline = np.mean(waveform[0:900])
        if abs(baseline-880)<1:
            amp_max  = np.min(waveform[1050:1150])
            if baseline-amp_max>4 and baseline-amp_max<7:
                if m <=5000:
                    m = m+1
                    for k in range(TIME_WINDOW):
                        signal_waveform_1.Fill(k+1,waveform[k])
                        w_tmp = signal_waveform_average.GetBinContent(k+1)
                        signal_waveform_average.SetBinContent(k+1,w_tmp+waveform[k])
                if m > 5000:
                    m2 = m2+1
                    for k in range(TIME_WINDOW):
                        signal_waveform_1c.Fill(k+1,waveform[k])
                        w_tmp = signal_waveform_average_c.GetBinContent(k+1)
            if baseline-amp_max>7 and baseline-amp_max<10 :
                m3 = m3+1
                for k in range(TIME_WINDOW):
                    signal_waveform_2.Fill(k+1,waveform[k])
                    w_tmp = signal_waveform_average_2pe.GetBinContent(k+1)
                    signal_waveform_average_2pe.SetBinContent(k+1,w_tmp+waveform[k])
                    signal_waveform_2pe.SetBinContent(k+1,waveform[k])
            if baseline-amp_max<3:
                j = j+1
                bkgQ[0] = sum(baseline-waveform[900:1400])
                sigQ[0] = 0
                ROOT_TREE.Fill()
                for k in range(TIME_WINDOW):
                    baseline_waveform.Fill(k+1,waveform[k])
                    w_tmp = baseline_waveform_average.GetBinContent(k+1)
                    baseline_waveform_average.SetBinContent(k+1,w_tmp+waveform[k])
        else:
            pass
        if m2 >5000 and j>5000 and m3>1000:
            break;
    for k in range(TIME_WINDOW):
        w_tmp = signal_waveform_average.GetBinContent(k+1)/m
        signal_waveform_average.SetBinContent(k+1,w_tmp)
        w_tmp = baseline_waveform_average.GetBinContent(k+1)/j
        baseline_waveform_average.SetBinContent(k+1,w_tmp)
        w_tmp = signal_waveform_average_c.GetBinContent(k+1)/m2
        signal_waveform_average_c.SetBinContent(k+1,w_tmp)
        w_tmp = signal_waveform_average_2pe.GetBinContent(k+1)/m3
        signal_waveform_average_2pe.SetBinContent(k+1,w_tmp)

with open(fileName,'r',encoding='gbk') as file_to_read:
    m4 = 0
    for lines in file_to_read:
        waveform = (lines.split())
        waveform = list(map(float,waveform))
        waveform = np.array(waveform[0:2002])
        baseline = np.mean(waveform[0:900])
        if abs(baseline-880)<1:
            amp_max  = 9999
            amp_max_bin = 1050
            for  i in range(100):
                if amp_max > waveform[1050+i]:
                    amp_max = waveform[1050+i]
                    amp_max_bin = 1050+i
            if baseline-amp_max>4 and baseline-amp_max<7 and m4<5000:
                    m4 =m4+1
                    for k in range(1000):
                        w_tmp = signal_waveform_model.GetBinContent(k+1)-waveform[amp_max_bin-500+k]+baseline_waveform_average.GetBinContent(amp_max_bin-500+k)
                        signal_waveform_model.SetBinContent(k+1,w_tmp)
    for k in range(1000):
        w_tmp = signal_waveform_model.GetBinContent(k+1)/m4
        signal_waveform_model.SetBinContent(k+1,w_tmp)
ROOT_TREE.Write()
ROOT_FILE.Write()
ROOT_FILE.Close()
