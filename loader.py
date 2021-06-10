import h5py
import numpy as np
import mne
from wavelet_transform import wavelet_transform

# import xarray as xr
# from utilities import flatten_dict

def load(directory, file):
    path = f"{directory}/{file}"
    
    mat_file = h5py.File(path, "r")
    cells_refs = mat_file['FCK_LOCKED_IC_JYOTIKA']
    n_IC, n_subj = cells_refs.shape
    
    data = {}
    
    print("loading the raw timecourses...")
    for IC in range(n_IC):
        for subj in range(n_subj):
            try:
                data[f'raw_timecourse_256Hz subject{subj+1}, IC{IC+1}'] = _load_raw_timecourse_256Hz(mat_file, cells_refs, IC, subj)
            except:
                print(f'The independent component IC{IC+1} of the subject {subj+1} is not in the .mat file.')

    n_trials = data['raw_timecourse_256Hz subject2, IC1'].shape[0]
    
    data['freq_axis'] = _load_freq(mat_file, cells_refs, 0, 0)
    data['time_axis'] = _load_time_256Hz(mat_file, cells_refs, 0, 0)
    
    info = mne.create_info(ch_names=['signal'], sfreq=256, ch_types=['eeg'])

    print("Computing and loading the time-frequency wavelet transformation of the 1st trial for all subjects, all IC...")
    for IC in range(1, n_IC+1):
        for subj in range(1, n_subj+1):
            try:
                data[f'tfr_256Hz subject{subj}, IC{IC}, trial1'] = wavelet_transform(data, info, subj, IC, 1)
            except:
                pass
    
    print("Computing and loading the time-frequency wavelet transformation of the 2nd subject for all IC, all trials...")
    for IC in range(1, n_IC+1):
        for trial in range(1, n_trials+1):
            try:
                data[f'tfr_256Hz subject2, IC{IC}, trial{trial}'] = wavelet_transform(data, info, 2, IC, trial)
            except:
                pass
    print("Loaded")
        
    return data, n_IC, n_subj, n_trials
    

def _load_raw_timecourse_256Hz(mat_file, cells_refs, IC, subj):
    cell = mat_file[cells_refs[IC, subj]]
    raw_timecourse_256Hz = cell['raw_timecourse_256Hz'][:]
    raw_timecourse_256Hz = np.transpose(raw_timecourse_256Hz)
    return raw_timecourse_256Hz

def _load_time_256Hz(mat_file, cells_refs, IC, subj):
    cell = mat_file[cells_refs[IC, subj]]
    time_256Hz = cell['time_256Hz'][:]
    time_256Hz = np.transpose(time_256Hz)[0]
    return time_256Hz

def _load_freq(mat_file, cells_refs, IC, subj):
    cell = mat_file[cells_refs[IC, subj]]
    freq = cell['freq'][:]
    freq = np.transpose(freq)[0]
    return freq
            


