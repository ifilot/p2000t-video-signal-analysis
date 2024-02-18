# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import scipy

def main():
    # load data
    time, ch1, ch2 = get_data()
    
    # find signal that provides best match with hsync
    x0 = int((1e-5 - time[0]) / 4.1909516e-09)
    x1 = x0 + 100000
    fh, oh, dch, hmax = align_signal(time[x0:x1], ch1[x0:x1], 15625, 1.55e-5, 0.93)
    
    # plt.figure(dpi=144, figsize=(12,4))
    # plt.plot(time[x0:x1], ch1[x0:x1])
    # plt.plot(time[x0:x1], (0.5 * scipy.signal.square((time[x0:x1] + oh) * 2.0 * np.pi * fh, dch) + 0.5) * hmax)
    # plt.tight_layout()
    
    # create pixel clock
    #x = np.linspace(-2e-5, 5e-5, 100000)
    pixclk = scipy.signal.square(time * 2.0 * np.pi * 6e6) * 2 + 2
    vsync = scipy.signal.square(time * 2.0 * np.pi * 50) * 2 + 2
    hsync = scipy.signal.square((time + oh) * 2.0 * np.pi * fh, dch) * 0.5 + 0.5
    
    fig, ax = plt.subplots(4,1,dpi=144, figsize=(12,4))
    
    ax[0].plot(time, ch1, linewidth=0.5)
    ax[0].set_ylim(0,1)
    ax[0].set_xlim(-0.0040, 0.0175)
    
    ax[1].plot(time, ch1, linewidth=0.5)
    ax[1].plot(time, ch2, linewidth=0.5, alpha=0.5)
    ax[1].plot(time, hsync, linewidth=0.5, alpha=0.5)
    ax[1].set_xlim(-0.001, 0.001)
    ax[1].set_ylim(0,1)
    
    ax[2].plot(time, ch1, linewidth=0.5)
    ax[2].plot(time, ch2, linewidth=0.5)
    ax[2].fill_between(time, 0, hsync, linewidth=0.5, alpha=0.2)
    ax[2].set_xlim(-2e-5, 5e-5)
    ax[2].set_ylim(0,1)
    
    ax[3].plot(time, ch1, linewidth=0.5, alpha=0.5)
    ax[3].plot(time, ch2, linewidth=0.5, alpha=0.5)
    ax[3].plot(time, pixclk, linewidth=0.5)
    ax[3].plot(time, (pixclk * ch2 > 5) * 4, linewidth=0.5)
    ax[3].set_xlim(0, 2e-5)
    ax[3].set_ylim(0,1)

    plt.tight_layout()

def align_signal(time, signal, f0, o0, dc0):
    
    def opt(x, time, signal):
        """
        Cost function
        """
        f, o, dc, h = x
        y = (0.5 * scipy.signal.square((time + o) * 2.0 * np.pi * f, dc) + 0.5) * h
        return np.sum(np.power(signal - y,2))
    
    res = scipy.optimize.minimize(opt, (f0, o0, dc0, 1.0), args=(time, signal), tol=1e-14)
    print(res)
    
    return res.x

def normalize(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

def get_data():
    time = np.load('time.npy')
    ch1 = np.load('ch1.npy')
    ch2 = np.load('ch2.npy')
    
    # normalize signals
    ch1 = normalize(ch1)
    ch2 = normalize(ch2)
    
    # prune data
    x0 = np.argwhere(time > -0.0040)[0][0]
    x1 = np.argwhere(time > 0.0175)[0][0]
    
    print(time[x0])
    print(time[x1])
    
    print(time[x1] - time[x0])
    
    return time[x0:x1], ch1[x0:x1], ch2[x0:x1]

if __name__ == '__main__':
    main()