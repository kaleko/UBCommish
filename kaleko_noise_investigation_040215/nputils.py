import os, sys
from ROOT import *
import numpy as np
from scipy.fftpack import fft

def TH1_to_nparray(hist,maxbins=99999999):

#    if type(hist) is not TH1F or TH1D:
#        print type(hist)
#        raise AttributeError("Input histogram to TH1_to_nparray is not type ROOT.TH1F or ROOT.TH1D.")

    n = (hist.GetNbinsX() if hist.GetNbinsX()<maxbins else maxbins)        

    my_array = np.zeros(n)
    for x in xrange(n):
        my_array[x] = hist.GetBinContent(x)
    
    return my_array

def nparray_to_TH1F(hist,nparray,nparray_spacing=1.):
    
    array_size = nparray.size
    for i in xrange(array_size):
        x = i*nparray_spacing
        hist.Fill(x,nparray[i])


def FFT_on_nparray(nparray):

    if type(nparray) is not np.ndarray:
        raise AttributeError("Input histogram to FFT_on_nparray is not type numpy.ndarray.")

    #First remove pedestal
    nparray = np.subtract(nparray,compute_pedestal(nparray))

    #Number of data points in waveform
    N = nparray.size
    #Spacing between points in waveform (500 ns for TPC waveform)
    T = 1.0/2000000.

    x = np.linspace(0.0,N*T,N)
    y = nparray

    yf = fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)

    return xf, yf

def compute_pedestal(nparray, nsamples=20):

    pedestal = 0.
    for x in xrange(nsamples):
        pedestal = pedestal + nparray[x]
    pedestal = pedestal / nsamples

    return pedestal
