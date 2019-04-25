# -*- coding: utf-8 -*-

## Make Config Files for many data files.
# Will copy a global config file (in cwd) and apply it to all subdirectories with a *.ohm datafile.

import os
import shutil
from tkinter import Tk, filedialog

spacings = ['2.5m','5m','10m','25m','50m']
inflows = ['3MLpy','1MLpy']
arrays = ['gr','dd','wa']
arrays = [s + '.ohm' for s in arrays]

iFace = 'interface_seabed_short.xz'
pMesh = 'mesh_regions.bms'
regionFile = 'regions_PLC.control'
paraGeometry = 'plc_region.poly'

dirPath = filedialog.askdirectory()
os.chdir(dirPath)
#for dirpath, dirnames, filenames in os.walk(dirPath):
#    for f in filenames:
#        if f.endswith('.ohm'):
#            fSplit = f.split('_')
#            array = [i for i in arrays if i in fSplit][0][:-4]
#            spacing = [i for i in spacings if i in fSplit]
##            inflow = [i for i in inflows if i in fSplit][0]
#            directory = dirpath+'\{}\{}'.format(array,spacing)
#            if not os.path.exists(directory):
#                os.makedirs(directory)
#            shutil.copy(f, directory)
#            shutil.copy(paraGeometry, directory)
#
#            with open(directory+"\config_{}_{}_unconstrained.cfg".format(array,spacing), "w") as config:
#                config.write('DATAFILE={} \n'.format(f))
#                config.write('DIMENSION=2 \n')
#                config.write('TOPOGRAPHY=1 \n')
#                config.write('SURFACESMOOTH=1 \n')
#                config.write('PARADX=0.1 \n')
#                config.write('SPLINEBOUNDARY=1 \n')
#                config.write('PARA2DQUALITY=33.8 \n')
#                config.write('PARAMAXCELLSIZE=20 \n')
#                config.write('RECALCJACOBIAN=1 \n')
#                config.write('#PARAGEOMETRY={} \n'.format(paraGeometry))
#                config.write('####### Constraint Options ####### \n')
#                config.write('#INTERFACE={} \n'.format(iFace))
#                config.write('#PARAMESH={} \n'.format(pMesh))
#                config.write('#REGIONFILE={} \n'.format(regionFile))
filenames = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('ohm')]
for f in filenames:
    fSplit = f.split('_')
    array = [i for i in arrays if i in fSplit][0][:-4]
    spacing = [i for i in spacings if i in fSplit][0]
#            inflow = [i for i in inflows if i in fSplit][0]
    directory = dirPath+'\{}\{}'.format(array,spacing)
    if not os.path.exists(directory):
        os.makedirs(directory)
    shutil.copy(f, directory)
    shutil.copy(paraGeometry, directory)

    with open(directory+"\config_{}_{}_unconstrained.cfg".format(array,spacing), "w") as config:
        config.write('DATAFILE={} \n'.format(f))
        config.write('DIMENSION=2 \n')
        config.write('TOPOGRAPHY=1 \n')
        config.write('SURFACESMOOTH=1 \n')
        config.write('PARADX=0.1 \n')
        config.write('SPLINEBOUNDARY=1 \n')
        config.write('PARA2DQUALITY=33.8 \n')
        config.write('PARAMAXCELLSIZE=20 \n')
        config.write('RECALCJACOBIAN=1 \n')
        config.write('#PARAGEOMETRY={} \n'.format(paraGeometry))
        config.write('####### Constraint Options ####### \n')
        config.write('#INTERFACE={} \n'.format(iFace))
        config.write('#PARAMESH={} \n'.format(pMesh))
        config.write('#REGIONFILE={} \n'.format(regionFile))