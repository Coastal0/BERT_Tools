# -*- coding: utf-8 -*-
#!/usr/bin/env F:\WinPython-64bit-3.6.3.0Qt5\python-3.6.3.amd64\python

import pygimli as pg
import matplotlib.pyplot as plt
import glob
import os
import imageio
import numpy as np
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split('(\d+)', text) ]

def showVec(gif, timelapse, cmap):
    plt.close('all')
    nameList = []
    meshInv = pg.load('mesh\meshParaDomain.bms')
    if timelapse == 1:
        vectors = glob.glob("response_tl_*.vector")
    else:
        vectors = glob.glob("model_*.vector")
    vectors.sort(key=natural_keys)
    if gif == 1:
        for vectors in vectors:
            print(vectors)
            ax = plt.gca()
            datInv = pg.load(vectors)
            print(datInv.size())
            dataplot, _ = pg.show(ax=ax, mesh=meshInv, data=datInv,
                                   cmap=cmap, showMesh=0, cMin=1, cMax=1000,
                                   colorBar=True)
            # Formatting
            ax.set_xlim(left=-10, right=500)
            ax.set_ylim(top=40, bottom=-50)
            ax.minorticks_on()
            ax.set_title(os.getcwd()+' -- '+vectors, loc='left')
            ax.set_ylabel('Elevation (mASL)')
            ax.set_xlabel('Distance (m)')
            dataplot.plot(dataplot.get_xlim(), [-30, -30], color='black')
            dataplot.plot(dataplot.get_xlim(), [0, 0], color='black')
            fig = plt.gcf()
            fig.set_size_inches(19, 5)
            fig.tight_layout()
            plt.ion()
            plt.show()
            plt.pause(0.001)
            
            filename = os.path.basename(os.path.normpath(os.getcwd())+'_'+vectors)
            nameList.append(filename+'.png')
            plt.savefig('{}.png'.format(filename),dpi=150)
            plt.gcf().clear()
    plt.close('all')
    images = []
    for i in nameList[1:]:
        images.append(imageio.imread(i))
    imageio.mimsave('./test.gif',images)

showVec(gif = 1, timelapse = 1, cmap = 'jet_r')
