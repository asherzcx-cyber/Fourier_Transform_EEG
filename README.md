# Fourier Transform and EEG

> How can a complicated brain-wave recording be described as a combination of
> simple waves?

This math-class project derives the Fourier transform from the Fourier series,
implements a Fast Fourier Transform (FFT) from scratch, and applies it to a
real experimental EEG recording.

## Start here

**For a class presentation, open [the presentation walkthrough](presentation.md).**
It is organized as a short talk with speaker cues, equations, and the real EEG
result. The remaining files let classmates inspect the mathematics and code.

![An Oz EEG trace and its FFT power spectrum](figures/eeg_fft_demo.png)

## Project map

| File | Purpose |
| --- | --- |
| [presentation.md](presentation.md) | Class-ready walkthrough and speaking outline |
| [derivation.md](derivation.md) | Full Fourier series → Fourier transform → DFT derivation |
| [fft_from_scratch.py](fft_from_scratch.py) | Readable recursive Cooley--Tukey FFT |
| [eeg_analysis.py](eeg_analysis.py) | EDF reader, analysis, and figure generator |
| [figures/eeg_fft_demo.png](figures/eeg_fft_demo.png) | Plot generated from the supplied recording |
| [data/README.md](data/README.md) | How to work with the local EDF file |

## Set up and run

Create a Python environment and install the two packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then analyze the supplied EDF recording:

```bash
python eeg_analysis.py /Users/asherzcx/Downloads/S001R01.edf --channel Oz
```

The command writes `figures/eeg_fft_demo.png`. It also prints an approximate
band-power summary to the terminal. Try another electrode with, for example,
`--channel O1`, `--channel Cz`, or `--channel Fz`.

## Recording used in the demo

`S001R01.edf` has 64 EEG channels sampled at 160 Hz for 61 seconds, plus one
EDF annotation channel. It is not copied into this repository, both to keep the
repository small and to make the source of the data explicit.

For the default eight-second window:

$$
N = 8 \times 160 = 1280
$$

The FFT implementation pads this to 2048 samples because the recursive
Cooley--Tukey algorithm uses a power-of-two input. The original observation
window still determines the meaningful frequency resolution:

$$
\Delta f = \frac{160}{1280} = 0.125\ \text{Hz}.
$$

The 160 Hz sampling rate means frequencies above 80 Hz cannot be represented
without aliasing; 80 Hz is the Nyquist frequency.

## Suggested presentation story

1. Start with the question: “Which frequencies are hidden in this EEG signal?”
2. Derive the Fourier transform by making the Fourier-series period infinite.
3. Introduce the DFT for sampled data.
4. Explain that the FFT is a faster way to compute the same DFT.
5. Show the code’s time-domain signal and its frequency spectrum.
6. Point out the standard EEG frequency bands without making medical claims.

## Important scope note

This is an educational signal-processing demonstration, not clinical EEG
analysis or medical interpretation.
