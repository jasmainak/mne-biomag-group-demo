"""
=========================
PSD (linear vs log scale)
=========================

The Power Spectral Density (PSD) plot shows different information for
linear vs. log scale. We will demonstrate here how the PSD plot can be
used to conveniently spot bad sensors.
"""
import sys
import os
import os.path as op

import mne

from library.config import study_path, map_subjects

###############################################################################
# First some basic configuration as in all scripts

subjects_dir = os.path.join(study_path, 'subjects')

subject_id = 10
run = 2
subject = "sub%03d" % int(subject_id)

fname = op.join(study_path, 'ds117', subject, 'MEG', 'run_%02d_raw.fif' % run)
raw = mne.io.read_raw_fif(fname, preload=True)

###############################################################################
# Next, we get the list of bad channels
mapping = map_subjects[subject_id]
bads = list()
bad_name = op.join(op.dirname(sys.argv[0]), '..', 'processing',
                   'bads', mapping, 'run_%02d_raw_tr.fif_bad' % run)
if os.path.exists(bad_name):
    with open(bad_name) as f:
        for line in f:
            bads.append(line.strip())

###############################################################################
# and set the EOG/ECG channels appropriately

raw.set_channel_types({'EEG061': 'eog',
                       'EEG062': 'eog',
                       'EEG063': 'ecg',
                       'EEG064': 'misc'})  # EEG064 free floating el.
raw.rename_channels({'EEG061': 'EOG061',
                     'EEG062': 'EOG062',
                     'EEG063': 'ECG063'})

raw.pick_types(eeg=True, meg=False)

###############################################################################
# MNE also displays the cutoff frequencies of the online filters, but here
# we remove it from the info and show only the HPI coil frequencies.

raw.info['lowpass'] = None
raw.info['highpass'] = None
raw.info['line_freq'] = None

###############################################################################
# The line colors for the bad channels will be red.

colors = ['k'] * raw.info['nchan']
for b in bads:
    colors[raw.info['ch_names'].index(b)] = 'r'

# this channel should have been marked bad (subject=14, run=01)
# colors[raw.info['ch_names'].index('EEG024')] = 'g'

###############################################################################
# First we show the log scale to spot bad sensors.

import matplotlib.pyplot as plt  # noqa
from library.config import set_matplotlib_defaults  # noqa

set_matplotlib_defaults(plt)
fig = raw.plot_psd(average=False, line_alpha=0.6,
                   fmin=0, fmax=350, xscale='log',
                   spatial_colors=False, show=False)
plt.xlabel('Frequency (Hz)')

lines = plt.gca().get_lines()
for l, c in zip(lines, colors):
    if c == 'r':
        l.set_color(c)
        l.set_linewidth(2.)
        l.set_zorder(-1)

fig.tight_layout()
plt.show()
fig.savefig('psdA.pdf', bbox_to_inches='tight')

###############################################################################
# Next, the linear scale to check power line frequency

fig = raw.plot_psd(average=False, line_alpha=0.6, n_fft=2048, n_overlap=1024,
                   fmin=0, fmax=350, xscale='linear', spatial_colors=False)
plt.xlabel('Frequency (Hz)')
plt.ylabel('')

plt.axvline(50., linestyle='--', alpha=0.25, linewidth=2)
plt.axvline(50., linestyle='--', alpha=0.25, linewidth=2)
# HPI coils
for freq in [293., 307., 314., 321., 328.]:
    plt.axvline(freq, linestyle='--', alpha=0.25, linewidth=2)

plt.tight_layout()
fig.savefig('psdB.pdf', bbox_to_inches='tight')
