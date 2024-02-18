# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import scipy

def main():
    
    data = np.load('p2000t_video.npy')
    print(data.shape)
    
    # create pixel clock
    #x = np.linspace(-2e-5, 5e-5, 100000)
    pixclk = scipy.signal.square(data[:,0] * 2.0 * np.pi * 6e6) * 2 + 2
    vsync = scipy.signal.square(data[:,0] * 2.0 * np.pi * 50) * 2 + 2
    hsync = scipy.signal.square((data[:,0] + 1.45e-5) * 2.0 * np.pi * 15625, 0.93) * 2 + 2
    
    fig, ax = plt.subplots(3,1,dpi=144, figsize=(12,4))
    
    ax[0].plot(data[:,0], data[:,1], linewidth=0.5)
    ax[0].plot(data[:,0], data[:,2], linewidth=0.5, alpha=0.5)
    ax[0].plot(data[:,0], hsync, linewidth=0.5, alpha=0.5)
    ax[0].set_xlim(-0.001, 0.001)
    ax[0].set_ylim(0,5)
    
    ax[1].plot(data[:,0], data[:,1], linewidth=0.5)
    ax[1].plot(data[:,0], data[:,2], linewidth=0.5)
    ax[1].fill_between(data[:,0], 0, hsync, linewidth=0.5, alpha=0.2)
    ax[1].set_xlim(-2e-5, 5e-5)
    ax[1].set_ylim(0,5)
    
    x1=1775000
    x2=1793000
    ax[2].plot(data[x1:x2,0], data[x1:x2,1], linewidth=0.5, alpha=0.5)
    ax[2].plot(data[x1:x2,0], data[x1:x2,2], linewidth=0.5, alpha=0.5)

    ax[2].plot(data[:,0], pixclk, linewidth=0.5)
    ax[2].plot(data[:,0], (pixclk * data[:,2] > 5) * 4, linewidth=0.5)
    ax[2].set_xlim(0, 2e-5)
    ax[2].set_ylim(0,5)

    plt.tight_layout()

if __name__ == '__main__':
    main()