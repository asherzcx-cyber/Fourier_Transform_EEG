# Fourier Transform and EEG: Finding Frequencies Hidden in Brain Waves

> **Question:** An EEG trace looks irregular over time. Can mathematics reveal
> the rhythms hidden inside it?

This project derives the Fourier transform from the Fourier series, implements
the Fast Fourier Transform (FFT) from scratch, and applies it to a real
experimental EEG recording. The continuous Fourier transform supplies the
mathematical derivation; because the EEG was sampled at 160 Hz, the program
actually computes a discrete Fourier transform (DFT) using an FFT algorithm.

## Interactive presentation website

The repository also includes a browser-based interactive presentation in
[`docs/index.html`](docs/index.html). It has the real EEG result plus a live
two-wave mixer: changing the waves immediately changes the displayed DFT
spectrum. Follow [the short GitHub Pages instructions](docs/README.md) to put
it online.

![Eight seconds of the Oz EEG signal and its FFT power spectrum](figures/eeg_fft_demo.png)

## The main idea

The top graph shows a real EEG voltage trace changing over time. The lower
graph is the **same data**, but described by frequency. Tall peaks mean that
those frequencies contribute strongly to the selected signal segment.

The Fourier transform does not throw information away. It changes the question:

| Time domain | Frequency domain |
| --- | --- |
| “How does the voltage change at each moment?” | “Which repeating frequencies make up the voltage?” |

---

## 1. What does EEG measure?

**Electroencephalography (EEG)** uses electrodes on the scalp to measure tiny
changes in voltage created by the combined electrical activity of many neurons.
It does not directly record an individual neuron, thought, or diagnosis.

The demonstration recording, `S001R01.edf`, contains:

| Property | Value |
| --- | --- |
| EEG channels | 64 |
| Demonstration electrode | `Oz`, near the back of the head |
| Sampling rate | \(F_s=160\text{ Hz}\) |
| Recording duration | 61 seconds |
| Analysis window | 8 seconds, from 5 s to 13 s |

The EEG machine samples the voltage 160 times per second. That produces a
sequence of numbers, which is exactly the kind of data the DFT and FFT analyze.

> This is an educational signal-processing demonstration, not clinical EEG
> analysis or medical interpretation.

---

## 2. Why can we apply a Fourier transform to EEG?

EEG is a time-varying signal. It is reasonable to model a short segment as a
mixture of oscillations at different frequencies plus noise and artifacts:

$$
\text{EEG}(t)\approx\sum_j A_j\cos(2\pi f_jt+\phi_j)+\text{noise}.
$$

The Fourier transform tests the signal against sine and cosine waves at every
frequency. It tells us which frequencies best match patterns that occur in the
recording.

EEG often contains rhythms in ranges such as these:

| Band | Frequency range |
| --- | --- |
| Delta | 0.5–4 Hz |
| Theta | 4–8 Hz |
| Alpha | 8–13 Hz |
| Beta | 13–30 Hz |
| Gamma | 30–80 Hz |

These labels describe frequency ranges, not a diagnosis. A peak in a spectrum
only says that a component at that frequency was strong in this selected
segment.

---

## 3. Mathematical starting point: Fourier series

Suppose first that a signal \(x(t)\) is perfectly periodic with period \(T\):

$$
x(t+T)=x(t).
$$

Its fundamental angular frequency is

$$
\omega_0=\frac{2\pi}{T}.
$$

Fourier series says that it can be written as a sum of harmonics:

$$
\boxed{x(t)=\sum_{k=-\infty}^{\infty}c_k e^{ik\omega_0t}.}
$$

Here \(c_k\) is the amount of frequency \(k\omega_0\). Complex exponentials
are useful because Euler's formula combines sine and cosine in one expression:

$$
e^{i\omega t}=\cos(\omega t)+i\sin(\omega t).
$$

To find the coefficient \(c_m\), multiply by \(e^{-im\omega_0t}\) and
integrate over one period:

$$
\int_{-T/2}^{T/2}x(t)e^{-im\omega_0t}\,dt
=\sum_{k=-\infty}^{\infty}c_k
\int_{-T/2}^{T/2}e^{i(k-m)\omega_0t}\,dt.
$$

The exponential waves are orthogonal over one period:

$$
\int_{-T/2}^{T/2}e^{i(k-m)\omega_0t}\,dt=
\begin{cases}
T, & k=m,\\
0, & k\ne m.
\end{cases}
$$

So every term disappears except \(k=m\), leaving

$$
\boxed{c_k=\frac{1}{T}\int_{-T/2}^{T/2}x(t)e^{-ik\omega_0t}\,dt.}
$$

---

## 4. Deriving the Fourier transform

An EEG is not perfectly periodic. To move from Fourier series to a
non-repeating signal, imagine letting its period grow indefinitely.

The gap between adjacent Fourier-series frequencies is

$$
\Delta\omega=\omega_0=\frac{2\pi}{T}.
$$

As \(T\to\infty\), \(\Delta\omega\to0\). The discrete frequencies
\(k\omega_0\) fill a continuum, and the sum becomes an integral.

Define

$$
X(\omega)=\int_{-\infty}^{\infty}x(t)e^{-i\omega t}\,dt.
$$

Since \(1/T=\Delta\omega/(2\pi)\), the Fourier-series sum becomes the Riemann
sum

$$
x(t)=\sum_{k=-\infty}^{\infty}
\frac{\Delta\omega}{2\pi}X(k\omega_0)e^{ik\omega_0t}.
$$

Taking the limit \(\Delta\omega\to0\) gives the inverse transform:

