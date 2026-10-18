"""A small, readable radix-2 Cooley--Tukey FFT implementation.

This module is intentionally written for teaching, not as a replacement for
NumPy.  It shows the divide-and-conquer idea used by fast Fourier transforms.
"""

from __future__ import annotations

import cmath
from typing import Sequence


def is_power_of_two(value: int) -> bool:
    """Return True when value is a positive power of two."""
    return value > 0 and (value & (value - 1)) == 0


def next_power_of_two(value: int) -> int:
    """Return the smallest power of two that is at least value."""
    if value < 1:
        raise ValueError("value must be positive")
    return 1 << (value - 1).bit_length()


def fft(samples: Sequence[complex]) -> list[complex]:
    """Compute the DFT of power-of-two-length samples using a recursive FFT.

    The DFT is X[k] = sum_n x[n] exp(-2 pi i k n / N).  Splitting the input
    into its even- and odd-indexed samples recursively reduces the work from
    O(N^2) to O(N log_2 N).
    """
    values = list(samples)
    count = len(values)
    if not is_power_of_two(count):
        raise ValueError("FFT input length must be a power of two")
    if count == 1:
        return values

    even = fft(values[::2])
    odd = fft(values[1::2])
    half = count // 2
    result = [0j] * count
    for k in range(half):
        twiddle = cmath.exp(-2j * cmath.pi * k / count) * odd[k]
        result[k] = even[k] + twiddle
        result[k + half] = even[k] - twiddle
    return result


def ifft(spectrum: Sequence[complex]) -> list[complex]:
    """Compute the inverse FFT using conjugation."""
    values = list(spectrum)
    count = len(values)
    return [value.conjugate() / count for value in fft([v.conjugate() for v in values])]

