import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import numpy, os, csv
from scipy.signal import butter, filtfilt

def record_voice(out_name=None, channels=1, fs=44100, duration=2, dtype='float64'):
    '''
    out_name : str (directory)
               If not None, writes to file.
    channels: 1 for mono, 2 for stereo
    duration : In seconds
    dtype : 'int16' for 16 bit, float64 for 32 bit rate.
    fs : int
         Sampling frequency
    '''
    myrecording = sd.rec(duration * fs, samplerate=fs, channels=channels,dtype=dtype)
    sd.wait()
    if out_name: # Writes to file
        wav.write('%s.wav'%out_name, data=myrecording, rate=fs)

    return myrecording



#--- Based on Jarne (2017) "Simple empirical algorithm to obtain signal envelope in three steps"
def _get_envelope(signal, fs=44100, N=200, cutoff=2000):
    '''
    signal: input wav (numpy.ndarray)
    fs: sampling frequency
    N: number of samples per chunk (in part (2))
    cutoff: LPF cutoff, the smaller the cuttoff the stronger the filter. (tweek this).
    '''
    # 1) Take the absolute value of the signal
    abs_signal = abs(signal)
    # 2) Seperate into samples of N, and get peak value of each sample.
    chunked_signal = [abs_signal[i:i+N] for i in range(0, len(abs_signal), N)]
    new_signal = []
    for chunk in chunked_signal: #Then for each chunk, replace all values by max value
        max_value = np.max(chunk)
        new_chunk = [max_value for i in range(len(chunk))]
        new_signal.append(new_chunk)
    # new_signal = np.array(new_signal).flatten()
    new_signal = np.array([item for sublist in new_signal for item in sublist]) # flatten list of lists
    # 3) LPF the new_signal (the envelope, not the original signal)
    def FilterSignal(signal_in, fs, cutoff):
        B, A = butter(1, cutoff / (fs / 2.0), btype='low')
        filtered_signal = filtfilt(B, A, signal_in, axis=0)
        return filtered_signal
    filteredSignal = FilterSignal(new_signal, fs, cutoff)

    return filteredSignal




# Note The threshold depends also on the input volume set on the computer
def _get_voice_onset(signal, threshold = 200, fs=44100, min_time=100):
    '''
    signal : numpy.ndarray
             signal in. Should be the envelope of the raw signal for accurate results
    threshold : int
                Amplitude threshold for voice onset.
                (Threshold = 200 with NYUAD MEG mic at 75% input volume seems to work well)
    fs : int
         Sampling frequency
    min_time : int (ms)
             Time in ms after the threshold is crossed used to calculate
              the median amplitude and decide if it was random burst of noise
              or speech onset.
    '''

    n_above_thresh = int(fs/min_time) # convert time above threshold to number of samples.

    indices_onset = np.where(signal >= threshold)[0] # All indices above threshold
    # Next, find the first index that where the MEDIAN stays above threshold for the next 10ms
    # Not using the MEAN because sensitive to a single extreme value
    # Note 44.1 points per millesconds (for fs=44100)
    # 10ms = 441 points
    for i in indices_onset:
        median_mintime = np.median(np.abs(signal[i:i+n_above_thresh])) # median value in the timewindow of length min_time
        if median_mintime >= threshold:
            idx_onset = i
            onset_time = idx_onset / float(fs) * 1000.0

            return idx_onset, onset_time
    return np.nan, np.nan # if no point exceeds the threshold.
                          # Return "None" instead of None in order to be able to append it to a list later on



# LPF function: used in _get_envelope() but here for seperate use.
def FilterSignal(signal_in, fs=44100, cutoff=200):
    '''
    signal_in : numpy.ndarray
                Input .wav signal
    fs : int
         Sampling frequency
    cutoff : int
             LPF cutoff (200 works well with NYUAD MEG mic)
    '''
    B, A = butter(1, cutoff / (fs / 2.0), btype='low')
    filtered_signal = filtfilt(B, A, signal_in, axis=0)
    return filtered_signal



def auto_utterance_times(signal, fs, threshold=200, min_time=100):
    '''
    Automatically get utterance times.
    Returns idx and rt (ms)
    signal, fs : np.array, int
                 fs, signal = wav.read(file_in)
    threshold, min_time : see _get_voice_onset()
    Returns
    ---------
    idx : index of utterance time
    rt : in milliseconds
    '''
    flt_signal = FilterSignal(signal,fs=fs)
    env = _get_envelope(flt_signal,fs=fs)
    idx, rt = _get_voice_onset(env,fs=fs, threshold=threshold, min_time=min_time)

    return idx, rt


