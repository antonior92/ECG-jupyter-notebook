import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sgn


def find_ecgperiod(x, fs):
    """Find ECG period using autocorrelation sequence"""
    # Length x
    N = len(x)

    # Crosscorrelation
    r = np.correlate(x, x, "full")

    # normalize
    r = r[N-1:]/r[N-1]

    # Generate lag vector
    lag = np.arange(0, N)*1/fs

    # Get first value below zero
    negative_ind = next(x for x in range(len(r)) if r[x]<0)

    # Get maximum
    max_ind = (np.argmax(r[negative_ind:])+negative_ind)

    # First maximum
    first_max = max_ind/fs

    first_negative = negative_ind/fs

    return first_max, first_negative


def non_causal_diff(x, fs):
    """Aply non causal first diferential (central difference)"""

    # Length x
    N = len(x)

    # Diff
    diff = np.zeros(N)

    # Aproximate first diference fs/2*(x[t+1]-x[t-1])
    for t in range(1, N-1):
        diff[t] = fs/2*(x[t+1]-x[t-1])

    return diff


def enhance_ecg(x, fs):
    """Aply non causal first diferential followed by hilbert transform, obtaining
    a enhanced ecg signal apropriate for feature extraction"""

    y = non_causal_diff(x, fs)

    h = np.imag(sgn.hilbert(y))

    return h


def find_Rwave(x, xe, fs, period, min_period):
    """Tries to found R peak"""

    # Compute rms of enhanced signal
    rms_xe = xe.std()

    # set initial thresholds
    threshold_enhanced = np.sqrt(2)*rms_xe
    threshold = 0

    # Length x
    N = len(x)

    # Get period lengh in integer units
    P = int(round(period*fs))

    # Get minimum period lengh in integer units
    minP = int(round(min_period*fs))

    # find number of periods in a signal
    nperiods = int(np.floor(N/P))

    # Tries to find one peak per period
    count_peaks = 0
    start = 0
    end = start+int(round(P))
    max_peak = 0
    mean_peaks = 0
    max_e_peak = 0
    mean_e_peaks = 0
    for i in range(nperiods):
        max_ind_e = np.argmax(xe[start:end])+start
        max_e = xe[max_ind_e]
        max_ind = np.argmax(x[max_ind_e-minP:max_ind_e+minP])+max_ind_e-minP
        max_p = x[max_ind]
        start = max_ind + minP
        end = start+int(round(P*1.5))
        if max_e > threshold_enhanced and max_p > threshold:
            count_peaks += 1
            max_peak = max((max_peak, max_p))
            max_e_peak = max((max_e_peak, max_e))
            mean_peaks += max_p
            mean_e_peaks += max_e

    # divide mean
    mean_e_peaks = mean_e_peaks/count_peaks
    mean_peaks = mean_peaks/count_peaks

    # update thresholds
    threshold_enhanced = max((threshold_enhanced+2*mean_e_peaks-max_e_peak)/2, threshold_enhanced)
    threshold = max(3*mean_peaks-2*max_peak, threshold)

    # Choose all peaks above both thresholds
    peaks = []
    i_prev = -1000
    for i in range(len(x)):
        if xe[i] > threshold_enhanced:
            max_ind = np.argmax(x[i-minP:i+minP])+i-minP
            if  x[max_ind] > threshold:
                if i-i_prev > minP: 
                    peaks.append(max_ind*1/fs)
                    i_prev = i

    return peaks

def find_Swave(x, xe, fs, period, min_period):
    return find_Rwave(-x, -xe, fs, period, min_period)

def subdivide_ecg(x, fs, peaks, period):
    # Length x
    N = len(x)

    # Get period lengh in integer units
    P = int(round(period*fs))

    # find number of periods in a signal
    nperiods = len(peaks)

    interval = []
    start = 0
    end = 0
    for i in range(1,nperiods-1):
        start = peaks[i-1]
        center = peaks[i]
        end = peaks[i+1]
        interval.append((start, center, end))

    return interval
