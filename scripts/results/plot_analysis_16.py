"""
==========================================
Plotting the analysis chain (Subject 16)
==========================================

Run the analysis.
"""

import sys
import os
import os.path as op
import numpy as np

import mne

from library.config import study_path
###############################################################################
# Configuration

subjects_dir = os.path.join(study_path, 'subjects')
meg_dir = os.path.join(study_path, 'MEG')

subject = "sub%03d" % int(16)

fname = op.join(study_path, 'ds117', subject, 'MEG', 'run_01_raw.fif')
raw = mne.io.read_raw_fif(fname)

fname = op.join(meg_dir, subject, 'run_01_filt_sss_raw.fif')
raw_filt = mne.io.read_raw_fif(fname)

###############################################################################
# Filtering
raw.plot_psd()
raw_filt.plot_psd()

###############################################################################
# Events
events = mne.read_events(op.join(meg_dir, subject, 'run_01_filt_sss-eve.fif'))
fig = mne.viz.plot_events(events, show=False)
fig.suptitle('Events from run 01')

epochs = mne.read_epochs(op.join(meg_dir, subject, subject + '-epo.fif'))
epochs.plot_drop_log()

###############################################################################
# Evoked responses
evo_fname = op.join(meg_dir, subject, '%s-ave.fif' % subject)
evoked = mne.read_evokeds(evo_fname)

###############################################################################
# Faces
famous_evo, scrambled_evo, unfamiliar_evo, contrast_evo, faces_evo = evoked
faces_evo.plot(spatial_colors=True, gfp=True, ylim={'eeg': (-10, 10)},
               window_title='Faces %s' % subject)

###############################################################################
# Famous
famous_evo.plot(spatial_colors=True, gfp=True,
                window_title='Famous %s' % subject)

###############################################################################
# Scrambled
scrambled_evo.plot(spatial_colors=True, gfp=True,
                   window_title='Scrambled %s' % subject)

###############################################################################
# Unfamiliar
unfamiliar_evo.plot(spatial_colors=True, gfp=True,
                    window_title='Unfamiliar %s' % subject)

###############################################################################
# Faces - scrambled
contrast_evo.plot(spatial_colors=True, gfp=True,
                  window_title='Faces - scrambled %s' % subject)

###############################################################################
# Topomaps
times = np.arange(0.05, 0.3, 0.025)
famous_evo.plot_topomap(times=times, title='Famous %s' % subject)
scrambled_evo.plot_topomap(times=times, title='Scrambled %s' % subject)
unfamiliar_evo.plot_topomap(times=times, title='Unfamiliar %s' % subject)
contrast_evo.plot_topomap(times=times, title='Faces - scrambled %s' % subject)

###############################################################################
# TFR
fpower = mne.time_frequency.read_tfrs(
    op.join(meg_dir, subject, '%s-faces-tfr.h5' % subject))[0]
fitc = mne.time_frequency.read_tfrs(
    op.join(meg_dir, subject, '%s-itc_faces-tfr.h5' % subject))[0]
spower = mne.time_frequency.read_tfrs(
    op.join(meg_dir, subject, '%s-scrambled-tfr.h5' % subject))[0]
sitc = mne.time_frequency.read_tfrs(
    op.join(meg_dir, subject, '%s-itc_scrambled-tfr.h5' % subject))[0]
channel = 'EEG070'
idx = [fpower.ch_names.index(channel)]
fpower.plot(idx, title='Faces power %s' % channel, baseline=(-0.1, 0.0),
            mode='logratio')
spower.plot(idx, title='Scrambled power %s' % channel, baseline=(-0.1, 0.0),
            mode='logratio')
fitc.plot(idx, title='Faces ITC %s' % channel, baseline=(-0.1, 0.0),
          mode='logratio')
sitc.plot(idx, title='Scrambled ITC %s' % channel, baseline=(-0.1, 0.0),
          mode='logratio')


###############################################################################
# Covariance
cov = mne.read_cov(op.join(meg_dir, subject, '%s-cov.fif' % subject))
mne.viz.plot_cov(cov, faces_evo.info)
faces_evo.plot_white(cov)
