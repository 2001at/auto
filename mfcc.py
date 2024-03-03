import wave
import numpy as np
import csv
import os
import sys

class FeatureExtractor():
    def __init__(self, sample_frequency=16000, frame_length=25, frame_shift=10, num_mel_bins=23,
                 num_ceps=13, lifter_coef=22, low_frequency=20, high_frequency=8000, dither=1.0):
        self.sample_freq = sample_frequency
        self.frame_size = int(sample_frequency * frame_length * 0.001)
        self.frame_shift = int(sample_frequency * frame_shift * 0.001)
        self.num_mel_bins = num_mel_bins
        self.num_ceps = num_ceps
        self.lifter_coef = lifter_coef
        self.low_frequency = low_frequency
        self.high_frequency = high_frequency
        self.dither_coef = dither

        self.fft_size = 1
        while self.fft_size < self.frame_size:
            self.fft_size *= 2

        self.mel_filter_bank = self.MakeMelFilterBank()
        self.dct_matrix = self.MakeDCTMatrix()
        self.lifter = self.MakeLifter()

    def Herz2Mel(self, herz):
        return (1127.0 * np.log(1.0 + herz / 700))

    def MakeMelFilterBank(self):
        mel_high_freq = self.Herz2Mel(self.high_frequency)
        mel_low_freq = self.Herz2Mel(self.low_frequency)
        mel_points = np.linspace(mel_low_freq, mel_high_freq, self.num_mel_bins + 2)

        dim_spectrum = int(self.fft_size / 2) + 1
        mel_filter_bank = np.zeros((self.num_mel_bins, dim_spectrum))
        for m in range(self.num_mel_bins):
            left_mel = mel_points[m]
            center_mel = mel_points[m + 1]
            right_mel = mel_points[m + 2]
            for n in range(dim_spectrum):
                freq = 1.0 * n * self.sample_freq / 2 / dim_spectrum
                mel = self.Herz2Mel(freq)
                if mel > left_mel and mel < right_mel:
                    if mel <= center_mel:
                        weight = (mel - left_mel) / (center_mel - left_mel)
                    else:
                        weight = (right_mel - mel) / (right_mel - center_mel)
                    mel_filter_bank[m][n] = weight

        return mel_filter_bank

    def ExtractWindow(self, waveform, start_index, num_samples):
        window = waveform[start_index:start_index + self.frame_size].copy()

        if self.dither_coef > 0:
            window = window + np.random.rand(self.frame_size) * (2 * self.dither_coef) - self.dither_coef

        window = window - np.mean(window)

        power = np.sum(window ** 2)
        if power < 1E-10:
            power = 1E-10
        log_power = np.log(power)

        window = np.convolve(window, np.array([1.0, -0.97]), mode='same')
        window[0] -= 0.97 * window[0]
        window *= np.hamming(self.frame_size)

        return window, log_power

    def ComputeFBANK(self, waveform):
        num_samples = np.size(waveform)
        num_frames = (num_samples - self.frame_size) // self.frame_shift + 1
        fbank_features = np.zeros((num_frames, self.num_mel_bins))
        log_power = np.zeros(num_frames)

        for frame in range(num_frames):
            start_index = frame * self.frame_shift
            window, log_pow = self.ExtractWindow(waveform, start_index, num_samples)

            spectrum = np.fft.fft(window, n=self.fft_size)
            spectrum = spectrum[:int(self.fft_size / 2) + 1]

            spectrum = np.abs(spectrum) ** 2

            fbank = np.dot(spectrum, self.mel_filter_bank.T)

            fbank[fbank < 0.1] = 0.1
            fbank_features[frame] = np.log(fbank)
            log_power[frame] = log_pow

        return fbank_features, log_power

    def MakeDCTMatrix(self):
        N = self.num_mel_bins
        dct_matrix = np.zeros((self.num_ceps, self.num_mel_bins))
        for k in range(self.num_ceps):
            if k == 0:
                dct_matrix[k] = np.ones(self.num_mel_bins) * 1.0 / np.sqrt(N)
            else:
                dct_matrix[k] = np.sqrt(2 / N) * np.cos(((2.0 * np.arange(N) + 1) * k * np.pi) / (2 * N))

        return dct_matrix

    def MakeLifter(self):
        Q = self.lifter_coef
        I = np.arange(self.num_ceps)
        lifter = 1.0 + 0.5 * Q * np.sin(np.pi * I / Q)
        return lifter

    def ComputeMFCC(self, waveform):
        fbank, log_power = self.ComputeFBANK(waveform)
        mfcc = np.dot(fbank, self.dct_matrix.T)
        mfcc *= self.lifter
        mfcc[:, 0] = log_power
        return mfcc

if __name__ == "__main__":
    wav_file_path = 'パワポ用実験/mixed_all_sample.wav'
    out_file_path = 'パワポ用実験/tyo2_mix_all_sample.csv'

    sample_frequency = 44100
    frame_length = 50
    frame_shift = 10
    low_frequency = 20
    high_frequency = sample_frequency / 2
    num_mel_bins = 23
    num_ceps = 13
    dither = 1.0

    np.random.seed(seed=0)

    feat_extractor = FeatureExtractor(
        sample_frequency=sample_frequency,
        frame_length=frame_length,
        frame_shift=frame_shift,
        num_mel_bins=num_mel_bins,
        num_ceps=num_ceps,
        low_frequency=low_frequency,
        high_frequency=high_frequency,
        dither=dither)

    with wave.open(wav_file_path, 'rb') as wav:
        if wav.getframerate() != sample_frequency:
            sys.stderr.write('The expected sampling rate is 44100.\n')
            exit(1)

        if wav.getnchannels() != 1:
            sys.stderr.write('This program supports monaural wav file only.\n')
            exit(1)

        num_samples = wav.getnframes()
        waveform = wav.readframes(num_samples)
        waveform = np.frombuffer(waveform, dtype=np.int16)

        mfcc = feat_extractor.ComputeMFCC(waveform)

    (num_frames, num_dims) = np.shape(mfcc)

    with open(out_file_path, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(mfcc)
        print("Finished writing to", out_file_path)
