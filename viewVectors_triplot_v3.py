# -*- coding: utf-8 -*-
#!/usr/bin/env F:\WinPython-64bit-3.6.3.0Qt5\python-3.6.3.amd64\python
import pygimli as pg
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import os
import glob
import numpy as np
from tkinter import Tk, filedialog

root = Tk()
root.withdraw()
root.focus_force()

def showVec(lastOnly, cmap):
    plt.close('all')
    fig, ax = plt.subplots()
    vector = pg.load('resistivity.vector')
    meshes = glob.glob('**/*.bms', recursive = True)
    for m in meshes:
        if pg.load(m).cellCount() == len(vector):
            meshInv = pg.load(m)
            
#    if meshInv.cellCount() == vector.size():
#        meshInv = pg.load('mesh\\meshPrim.bms')
    coverage = pg.load('coverage.vector')
    print(meshInv)
    print(vector)
    dataplot, cb = pg.show(ax=ax, mesh=meshInv, fitView = True,
               data=vector, cMap=cmap, showMesh=True, 
               cMin = 1, cMax = 1000, colorBar = True, coverage = None)
    showSensors(dataplot)
    # Formatting
    ax.set_xlim(left=-10, right=300)
    ax.set_ylim(top=40, bottom=-50)
    ax.minorticks_on()
    ax.tick_params(which = 'both', direction = 'in')
    ax.xaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(2))
    ax.annotate(os.getcwd(), xy = [0.05,50],  transform=plt.gcf().transFigure, annotation_clip=False)
    ax.set_ylabel('Elevation (mASL)')
    ax.set_xlabel('Distance (m)')
    fig = plt.gcf()
    fig.set_size_inches(12,4)
    fig.tight_layout()
    filename = os.path.basename(os.path.normpath(os.getcwd()))
    i=0
    while os.path.exists('{}{:d}.png'.format(filename, i)):
        i += 1
    plt.savefig('{}_({:d}).png'.format(filename, i), bbox_inches='tight', dpi=600)

def showSensors(ax):
    dataList = glob.glob('*.data')
    if len(dataList) == 1:
        data = pg.load(dataList[0])
    sensors = np.asarray(data.sensors())
    ax.scatter(sensors[:,0],sensors[:,1], s = 5, c = 'k')
#def showErr():
#    import pybert as pb
#    data=pb.pg.load(glob.glob('*.data')[1])
#    resp=pb.pg.RVector("response.vector")
#    misfit=resp/data('rhoa')*100-100
#    fig, ax = plt.subplots()
#    cma = max(pb.pg.abs(misfit)) * 0.5
#    cma = pb.pg.utils.base.inthist(pb.pg.abs(misfit), 97)
#    pb.show(data, vals=misfit, ax=ax, cMin=-cma, cMax=cma, cmap='bwr', logScale=False)

#def showMisfit():
#    inputModel = np.load(r"G:/BERT/data/Constraints/resBulk.npy")
#    inputMesh = pg.load(r"G:\BERT\data\Constraints\meshERT.bms")
#    
#    invertedModel = pg.load()
#    invertedMesh = 
#    pg.show(inputMesh,inputModel)
dirPath = filedialog.askdirectory()
os.chdir(dirPath)
rootDir = os.getcwd()
showVec(lastOnly = 1, cmap = 'jet_r')

# traverse root directory, and list directories as dirs and files as files
#import fnmatch
#for root, dirs, files in os.walk(rootDir):
#    print(dirs)
#    if any(fnmatch.filter(dirs, 'result*')):
#        os.chdir(os.path.join(root, dirs[0]))
#        try:
#            showVec(lastOnly = 1, cmap = 'jet_r')
#        except:
#            print('aaaaa')
#        os.chdir(rootDir)

