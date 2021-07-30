import numpy as np
import mne

def wavelet_transform (data, info=None, trial=1):
    # The trial argument should be an integer or a numpy array (with values in [1, n_trials]), 
    # in which case the function will plot the tfr of the mean-timecourse of selected trials 
    if info==None:
        info = mne.create_info(ch_names=['signal'], sfreq=256, ch_types=['eeg'])
    if type(trial).__name__=='int':
        raw = mne.EpochsArray(data[f'raw_timecourse_256Hz'][trial-1,np.newaxis,np.newaxis,:], info, verbose=False) 
    else:
        raw = mne.EpochsArray(data[f'raw_timecourse_256Hz'][(trial-1).astype(int), np.newaxis, :], info, verbose=False) 
    tfr = mne.time_frequency.tfr_morlet(raw, freqs=data['freq_axis'], n_cycles=data['freq_axis']/2, picks='eeg', return_itc=False) 

    return tfr._data