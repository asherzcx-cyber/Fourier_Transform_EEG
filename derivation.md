# From Fourier Series to the Fourier Transform

## Goal

The Fourier transform answers a simple question: **how much of each frequency
is present in a signal?** The derivation begins with a periodic signal, whose
frequencies are discrete, and then lets its period grow without bound.

We use angular frequency \(\omega = 2\pi f\), where \(f\) is measured in hertz.

## 1. Complex Fourier series

Let \(x(t)\) be periodic with period \(T\):

$$
x(t+T)=x(t).
$$

Its fundamental angular frequency is

$$
\omega_0=\frac{2\pi}{T}.
$$

The complex Fourier series expresses the signal as a sum of harmonics:

$$
x(t)=\sum_{k=-\infty}^{\infty}c_k e^{ik\omega_0t}.
$$

To isolate coefficient \(c_m\), multiply both sides by
\(e^{-im\omega_0t}\) and integrate over a complete period:

$$
\int_{-T/2}^{T/2}x(t)e^{-im\omega_0t}\,dt
=
\sum_{k=-\infty}^{\infty}c_k
\int_{-T/2}^{T/2}e^{i(k-m)\omega_0t}\,dt.
$$

The complex exponentials are orthogonal over a period:

$$
\int_{-T/2}^{T/2}e^{i(k-m)\omega_0t}\,dt=
\begin{cases}
T,&k=m,\\
0,&k\ne m.
\end{cases}
$$

Only the \(k=m\) term survives. Therefore,

$$
c_k=\frac{1}{T}\int_{-T/2}^{T/2}x(t)e^{-ik\omega_0t}\,dt.
$$

## 2. From discrete frequencies to a continuum

The separation between neighboring Fourier-series frequencies is

$$
\Delta\omega=\omega_0=\frac{2\pi}{T}.
$$

When \(T\to\infty\), the signal no longer needs to repeat and
\(\Delta\omega\to0\). The discrete frequencies \(k\omega_0\) merge into a
continuous variable \(\omega\).

Define the limiting frequency function:

$$
X(\omega)=\int_{-\infty}^{\infty}x(t)e^{-i\omega t}\,dt.
$$

This is the **Fourier transform**. At a Fourier-series frequency,

$$
c_k=\frac{1}{T}X(k\omega_0)
=\frac{\Delta\omega}{2\pi}X(k\omega_0).
$$

Substituting this in the Fourier series gives

$$
x(t)=\sum_{k=-\infty}^{\infty}
\frac{\Delta\omega}{2\pi}X(k\omega_0)e^{ik\omega_0t}.
$$

This has the form of a Riemann sum. As \(\Delta\omega\to0\), it becomes an
integral:

$$
\boxed{x(t)=\frac{1}{2\pi}\int_{-\infty}^{\infty}X(\omega)e^{i\omega t}\,d\omega.}
$$

Thus the transform pair is

$$
\boxed{X(\omega)=\int_{-\infty}^{\infty}x(t)e^{-i\omega t}\,dt}
$$

and

$$
\boxed{x(t)=\frac{1}{2\pi}\int_{-\infty}^{\infty}X(\omega)e^{i\omega t}\,d\omega.}
$$

## 3. Why complex numbers appear

Euler's formula says

$$
e^{i\omega t}=\cos(\omega t)+i\sin(\omega t).
$$

So the transform compares a signal with sine and cosine waves of every
frequency. \(|X(\omega)|\) describes the amount of that frequency and
\(\arg X(\omega)\) describes its phase. For a real-valued EEG signal,

$$
X(-\omega)=X(\omega)^*,
$$

so negative and positive frequencies mirror one another.

## 4. The discrete Fourier transform

An EEG machine records samples \(x[0],x[1],\ldots,x[N-1]\), not a continuous
function. Its discrete Fourier transform (DFT) is

$$
\boxed{X[k]=\sum_{n=0}^{N-1}x[n]e^{-i2\pi kn/N}}
$$

for \(k=0,1,\ldots,N-1\). The inverse DFT is

$$
\boxed{x[n]=\frac{1}{N}\sum_{k=0}^{N-1}X[k]e^{i2\pi kn/N}.}
$$

For a sampled signal with sampling rate \(F_s\), bin \(k\) corresponds to

$$
f_k=\frac{kF_s}{N}, \qquad \Delta f=\frac{F_s}{N}.
$$

## 5. Why the FFT matters

A direct DFT needs about \(N^2\) arithmetic operations. The radix-2
Cooley--Tukey FFT divides a length-\(N\) input into its even and odd samples,
then combines their two length-\(N/2\) transforms:

$$
X[k]=E[k]+e^{-i2\pi k/N}O[k],
$$

$$
X[k+N/2]=E[k]-e^{-i2\pi k/N}O[k].
$$

Repeating this split produces an \(O(N\log_2N)\) algorithm. The FFT computes
the same DFT, just much more efficiently.

## 6. Application to this EEG recording

The supplied recording has sampling rate \(F_s=160\text{ Hz}\). For an
eight-second window, \(N=1280\), so

$$
\Delta f=\frac{160}{1280}=0.125\text{ Hz}.
$$

The Nyquist frequency is \(F_s/2=80\text{ Hz}\). The accompanying script
computes a spectrum of channel `Oz` and marks common EEG ranges: delta
(0.5--4 Hz), theta (4--8 Hz), alpha (8--13 Hz), beta (13--30 Hz), and gamma
(30--80 Hz). A frequency spectrum is a mathematical description of the
recording, not a medical diagnosis.

## Mathematical note

This is the standard derivation by a limiting Fourier series. A fully rigorous
inverse-transform theorem requires assumptions about the signal and more
advanced analysis; the formulas here apply to sufficiently well-behaved
signals.
