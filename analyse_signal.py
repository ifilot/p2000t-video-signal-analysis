# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import scipy

def main():
    time = np.load('time.npy')
    ch1 = np.load('ch1.npy')
    ch2 = np.load('ch2.npy')
    
    # create pixel clock
    #x = np.linspace(-2e-5, 5e-5, 100000)
    pixclk = scipy.signal.square(time * 2.0 * np.pi * 6e6) * 2 + 2
    vsync = scipy.signal.square(time * 2.0 * np.pi * 50) * 2 + 2
    hsync = scipy.signal.square((time + 1.45e-5) * 2.0 * np.pi * 15625, 0.93) * 2 + 2
    
    fig, ax = plt.subplots(3,1,dpi=144, figsize=(12,4))
    
    ax[0].plot(time, ch1, linewidth=0.5)
    ax[0].plot(time, ch2, linewidth=0.5, alpha=0.5)
    ax[0].plot(time, hsync, linewidth=0.5, alpha=0.5)
    ax[0].set_xlim(-0.001, 0.001)
    ax[0].set_ylim(0,5)
    
    ax[1].plot(time, ch1, linewidth=0.5)
    ax[1].plot(time, ch2, linewidth=0.5)
    ax[1].fill_between(time, 0, hsync, linewidth=0.5, alpha=0.2)
    ax[1].set_xlim(-2e-5, 5e-5)
    ax[1].set_ylim(0,5)
    
    ax[2].plot(time, ch1, linewidth=0.5, alpha=0.5)
    ax[2].plot(time, ch2, linewidth=0.5, alpha=0.5)
    ax[2].plot(time, pixclk, linewidth=0.5)
    ax[2].plot(time, (pixclk * ch2 > 5) * 4, linewidth=0.5)
    ax[2].set_xlim(0, 2e-5)
    ax[2].set_ylim(0,5)

    plt.tight_layout()

if __name__ == '__main__':
    main()