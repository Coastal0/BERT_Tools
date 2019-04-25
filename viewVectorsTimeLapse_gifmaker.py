# -*- coding: utf-8 -*-
#!/usr/bin/env F:\WinPython-64bit-3.6.3.0Qt5\python-3.6.3.amd64\python

import pygimli as pg
import matplotlib.pyplot as plt
import os
import imageio
import numpy as np

def showVec(cmap):
    plt.close('all')
    meshInv = pg.load('mesh\meshParaDomain.bms')
    nameList = []   # Empty vector for gif names.
    # modelAbs.bmat for values
    # modelDiff.bmat for differences
    vectors = pg.load('modelDiff.bmat')
    for vector in enumerate(vectors):
        print(vector[0])
        ax = plt.gca()
        datInv = vector[1]
        print(datInv.size())
        dataplot, _ = pg.show(ax=ax, mesh=meshInv, data=datInv,
                               cmap=cmap, showMesh=0, cMin=0, cMax=100,
                               colorBar=True)
        # Format axes
        ax.set_xlim(left=-10, right=500)
        ax.set_ylim(top=40, bottom=-50)
        ax.minorticks_on()
        ax.set_title(os.getcwd()+' -- '+ str(vector[0]), loc='left')
        ax.set_ylabel('Elevation (mASL)')
        ax.set_xlabel('Distance (m)')
        # Draw boundary lines
        dataplot.plot(dataplot.get_xlim(), [-30, -30], color='black')
        dataplot.plot(dataplot.get_xlim(), [0, 0], color='black')
        # Setup figure
        fig = plt.gcf()
        fig.set_size_inches(19, 5)
        fig.tight_layout()
        plt.ion()
        plt.show()
        plt.pause(0.001)
        # Assign names
        filename = os.path.basename(os.path.normpath(os.getcwd())+'_'+str(vector[0]))
        # Store names for GIF maker
        nameList.append(filename+'.png')
        plt.savefig('{}.png'.format(filename),dpi=150)
        # Clear figure (rather than recreate each time)
        plt.gcf().clear()
    plt.close('all')
    # Make GIF
    images = []
    for i in nameList:
        images.append(imageio.imread(i))
    fTimes=list(np.ones(len(images))*0.2)
    fTimes[0] = 1
    fTimes[-1] = 1
    imageio.mimsave('./test.gif',images, duration=fTimes)

showVec(cmap = 'jet_r')
