import numpy as np
import matplotlib.pyplot as plt

def plot_all_timecourses (data, n_IC, n_subj, trial=1, save=False):
    plt.figure(figsize=(16, 30))
    for IC in range(1, n_IC+1):
        for subj in range(1, n_subj+1):
            try:
                plt.subplot(n_subj, n_IC, IC+(subj-1)*n_IC)
                amax = np.amax(data[f'raw_timecourse_256Hz subject{subj}, IC{IC}'][trial-1,:])
                if amax>=1:
                    plt.plot(data['time_axis'], data[f'raw_timecourse_256Hz subject{subj}, IC{IC}'][trial-1,:], color='green', linewidth=.3)
                elif amax>=0.0004:
                    plt.plot(data['time_axis'], data[f'raw_timecourse_256Hz subject{subj}, IC{IC}'][trial-1,:], color='blue', linewidth=.3)
                else:
                    plt.plot(data['time_axis'], data[f'raw_timecourse_256Hz subject{subj}, IC{IC}'][trial-1,:], color='red', linewidth=.3)
            except:
                pass
    if save==True:
        plt.savefig('all-timecourses.png', dpi=600)
        
def plot_timecourse (data, IC, subj, trial, save=False):
    plt.figure(figsize=(16, 3))
    plt.plot(data['time_axis'], data[f'raw_timecourse_256Hz subject{subj}, IC{IC}'][trial-1,:], linewidth=.3)
    if save==True:
        plt.savefig(f'timecourse-subj{subj}_IC{IC}_trial{trial}.png', dpi=600)
        
def save_all_tfr_one_trial (data, n_subj, n_IC, trial=1, vmin=None, vmax=None, save=False):
    fig = plt.figure(figsize=(13, 20), clear=True)
    for subj in range(1, n_subj+1):
        fig.clf()
        for IC in range(1, n_IC+1):
            try:
                plt.subplot(4, 1, IC)
                plt.title(f'Wavelet transform IC{IC}')
                plt.imshow(data[f'tfr_256Hz subject{subj}, IC{IC}, trial{trial}'][0], 
                           aspect='auto', origin='lower', extent=[-4, 3, 2, 50], vmin=vmin, vmax=vmax, cmap='RdBu_r')
                plt.xlabel('Time (s)')
                plt.ylabel('Frequencies (Hz)')
                plt.colorbar()
            except:
                pass
        if save==True:
            plt.savefig(f'tfr/tfr-subj{subj}_trial{trial}.png', dpi=600)
            
def plot_all_tfr_one_trial (data, n_subj, n_IC, trial=1, vmin=None, vmax=None, save=False):
    plt.figure(figsize=(16, 30))
    plt.title('Wavelet transform')
    for IC in range(1, n_IC+1):
        for subj in range(1, n_subj+1):
            try:
                plt.subplot(n_subj, n_IC, IC+(subj-1)*n_IC)
                plt.imshow(data[f'tfr_256Hz subject{subj}, IC{IC}, trial{trial}'][0], 
                           aspect='auto', origin='lower', extent=[-4, 3, 2, 50], vmin=vmin, vmax=vmax, cmap='RdBu_r')
                plt.tight_layout()
                plt.colorbar()
            except:
                pass
    if save==True:
        plt.savefig(f'all-tfr_trial{trial}.png', dpi=600)
        
def plot_hmm_over_tfr(   
    data, gamma, lags, n_states, max_power, # the data we need for the plot
    
    subj, IC, trial, # which trial is of interest here 
    
    covariance_type, model_type, tol, n_mix, # infos we put in the .png name if we want to save it
    
    save=False # do we really want to save the figure?
):
    
    fig = plt.figure(figsize=(16, 5))

    # HMM states probability plot
    plt.subplot(211)
    plt.title('HMM States probability')
    time = data['time_axis'][np.abs(np.min(lags)):-np.abs(np.max(lags))]

    burst = np.argmax(max_power) # this is the burst state index
    
    labels = ['']
    states = np.where([i not in [burst] for i in range(n_states)])[0] # the other indexes
    for i in states:
        plt.fill_between(x=time, y1=gamma[:, i], alpha=0.2)
        plt.xlim(-4, 3)
        labels.append(f'state {i+1}')
    plt.plot(time, gamma[:, burst]>0.6, 'red')
    labels[0]=(f'burst state (state {burst+1})')
    plt.fill_between(x=time, y1=gamma[:, burst], alpha=0.2, color='red')
    plt.ylabel('State probability')
    plt.legend(labels, loc='upper right')

    # Time-frequency plot
    plt.subplot(212)

    plt.title('Wavelet transform')
    plt.imshow(data[f'tfr_256Hz subject{subj}, IC{IC}, trial{trial}'][0], 
               aspect='auto', origin='lower', extent=[-4, 3, 2, 50], cmap='RdBu_r')
    plt.xlabel('Time (s)')
    plt.ylabel('Frequencies (Hz)')
    plt.tight_layout()
    
    if save == True:
        plt.savefig(f'tde-hmm/tde-hmm_subj{subj}IC{IC}trial{trial}_{n_states}states_'
                    +covariance_type+'_'+model_type+f'_tol{tol}nmix{n_mix}.png', dpi=600)
        
#     plt.close(fig)
