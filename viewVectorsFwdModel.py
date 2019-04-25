# -*- coding: utf-8 -*-
#!/usr/bin/env F:\WinPython-64bit-3.6.3.0Qt5\python-3.6.3.amd64\python

import pygimli as pg
import matplotlib.pyplot as plt
import glob
import os
import re
import numpy as np


def showVec(lastOnly, cmap):
    plt.close('all')
    
    fwdPath = r'G:\BERT\data\New folder'
    fwdMeshN = fwdPath+'\meshERT_025mday.bms'
    fwdMesh= pg.load(fwdMeshN)
    fwdDataN = fwdPath+'\\resbulk_025mday_dd.vector'
    fwdData = pg.load(fwdDataN)
    ax = plt.gca()

    dataplot, _ = pg.show(ax=ax, mesh=fwdMesh, data=fwdData,
                           cmap=cmap, showMesh=0, cMin=1, cMax=1000,
                           colorBar=True)
    # Formatting
    ax.set_xlim(left=-10, right=500)
    ax.set_ylim(top=40, bottom=-50)
    ax.minorticks_on()
    ax.set_title(os.getcwd()+' -- '+fwdDataN, loc='left')
    ax.set_ylabel('Elevation (mASL)')
    ax.set_xlabel('Distance (m)')
    dataplot.plot(dataplot.get_xlim(), [-30, -30], color='black')
    dataplot.plot(dataplot.get_xlim(), [0, 0], color='black')
    fig = plt.gcf()
    fig.set_size_inches(19, 5)
    fig.tight_layout()
    plt.show()

    filename = os.path.basename(os.path.normpath(os.getcwd()))

    plt.savefig('{}.png'.format(filename),dpi=150)
    
showVec(lastOnly = 1, cmap = 'jet_r')