$$
\boxed{x(t)=\frac{1}{2\pi}\int_{-\infty}^{\infty}X(\omega)e^{i\omega t}\,d\omega.}
$$

Therefore the Fourier transform pair is

$$
\boxed{X(\omega)=\int_{-\infty}^{\infty}x(t)e^{-i\omega t}\,dt}
$$

and

$$
\boxed{x(t)=\frac{1}{2\pi}\int_{-\infty}^{\infty}X(\omega)e^{i\omega t}\,d\omega.}
$$

For a real signal such as EEG, negative frequencies mirror positive
frequencies:

$$
X(-\omega)=X(\omega)^*.
$$

That is why the plotted spectrum shows only the nonnegative frequencies.

---

## 5. The discrete Fourier transform for sampled EEG

The computer does not receive a continuous function. It receives \(N\) samples:

$$
x[0],x[1],\ldots,x[N-1].
$$

The **discrete Fourier transform (DFT)** is

$$
\boxed{X[k]=\sum_{n=0}^{N-1}x[n]e^{-i2\pi kn/N}}
$$

and its inverse is

$$
\boxed{x[n]=\frac{1}{N}\sum_{k=0}^{N-1}X[k]e^{i2\pi kn/N}.}
$$

For sampling rate \(F_s\), the frequency of DFT bin \(k\) is

$$
f_k=\frac{kF_s}{N}.
$$

This demo uses an eight-second segment, so

$$
N=8\text{ s}\times160\text{ samples/s}=1280\text{ samples}.
$$

The meaningful frequency resolution is

$$
\boxed{\Delta f=\frac{F_s}{N}=\frac{160}{1280}=0.125\text{ Hz}.}
$$

The highest representable frequency is the **Nyquist frequency**:

$$
\boxed{f_{\text{Nyquist}}=\frac{F_s}{2}=80\text{ Hz}.}
$$

---

## 6. Why the FFT is fast

Computing the DFT directly needs about \(N^2\) operations. The
Cooley–Tukey FFT splits the input into its even and odd samples, calculates
two smaller transforms, then combines them:

$$
X[k]=E[k]+e^{-i2\pi k/N}O[k],
$$

$$
X[k+N/2]=E[k]-e^{-i2\pi k/N}O[k].
$$

Repeating that split reduces the work to approximately

$$
\boxed{O(N\log_2N).}
$$

The FFT is **not** a different transform; it is a much faster algorithm for
computing the same DFT. See the implementation in
[fft_from_scratch.py](fft_from_scratch.py).

---

## 7. Live demo: reproduce the EEG figure

Install the two required packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then run the analysis with the EDF file:

```bash
python3 eeg_analysis.py /path/to/S001R01.edf --channel Oz
```

The program performs these steps:

1. Reads the `Oz` voltage samples from the EDF file.
2. Removes the average voltage and applies a Hann window to reduce edge effects.
3. Pads the 1280 values to 2048 values so the recursive radix-2 FFT can run.
4. Computes \(\lvert X[k]\rvert^2\), the power at each frequency.
5. Saves `figures/eeg_fft_demo.png`.

Example output from this recording:

```text
Channel: Oz | sampling rate: 160 Hz | selected samples: 1280
Delta  ( 0.5-4  Hz): 740.7 uV²
Theta  (   4-8  Hz): 199.4 uV²
Alpha  (   8-13 Hz): 123.8 uV²
Beta   (  13-30 Hz): 305.9 uV²
Gamma  (  30-80 Hz): 33.67 uV²
```

Zero-padding makes the recursive FFT possible and samples the plotted spectrum
more densely; it does **not** improve the true \(0.125\text{ Hz}\) resolution
set by the original eight-second recording window.

Try different electrodes:

```bash
python3 eeg_analysis.py /path/to/S001R01.edf --channel O1
python3 eeg_analysis.py /path/to/S001R01.edf --channel Cz
python3 eeg_analysis.py /path/to/S001R01.edf --channel Fz
```

---

## 8. Suggested class walkthrough

1. **Show the figure.** Ask what could be hidden in the messy time-domain signal.
2. **Explain EEG.** It is sampled scalp voltage, not a medical diagnosis.
3. **Show the Fourier series.** A periodic signal is built from harmonics.
4. **Take the infinite-period limit.** This produces the Fourier transform.
5. **Show the DFT and FFT.** Sampling gives the DFT; the FFT speeds it up.
6. **Return to the figure.** The frequency plot exposes the component rhythms.

## Questions you might get

**Why use a window?** A finite segment has abrupt endpoints. A Hann window
softens them and reduces spectral leakage, where an edge spreads energy across
many frequencies.

**Why are there no negative frequencies in the plot?** For a real EEG signal,
the negative side is the mirror image of the positive side.

**Can NumPy calculate this more simply?** Yes. This project writes the FFT
recursively from scratch so the mathematical algorithm is visible, then checks
it against NumPy for correctness.

**What assumptions are hidden in the derivation?** This standard derivation
assumes a sufficiently well-behaved signal. A fully rigorous inverse-transform
theorem belongs to more advanced real and functional analysis.

---

## Files in this repository

| File | Purpose |
| --- | --- |
| [README.md](README.md) | Complete presentation and reproducible demo |
| [derivation.md](derivation.md) | Standalone derivation handout |
| [fft_from_scratch.py](fft_from_scratch.py) | Recursive Cooley–Tukey FFT code |
| [eeg_analysis.py](eeg_analysis.py) | EDF loader, analysis, and plotting code |
| [presentation.md](presentation.md) | Alternative short presentation outline |
| [data/README.md](data/README.md) | Local data-file instructions |
