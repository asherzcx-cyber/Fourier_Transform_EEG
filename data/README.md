# EEG data

The demonstration uses `S001R01.edf`, an EDF-format experimental EEG
recording. The data file is intentionally not committed to the repository.

To reproduce the figure, put a copy of the recording in this folder or point
the analysis script at its location:

```bash
python3 eeg_analysis.py /path/to/S001R01.edf --channel Oz
```

The file contains 64 EEG channels sampled at 160 Hz for 61 seconds, plus an
EDF annotation channel. This repository uses it only for educational
signal-processing analysis and makes no clinical claims.

