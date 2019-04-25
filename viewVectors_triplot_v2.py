# -*- coding: utf-8 -*-
#!/usr/bin/env F:\WinPython-64bit-3.6.3.0Qt5\python-3.6.3.amd64\python

import pygimli as pg
import matplotlib.pyplot as plt
import glob
import os
import re
import numpy as np
import fnmatch
from tkinter import Tk, filedialog

def showVec(lastOnly, cmap):
    plt.close('all')
    for m in glob.glob("**/*.bms",  recursive=True):
        if any(fnmatch.filter(m, 'result*')):
            None
        else:
            vectors = glob.glob("model_*.vector")
            print(m)
            m_ = pg.load(m)
            m__ = m_.cellCount()
            if m__ == len(pg.load(vectors[0])):
                meshInv = m_
                print(m_)
                break
    # Get the final model vector(e.g. the highest number)
    v = np.zeros(len(vectors))
    for s in enumerate(vectors):
        v[s[0]] = int(re.split(r'[_.]', s[1])[1])
    i0 = vectors[np.where(v == 0)[0][0]]
    i1 = vectors[np.where(v == 1)[0][0]]
    iMax = vectors[np.where(v == v.max())[0][0]]
    if lastOnly == 1:
        vectors = [iMax]
    else:
        # Get the Initial model, first iteration, and last iteration only
        vectors = [i0, i1, iMax]

    if type(vectors) == list:
        fig, ax = plt.subplots(len(vectors), 1, sharex='all', sharey='all', squeeze = False)
        for n, vecName in enumerate(vectors):
            print(vecName)
#            ax = plt.gca()
            datInv = pg.load(vecName)
            print(datInv.size())
            dataplot, cb = pg.show(ax=ax[0][n], mesh=meshInv, fitView = True,
                       data=datInv, cMap=cmap, showMesh=True, 
                       cMin = 1, cMax = 1000, colorBar = True)
            ax[0][n].set_xlim(left=-50, right=500)
            ax[0][n].set_ylim(top=40, bottom=-50)
            ax[0][n].minorticks_on()
            ax[0][n].set_title(os.getcwd()+' -- '+vecName[1], loc=  'left')
            ax[0][n].set_ylabel('Elevation (mASL)')
            ax[0][n].set_xlabel('Distance (m)')
#            dataplot.plot(dataplot.get_xlim(), [-30,-30], color = 'black')
#            dataplot.plot(dataplot.get_xlim(), [0,0], color = 'black')
        fig = plt.gcf()
        fig.set_size_inches(15,3*len(vectors)+1)
        fig.tight_layout()
    meshInv.cellCount() == datInv.size()
    filename = os.path.basename(os.path.normpath(os.getcwd()))
    i=0
    while os.path.exists('{}{:d}.png'.format(filename, i)):
        i += 1
    plt.savefig('{}_({:d}).png'.format(filename, i),dpi=600)
    
    
#    plt.savefig('{}{:d}.eps'.format(filename, i),format = 'eps',dpi=500)

#    manager.window.showMaximized()
dirPath = filedialog.askdirectory()
os.chdir(dirPath)
showVec(lastOnly = 1, cmap = 'jet_r')
