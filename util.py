from ECGManager import *
from feature_detection import *
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sgn

# Usefull functions and routines for ECG Project #


def get_signal(exam_number=0, lead_number=0):
    """Read one ECG signal from database"""

    manager = ECGManager()
    N = manager.contar_qtd_exames()
    examlist = manager.buscar_lista_exames(N)
    exam = manager.buscar_exame_completo(examlist[exam_number][0])
    content = exam.conteudo_ecg[0]
    lead = content.derivacoes[lead_number]

    x = np.array(lead.amostra)/1000.0
    fs = float(content.velocidade)

    return (x, fs)


def print_info(exam_number=0):
    """ Print some usefull information aboat an exam"""

    manager = ECGManager()
    N = manager.contar_qtd_exames()
    examlist = manager.buscar_lista_exames(N)
    exam = manager.buscar_exame_completo(examlist[exam_number][0])
    content = exam.conteudo_ecg[0]

    print "60 Hz filter = " + str(content.filtro_60_hz)
    print "Muscular filter = " + str(content.filtro_muscular)
    print "Sample Rate = " + str(content.velocidade) + "Hz"
    return


def get_signal_txt(fname):
    """Read one ECG signal from txt"""

    x = np.loadtxt(fname)

    return x


def plot_signal(x, fs=1):
    """Plot one ECG lead signal"""

    tmax = len(x)*1/fs

    # Create time vector
    t = np.arange(len(x))*1/fs

    # Plot
    f, ax = plt.subplots(figsize=(12,10))
    ax.plot(t, x, 'k')
    ax.set_ylabel("Voltage(mV)", fontsize=18, labelpad=30)
    ax.set_xlabel("Time(s)", fontsize=18)
    ax.axis([0, tmax, round(1.2*min(x),1), round(1.2*max(x),1)])
    ax.set_xticks(np.arange(0, tmax+0.2, 0.2), minor=True)
    ax.set_yticks(np.arange(round(1.2*min(x),1), round(1.2*max(x),1), 0.1), minor=True)
    ax.grid(which='minor')
    ax.grid()

    return


def plot_freq_respose(b, a, fs, xaxis=None):
    """Plot Frequency Response of Digital Filter"""

    w, h = sgn.freqz(b, a)
    freq = w/(2*np.pi)*fs
    f, ax = plt.subplots( figsize=(12,10))
    ax.plot(freq, 20*np.log10(abs(h)))
    ax.set_ylabel("Gain(dB)", fontsize=18, labelpad=30)
    ax.grid()
    ax.set_xlabel("Frequency(Hz)", fontsize=18)
    if xaxis:
        ax.set_xlim(xaxis)

    return


def plot_fft(x, fs, n=2**16, xaxis=None):
    """Plot fft using hamming windown and zeropading"""

    # length x
    N = len(x)

    # Hamming window
    w = np.hamming(N)

    # Pre multiply signal by hamming window
    xw = x*w

    # compute fft
    X = np.fft.fft(xw, n)

    X = X[0:n/2]

    # Get spectral power
    psdx = (1/(fs*n))*abs(X)**2

    # get frequency grid
    f = np.arange(0, len(X))*fs/n

    
    fig, ax = plt.subplots(figsize=(12,10))
    ax.plot(f, psdx)
    ax.set_ylabel("Power Spectral Density", fontsize=18, labelpad=30)
    ax.set_xlabel("Frequency(Hz)", fontsize=18, labelpad=20)
    if xaxis:
        ax.set_xlim(xaxis)
    ax.grid()



