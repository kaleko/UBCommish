import numpy as np

def find_chirp_regions(wf,RMS_chirp_cutoff=15,RMS_windowsize=20):
 
    RMS_array = []
    
    #chirp_regions is [ (start_t,stop_t), (start,stop), etc]
    chirp_regions = []

    chirp_start, chirp_end = 0,0
    last_tick = False
    
    #sliding window of size RMS_windowsize over waveform, computing RMS in window each time
    for tick in np.arange(0,len(wf),int(RMS_windowsize)):
        if tick + RMS_windowsize >= len(wf):
            break
        if len(wf) - (tick + RMS_windowsize) == 1:
            last_tick = True
            
        window_rms = wf[tick:(tick+RMS_windowsize)].std()
        RMS_array.append(window_rms)

        if window_rms > RMS_chirp_cutoff and tick == 0:
            chirp_start = 1
            
        if len(RMS_array) < 2: continue
 
        #chirps start if it goes from low RMS to high RMS
        if RMS_array[-1] > RMS_chirp_cutoff and RMS_array[-2] < RMS_chirp_cutoff:
            chirp_start = tick 

        #chirps end if it goes from high RMS to low RMS
        if RMS_array[-1] < RMS_chirp_cutoff and RMS_array[-2] > RMS_chirp_cutoff:
            chirp_end = tick 
         
        #assume chirp ends on last tick if in high RMS region
        if last_tick and RMS_array[-1] > RMS_chirp_cutoff:
            chirp_end = tick
            
        if chirp_start != 0 and chirp_end != 0 and chirp_end - chirp_start > RMS_windowsize:
            chirp_regions.append((chirp_start,chirp_end))
            chirp_start, chirp_end = 0, 0

    return chirp_regions
