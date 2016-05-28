import matplotlib.pyplot as plt
import numpy as np
from util import *
import scipy.signal as sgn

def notch_filter(fs, fr=60.0, r=0.98):
    """Get a second order notch filter"""

    z = []
    p = []
    for f_remov in fr:
        w0 = f_remov/fs*2*np.pi
        z.append(np.array([np.exp(1j*w0), np.exp(-1j*w0)]))
        p.append(np.array([r*np.exp(1j*w0), r*np.exp(-1j*w0)]))

    z = np.concatenate(z).reshape((len(fr)*2,))
    p = np.concatenate(p).reshape((len(fr)*2,))

    b, a = sgn.zpk2tf(z, p, 1)
    return b, a



