# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 13:47:06 2018

THIS HAS BEEN SUPERCEEDED BY viewVectors GIF MAKER~~~ !!!!!!!

@author: 264401k
"""

#%% Timelapse vector viewer
import glob
import pygimli as pg
vecList = glob.glob(r'..\Timelapse2\response_tl_*.vector')

data = pg.load(vecList[0])
mesh = pg.load(r'..\Timelapse2\mesh\meshParaDomain.bms')
