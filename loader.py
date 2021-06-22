import h5py
import numpy as np
import mne
from wavelet_transform import *

# import xarray as xr
# from utilities import flatten_dict

def load(directory, file, tfr="Comp256Hz", csvdirectory=None, csvfile=None):
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
    
    if tfr=="Comp256Hz":
        print("Computing and loading the time-frequency wavelet transformation of all subjects for all IC, 22 trials...")
        for subj in range(1, n_subj+1):
            for IC in range(1, n_IC+1):
                for trial in range(1, 22):
                    try:
                        data[f'tfr_256Hz subject{subj}, IC{IC}, trial{trial}'] = wavelet_transform(data, info, subj, IC, trial)
                    except:
                        pass
            print(f"Loaded subject {subj}")
        
    if tfr=="mat20Hz":
        print("Loading the time-frequency wavelet transformation of the 2nd subject from the .mat file")
        subj=2-1
        for IC in range(n_IC):
            try:
                data[f'raw_timecourse_256Hz subject{subj+1}, IC{IC+1}'] = _load_ALL_FREQ_power_20Hz(mat_file, cells_refs, IC, subj)
            except:
                print(f'The independent component IC{IC+1} of the subject {subj+1} is not in the .mat file.')
        print("Loaded")
        
    if tfr=="csv256Hz":
        csvpath = f"{csvdirectory}/{csvfile}"
        
        csvfileread = open(csvpath, 'r', newline='')
        spamreader = csv.reader(csvfileread, delimiter=';', quotechar='|')
        
        print("Loading the time-frequency wavelet transformation from the .csv file")        
#         for row in spamreader:
        for n in range(97*200):
            row = spamreader.__next__()
            index = row[0]
            vect = np.zeros(len(row)-1)
            for t in range(len(row)-1):
                vect[t] = sp[t+1]
            data[index] = vect
        print("Loaded")
            
    return data, n_IC, n_subj, n_trials

def load_oneIC(mat_file, cells_refs, subj=2, IC=1):

    data = {}
    
    try:
        print("Loading the raw timecourse")
        data[f'raw_timecourse_256Hz'] = _load_raw_timecourse_256Hz(mat_file, cells_refs, IC-1, subj-1)
        
        n_trials = data[f'raw_timecourse_256Hz'].shape[0]
    
        data['freq_axis'] = _load_freq(mat_file, cells_refs, IC-1, subj-1)
        data['time_axis'] = _load_time_256Hz(mat_file, cells_refs, IC-1, subj-1)

        info = mne.create_info(ch_names=['signal'], sfreq=256, ch_types=['eeg'])

        print(f"Computing and loading the time-frequency wavelet transformation for 3 trials")
        for trial in range(1, 4):
            data[f'tfr_256Hz trial{trial}'] = wavelet_transform2(data, info, trial)

    except:
        print(f'The independent component IC{IC} of the subject {subj} is not in the .mat file.')
        raise

    return data, n_trials
    

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

def _load_ALL_FREQ_power_20Hz(mat_file, cells_refs, IC, subj):
    cell = mat_file[cells_refs[IC, subj]]
    all_freq_power_20Hz = cell['ALL_FREQ_power_20Hz'][:]
#     all_freq_power_20Hz = np.transpose(all_freq_power_20Hz)
    return all_freq_power_20Hz
            


