from ROOT import *
import numpy as np
import sys
import nputils as npu
import matplotlib.pyplot as plt
gStyle.SetOptStat(0)

### arguments are :
# run number, (larsoft) channel number

filename = '/Users/davidkaleko/Data/UBCommish/noise_run095_subrun000_019.root'
name = 'hWF_GOOD_7038'

f = TFile(filename,"READ")

c = TCanvas()

h = f.Get(name)
wf = npu.TH1_to_nparray(h)
myx, myy = npu.FFT_on_nparray(wf)
rebinned = TH1F("rebinnedfft_ch4191","FFT Rebinned of 7038 run 95;Frequency [Hz];FFT Value [Arb]",50,0,100000)
dummy = npu.nparray_to_TH1F(rebinned,np.abs(myy[1:wf.size/2]),nparray_spacing=(myx[-1]-myx[1])/myx.size)
#rebinned.GetYaxis().SetRangeUser(0,180000)
rebinned.Draw()
c.Update()
c.Modified()

sys.stdin.readline()
