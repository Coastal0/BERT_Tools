# -*- coding: utf-8 -*-
#!/usr/bin/env F:\WinPython-64bit-3.6.3.0Qt5\python-3.6.3.amd64\python

import pygimli as pg
import matplotlib.pyplot as plt
import glob
import os
import re
import numpy as np
import tkinter


def showVec(lastOnly, cmap):
    plt.close('all')
    meshInv = pg.load('mesh\mesh.bms')
    vectors = glob.glob("model_*.vector")
    # Get the final model vector(e.g. the highest number)
    v = np.zeros(len(vectors))
    for s in enumerate(vectors):
        v[s[0]] = int(re.split(r'[_.]', s[1])[1])
    i0 = vectors[np.where(v == 0)[0][0]]
    i1 = vectors[np.where(v == 1)[0][0]]
    iMax = vectors[np.where(v == v.max())[0][0]]
    if lastOnly == 1:
        vectors = iMax
    else:
        # Get the Initial model, first iteration, and last iteration only
        vectors = [i0, i1, iMax]

    print(meshInv.cellCount())
    if type(vectors) == str:
        ax = plt.gca()
        datInv = pg.load(vectors)
        print(datInv.size())
        dataplot, _ = pg.show(ax=ax, mesh=meshInv, data=np.log10(datInv),
                               cmap='jet_r', showMesh=0, vmin=np.log10(1), vmax=np.log10(1000),
                               colorBar=True, tri=True,shading='gouraud',antialiased=True)
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
        plt.show()
    if type(vectors) == list:
        fig, ax = plt.subplots(len(vectors), 1, sharex='all', sharey='all')
        for vecName in enumerate(vectors):
            print(vecName)
    #        ax = plt.gca()
            datInv = pg.load(vecName[1])
            print(datInv.size())
            dataplot, cb = pg.show(ax=ax[vecName[0]], mesh=meshInv, 
                       data=datInv, cmap=cmap, showMesh=0, 
                       cMin = 1, cMax = 1000, colorBar = True)
            ax[vecName[0]].set_xlim(left=-10, right=500)
            ax[vecName[0]].set_ylim(top=40, bottom=-50)
            ax[vecName[0]].minorticks_on()
            ax[vecName[0]].set_title(os.getcwd()+' -- '+vecName[1], loc=  'left')
            ax[vecName[0]].set_ylabel('Elevation (mASL)')
            ax[vecName[0]].set_xlabel('Distance (m)')
            dataplot.plot(dataplot.get_xlim(), [-30,-30], color = 'black')
            dataplot.plot(dataplot.get_xlim(), [0,0], color = 'black')
        fig = plt.gcf()
        fig.set_size_inches(15,11)
        fig.tight_layout()
    meshInv.cellCount() == datInv.size()
    filename = os.path.basename(os.path.normpath(os.getcwd()))
    i=0
    while os.path.exists('{}{:d}.png'.format(filename, i)):
        i += 1
    plt.savefig('{}_({:d}).png'.format(filename, i),dpi=600)
    
    
#    plt.savefig('{}{:d}.eps'.format(filename, i),format = 'eps',dpi=500)

#    manager.window.showMaximized()
dirPath = tkinter.filedialog.askdirectory()
os.chdir(dirPath)
showVec(lastOnly = 1, cmap = 'jet_r')
