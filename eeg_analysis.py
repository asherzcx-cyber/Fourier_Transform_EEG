"""Make presentation-ready FFT plots from an EDF EEG recording.

Example:
    python eeg_analysis.py /Users/asherzcx/Downloads/S001R01.edf --channel Oz
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

import matplotlib.pyplot as plt
import numpy as np

from fft_from_scratch import fft, next_power_of_two


@dataclass
class EdfChannel:
    label: str
    physical_dimension: str
    physical_minimum: float
    physical_maximum: float
    digital_minimum: int
    digital_maximum: int
    samples_per_record: int


@dataclass
class EdfRecording:
    record_duration: float
    record_count: int
    channels: list[EdfChannel]
    data_start: int


def _field(raw: bytes, start: int, width: int) -> str:
    return raw[start : start + width].decode("latin-1").strip()


def _read_edf_header(handle: BinaryIO) -> EdfRecording:
    """Read the EDF fixed and per-signal headers.

    The included recording is ordinary 16-bit EDF data with an EDF+ annotation
    channel.  We parse the numeric channels directly and ignore annotations.
    """
    fixed = handle.read(256)
    if len(fixed) != 256:
        raise ValueError("File is too short to be a valid EDF recording.")
    header_bytes = int(_field(fixed, 184, 8))
    record_count = int(_field(fixed, 236, 8))
    record_duration = float(_field(fixed, 244, 8))
    signal_count = int(_field(fixed, 252, 4))
    signal_header = handle.read(header_bytes - 256)
    if len(signal_header) != header_bytes - 256:
        raise ValueError("EDF header is incomplete.")

    widths = [16, 80, 8, 8, 8, 8, 8, 80, 8, 32]
    columns: list[list[str]] = []
    offset = 0
    for width in widths:
        columns.append(
            [_field(signal_header, offset + index * width, width) for index in range(signal_count)]
        )
        offset += width * signal_count

    channels = [
        EdfChannel(
            label=columns[0][index],
            physical_dimension=columns[2][index],
            physical_minimum=float(columns[3][index]),
            physical_maximum=float(columns[4][index]),
            digital_minimum=int(columns[5][index]),
            digital_maximum=int(columns[6][index]),
            samples_per_record=int(columns[8][index]),
        )
        for index in range(signal_count)
    ]
    return EdfRecording(record_duration, record_count, channels, header_bytes)


def describe_edf(path: Path) -> EdfRecording:
    with path.open("rb") as handle:
        return _read_edf_header(handle)


def load_channel(path: Path, requested_label: str) -> tuple[np.ndarray, float, str]:
    """Load one non-annotation EDF channel and convert digital values to units."""
    with path.open("rb") as handle:
        recording = _read_edf_header(handle)
        normalized = requested_label.lower().rstrip(".")
        matches = [
            index
            for index, channel in enumerate(recording.channels)
            if channel.label.lower().rstrip(".") == normalized
        ]
        if not matches:
            labels = ", ".join(channel.label for channel in recording.channels[:-1])
            raise ValueError(f"Channel '{requested_label}' was not found. Available channels: {labels}")
        channel_index = matches[0]
        channel = recording.channels[channel_index]
        if channel.label.lower().startswith("edf annotations"):
            raise ValueError("Choose an EEG channel, not the EDF Annotations channel.")

        record_bytes = sum(item.samples_per_record for item in recording.channels) * 2
        digital_values: list[np.ndarray] = []
        for record in range(recording.record_count):
            offset = recording.data_start + record * record_bytes
            before = sum(item.samples_per_record for item in recording.channels[:channel_index]) * 2
            handle.seek(offset + before)
            raw = handle.read(channel.samples_per_record * 2)
            digital_values.append(np.frombuffer(raw, dtype="<i2").copy())

    digital = np.concatenate(digital_values).astype(float)
    scale = (channel.physical_maximum - channel.physical_minimum) / (
        channel.digital_maximum - channel.digital_minimum
    )
    signal = (digital - channel.digital_minimum) * scale + channel.physical_minimum
    sample_rate = channel.samples_per_record / recording.record_duration
    return signal, sample_rate, channel.physical_dimension


def band_power(frequencies: np.ndarray, power: np.ndarray, low: float, high: float) -> float:
    mask = (frequencies >= low) & (frequencies < high)
    return float(np.trapezoid(power[mask], frequencies[mask])) if np.any(mask) else 0.0


def analyze(path: Path, channel: str, start_seconds: float, window_seconds: float, output: Path) -> None:
    signal, sample_rate, unit = load_channel(path, channel)
    start = round(start_seconds * sample_rate)
    count = round(window_seconds * sample_rate)
    segment = signal[start : start + count]
    if len(segment) != count:
        raise ValueError("Selected window extends past the end of the recording.")

    # Removing the mean makes the zero-Hz offset less dominant. The Hann window
    # reduces spectral leakage at the two edges of the selected interval.
    centered = segment - np.mean(segment)
    windowed = centered * np.hanning(len(centered))
    n_fft = next_power_of_two(len(windowed))
    padded = np.pad(windowed, (0, n_fft - len(windowed)))
    spectrum = np.asarray(fft(padded.tolist()))
    frequencies = np.fft.rfftfreq(n_fft, d=1 / sample_rate)
    positive = spectrum[: len(frequencies)]
    power = np.abs(positive) ** 2 / (sample_rate * np.sum(np.hanning(len(centered)) ** 2))
    if len(power) > 2:
        power[1:-1] *= 2

    bands = [("Delta", 0.5, 4), ("Theta", 4, 8), ("Alpha", 8, 13), ("Beta", 13, 30), ("Gamma", 30, 80)]
    print(f"Channel: {channel} | sampling rate: {sample_rate:g} Hz | selected samples: {len(segment)}")
    for name, low, high in bands:
        print(f"{name:6s} ({low:>4g}-{high:<2g} Hz): {band_power(frequencies, power, low, high):.4g} {unit}²")

    time = (np.arange(len(segment)) + start) / sample_rate
    figure, axes = plt.subplots(2, 1, figsize=(11, 8), constrained_layout=True)
    axes[0].plot(time, segment, color="#193c6b", linewidth=0.8)
    axes[0].set(title=f"EEG signal: {channel} ({start_seconds:g}–{start_seconds + window_seconds:g} s)", xlabel="Time (seconds)", ylabel=f"Amplitude ({unit})")
    axes[0].grid(alpha=0.25)
    axes[1].plot(frequencies, power, color="#c0521d", linewidth=1.2)
    axes[1].set(xlim=(0, 45), title="Power spectrum computed with a from-scratch FFT", xlabel="Frequency (Hz)", ylabel=f"Power ({unit}²/Hz)")
    axes[1].grid(alpha=0.25)
    for _, low, high in bands[:4]:
        axes[1].axvline(low, color="gray", alpha=0.35, linewidth=0.8)
        axes[1].axvline(high, color="gray", alpha=0.35, linewidth=0.8)
    output.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(output, dpi=180)
    print(f"Saved figure to {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze one EDF EEG channel with a teaching FFT.")
    parser.add_argument("edf_file", type=Path, help="Path to an EDF recording")
    parser.add_argument("--channel", default="Oz", help="EEG channel label (default: Oz)")
    parser.add_argument("--start", type=float, default=5.0, help="Window start in seconds (default: 5)")
    parser.add_argument("--window", type=float, default=8.0, help="Window duration in seconds (default: 8)")
    parser.add_argument("--output", type=Path, default=Path("figures/eeg_fft_demo.png"), help="Output PNG path")
    args = parser.parse_args()
    analyze(args.edf_file, args.channel, args.start, args.window, args.output)


if __name__ == "__main__":
    main()

