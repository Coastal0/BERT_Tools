# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 09:47:24 2018

@author: 264401k
"""

import workbook as w
import os


hull, bPoly = w.loadHull(r"G:/BERT/data/boundsXY.mat")

fList = [r"file:///F:/results/Throughflow/QR_Quad_010mday_mass.dat",
         r"file:///F:/results/Throughflow/QR_Quad_005mday_mass.dat"]
fList2 = [r"file:///F:/results/Throughflow/QR_Quad_010mday_sat.dat",
         r"file:///F:/results/Throughflow/QR_Quad_005mday_sat.dat"]

for n, f in enumerate(fList):
    hull = []
    bPoly = []
    data = []
    coords = []
    bPolyMesh = []
    topoArray = []
    dMesh = []
    dInterp = []
    ertScheme = []
    meshERT = []
    resBulk = []

    hull, bPoly = w.loadHull(r"G:/BERT/data/boundsXY.mat")

    fName = f
    fName2 = fList2[n]
    print(fName, fName2)
    data, coords = w.loadData(fName)
    data2, coords2 = w.loadData(fName2)

    if (coords2 == coords).all():
        data['SINIT'] = data2['SINIT'] # The header for data2 will depend on the datatype exported. adjust as needed
        del data2
    else:
        print('Error: Coordinates do not match')

    bPolyMesh = w.fillPoly(bPoly, coords, hull) # Fill boundary mesh with nodes at coordinates
    w.checkMesh(bPolyMesh) # Check each node has a value. If !0, ERT will not work.
    topoArray = w.getTopo(hull) # Extract the topography from the concave hull
    dMesh = w.makeDataMesh(coords, 0) # Make a mesh with the datapoints (interpolates across topography, hence need for above steps)

    data['dataCol'] = data['MINIT'] * data['SINIT']
    dInterp = w.makeInterpVector(data, dMesh, bPolyMesh) # Add data to the nodes

    ertScheme, meshERT = w.createArray(0, 710, 10, 'dd', topoArray, enlarge = 1)
    invalids = 0
    for i,m in enumerate(ertScheme("m")):
        if m < int(ertScheme("b")[i]):
            invalids = invalids + 1
            ertScheme.markInvalid(int(i))

    for i,n in enumerate(ertScheme("n")):
        if n < int(ertScheme("m")[i]):
            invalids = invalids + 1
            ertScheme.markInvalid(int(i))
    print(invalids)
    ertScheme.save('testests', "a b m n valid")

    resBulk = w.convertFluid(dInterp, bPolyMesh, meshERT)
    dataName = (os.path.basename(fName)[:-9]+'_dd_10m')
    simdata = w.simulate(meshERT, resBulk, ertScheme, dataName)
