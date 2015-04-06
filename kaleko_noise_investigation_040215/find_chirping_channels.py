

#Modify this to point towards your data files
data_basedir = '/Users/davidkaleko/Data/UBCommish/noise_files/'



import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from root_numpy import root2array, root2rec, tree2rec, array2root
from ROOT import TH1F, TFile
import nputils as nputils
import sys

if len(sys.argv) != 4:
    print "Usage: python find_chirping_channels.py runno subrun subrun"
    quit()

run = int(sys.argv[1])
subrun1 = int(sys.argv[2])
subrun2 = int(sys.argv[3])

fname = data_basedir + 'noise_run%03d_subrun%03d_%03d.root'%(run,subrun1,subrun2)
f = TFile(fname,"READ")

ch_mapping = 'mapping_for_jeremy.txt'
mapping_df = pd.DataFrame(np.loadtxt(ch_mapping, delimiter='\t',dtype='int'))
mapping_df.columns = ['larsoft_chno','crate','slot','femch']

def does_wf_chirp(wf):
 
    RMS_chirp_min = 40
    RMS_quiet_max = 10
    RMS_windowsize = 20
    RMS_array = []
    
    did_chirp = False
    
    #sliding window of size RMS_windowsize over waveform, computing RMS in window each time
    for tick in np.arange(0,len(wf),int(RMS_windowsize/2)):
        if tick + RMS_windowsize >= len(wf):
            break
        window_rms = wf[tick:(tick+RMS_windowsize)].std()
        RMS_array.append(window_rms)
        
        if len(RMS_array) < 2: continue
        #it chirped it if went from high RMS to low RMS
        did_chirp = True if RMS_array[-1] > RMS_chirp_min and RMS_array[-2] < RMS_quiet_max else False
        #it also chirped if it went from low RMS to high RMS
        did_chirp = True if RMS_array[-1] < RMS_quiet_max and RMS_array[-2] > RMS_chirp_min else False
    
        if did_chirp: break
    
    return did_chirp

#Get a list of channels that have even slightly bad RMS to check for chirping behavior
high_rms_channels = []
wf_df = pd.DataFrame(root2array(fname,'tree'))
grp = wf_df.groupby(['crate', 'slot', 'femch'])

for key, grp_df in grp:
    sr = grp_df['rms']
    rms = sr.std()
    if rms > 5:
        high_rms_channels.append(key)

#import both "BAD" and "GOOD" waveforms of each and check for chirping
chirping_channels = []
for c,s,ch in high_rms_channels:
    larsoft_num = int(mapping_df.query('crate == %d and slot == %d and femch == %d'%(c,s,ch))['larsoft_chno'])        
    bad_wf = nputils.TH1_to_nparray(f.Get('hWF_BAD_%0.4d'%larsoft_num))
    bad_wf = bad_wf[1:]
    good_wf = nputils.TH1_to_nparray(f.Get('hWF_GOOD_%0.4d'%larsoft_num))
    good_wf = good_wf[1:]

    if does_wf_chirp(bad_wf):
        chirping_channels.append((c,s,ch))
        continue
    if does_wf_chirp(good_wf):
        chirping_channels.append((c,s,ch))
        continue


print "# of high RMS channels found is %d."%len(high_rms_channels)
print "# of those channels found to chirp is %d."%len(chirping_channels)


#Save the list of (larsoft) channel numbers to a text file, to draw with VireViewer
outfname = 'chirping_channel_list_run%03d_subrun%03d_%03d.txt'%(run,subrun1,subrun2)
outfile = open(outfname,'w')
for cc in chirping_channels:
    outfile.write('%d %d %d\n'%(cc[0],cc[1],cc[2]))
outfile.close()


print "Saved list of chirping channels to %s." % outfname
