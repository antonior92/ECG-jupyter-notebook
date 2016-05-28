import matplotlib.pyplot as plt
import numpy as np
from util import *
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

    # set initial threshold
    threshold = np.sqrt(2)*rms_xe

    # Length x
    N = len(x)

    # Get period lengh in integer units
    P = int(round(period*fs))

    # Get minimum period lengh in integer units
    minP = int(round(min_period*fs))

    # find number of periods in a signal
    nperiods = int(np.floor(N/P))

    # Tries to find one peak per period
    peaks = []
    start = 0
    end = start+int(round(P))
    for i in range(nperiods):
        max_ind_e = np.argmax(xe[start:end])+start
        max_ind = np.argmax(x[max_ind_e-minP:max_ind_e+minP])+max_ind_e-minP
        start = max_ind + minP
        end = start+int(round(P*1.5))
        peaks.append(max_ind*1/fs)

    return peaks

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
        start = max(0, peaks[i] - period)
        end = min(len(x)*1/fs, peaks[i] + period)
        interval.append((start, end))

    return interval
