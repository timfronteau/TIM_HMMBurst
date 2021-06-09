import h5py
import numpy as np
import mne

# import xarray as xr
# from utilities import flatten_dict

def load(directory, file):
    path = f"{directory}/{file}"
    
    mat_file = h5py.File(path, "r")
    cells_refs = mat_file['FCK_LOCKED_IC_JYOTIKA']
    n_IC, n_subj = cells_refs.shape
    
    data = {}
    
    for IC in range(n_IC):
        for subj in range(n_subj):
#             try:
            data[f'raw_timecourse_256Hz subject{subj+1}, IC{IC+1}'] = _load_raw_timecourse_256Hz(IC, subj)
#             except:
#                 print(f'The independent component IC{IC+1} of the subject {subj+1} is not in the .mat file.')

    n_trials = data['raw_timecourse_256Hz subject1, IC1'].shape[0]
    
    data['freq_axis'] = _load_freq(0, 0)
    data['time_axis'] = _load_time_256Hz(0, 0)
    
    info = mne.create_info(ch_names=['signal'], sfreq=256, ch_types=['eeg'])
    
    load_all_tfr_one_trial()
    load_all_tfr_one_subject()
    
    return data, n_IC, n_subj, n_trials
    

def _load_raw_timecourse_256Hz(IC, subj):
    cell = mat_file[cells_refs[IC, subj]]
    raw_timecourse_256Hz = cell['raw_timecourse_256Hz'][:]
    raw_timecourse_256Hz = np.transpose(raw_timecourse_256Hz)
    return raw_timecourse_256Hz

def _load_time_256Hz(IC,subj):
    cell = mat_file[cells_refs[IC, subj]]
    time_256Hz = cell['time_256Hz'][:]
    time_256Hz = np.transpose(time_256Hz)[0]
    return time_256Hz

def _load_freq(IC,subj):
    cell = mat_file[cells_refs[IC, subj]]
    freq = cell['freq'][:]
    freq = np.transpose(freq)[0]
    return freq

def load_all_tfr_one_trial (trial=1):
    for IC in range(1, n_IC+1):
        for subj in range(1, n_subj+1):
            try:
                data[f'tfr_256Hz subject{subj}, IC{IC}, trial{trial}'] = wavelet_transform(subj, IC, trial)
            except:
                pass
    return None

def load_all_tfr_one_subject (subj=1):
    for IC in range(1, n_IC+1):
        for trial in range(1, n_trials+1):
            try:
                data[f'tfr_256Hz subject{subj}, IC{IC}, trial{trial}'] = wavelet_transform(subj, IC, trial)
            except:
                pass
    return None
            
def wavelet_transform (subj=1, IC=1, trial=1):
    raw = mne.EpochsArray(data[f'raw_timecourse_256Hz subject{subj}, IC{IC}'][trial-1,np.newaxis,np.newaxis,:], info, verbose=False) 
    tfr = mne.time_frequency.tfr_morlet(raw, freqs=data['freq_axis'], n_cycles=data['freq_axis']/2, picks='eeg', return_itc=False)
    
#     For a wavelet transform on several trials/all the trials:
#
#     raw = mne.EpochsArray(raw_timecourse_subj0_IC0[100:105, np.newaxis, :], info, verbose=False) 
#     raw = mne.EpochsArray(raw_timecourse_subj0_IC0[:, np.newaxis, :], info, verbose=False) 

    return tfr._data