def plot_fft_log(x, fs, n=2**16, xaxis=None):
    """Plot fft using hamming windown and zeropading"""

    # length x
    N = len(x)

    # Hamming window
    w = np.hamming(N)

    # Pre multiply signal by hamming window
    xw = x*w

    # compute fft
    X = np.fft.fft(xw, n)

    X = X[0:n/2]

    # Get spectral power
    psdx = (1/(fs*n))*abs(X)**2

    # get frequency grid
    f = np.arange(0, len(X))*fs/n

    fig, ax = plt.subplots(figsize=(12,10))
    ax.plot(f, 10*np.log10(psdx))
    ax.set_ylabel("Power Spectral Density (dB/Hz)", fontsize=18, labelpad=30)
    ax.set_xlabel("Frequency(Hz)", fontsize=18)
    if xaxis:
        ax.set_xlim(xaxis)
    ax.grid()


def plot_crosscorr(x, fs, xaxis=None):
    """Plot Autocorrelation Sequence"""

    # Length x
    N = len(x)

    # Crosscorrelation
    r = np.correlate(x, x, "full")

    # normalize
    r = r[N-1:]/r[N-1]

    # Generate lag vector
    lag = np.arange(0, N)*1/fs

    fig, ax = plt.subplots(figsize=(12,10))
    ax.plot(lag, r)
    ax.grid()
    ax.set_ylabel("Autocorrelation", fontsize=18, labelpad=30)
    ax.set_xlabel("Lag(s)", fontsize=18)
    if xaxis:
        ax.set_xlim(xaxis)
    else:
        ax.set_xlim([0, 2])


def plot_peaks(x, fs, peaks):
    """Plot one ECG lead signal"""

    tmax = len(x)*1/fs

    # Create time vector
    t = np.arange(len(x))*1/fs

    # Plot
    f, ax = plt.subplots(figsize=(12,10))
    ax.plot(t, x, 'k')
    for p in peaks:
        index = int(round(fs*p))
        ax.plot(t[index], x[index], 'ro', markersize=10)
    ax.set_ylabel("Voltage(mV)", fontsize=18, labelpad=30)
    ax.set_xlabel("Time(s)", fontsize=18)
    ax.axis([0, tmax, 1.2*min(x), 1.2*max(x)])
    ax.set_xticks(np.arange(0, tmax+0.2, 0.2), minor=True)
    ax.set_yticks(np.arange(1.2*min(x), 1.2*max(x), 0.1), minor=True)
    ax.grid(which='minor')
    ax.grid()

    return

def plot_entangled_signal(x, fs, interval, period):
    """Plot several signal arts in the same plot"""

    # Find maximum interval
    right_extrem = 0
    left_extrem = 0
    for interv in interval:
        if interv[1]-interv[0] > left_extrem:
            left_extrem = interv[1]-interv[0]

        if interv[2]-interv[1] > right_extrem:
            right_extrem = interv[2]-interv[1]

    left_extrem = int(np.ceil(left_extrem*fs))+1
    right_extrem = int(np.ceil(right_extrem*fs))+1


    # Create mean vector
    xmean = np.zeros(right_extrem+left_extrem)

    # Plot
    f, ax = plt.subplots(figsize=(12,10))
    for interv in interval:
        # Get start end and center
        start = int(round(interv[0]*fs))
        center = int(round(interv[1]*fs))
        end = int(round(interv[2]*fs))
        
        # Create time vector
        t = (np.arange(len(x[start:end])) - (center-start))
        plt.plot(t/fs, x[start:end])
        xmean[(left_extrem+min(t)):(left_extrem+max(t)+1)] += x[start:end]/len(interval)

    t = (np.arange(len(xmean)) - left_extrem)
    plt.plot(t/fs, xmean, color='black', linewidth=4)
    ax.set_ylabel("Voltage(mV)", fontsize=18, labelpad=30)
    ax.set_xlabel("Time(s)", fontsize=18)
    ax.axis([-0.6*period, 0.6*period, 1.2*min(x), 1.2*max(x)])
    ax.set_xticks(np.arange(-0.6*period, 0.6*period, 0.2), minor=True)
    ax.set_yticks(np.arange(1.2*min(x), 1.2*max(x), 0.1), minor=True)
    ax.grid(which='minor')
    ax.grid()

    return

