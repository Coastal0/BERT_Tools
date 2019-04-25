# -*- coding: utf-8 -*-
"""Simplistic version a complete ERT Modelling->Inversion example."""

import pygimli as pg
import pygimli.meshtools as plc  # save space
import pybert as pb
import numpy as np
import itertools

def abmn(n):
    """
    Construct all possible four-point configurations for a given
    number of sensors after Noel and Xu (1991).
    """
    combs = np.array(list(itertools.combinations(list(range(1, n+1)), 4)))
    perms = np.empty((int(n*(n-3)*(n-2)*(n-1)/8), 4), 'int')
    print(("Comprehensive data set: %d configurations." % len(perms)))
    for i in range(np.size(combs, 0)):
        perms[0+i*3, :] = combs[i,:] # ABMN
        perms[1+i*3, :] = (combs[i, 0], combs[i, 2], combs[i, 3], combs[i, 1]) #AMNB
        perms[2+i*3, :] = (combs[i, 0], combs[i, 2], combs[i, 1], combs[i, 3]) #AMBN

    return perms - 1

# Create geometry definition for the modelling domain.
# worldMarker=True indicates the default boundary conditions for the ERT
world = plc.createWorld(start=[-10, 0], end=[60, -30],
                        layers=[-1, -5], worldMarker=True)

# Create some heterogeneous circular
block = plc.createCircle(pos=[25, -3.], radius=1, marker=4,
                         boundaryMarker=10, area=0.1)

# Merge geometry definition into a Piecewise Linear Complex (PLC)
geom = plc.mergePLC([world, block])

# Optional: show the geometry
pg.show(geom,boundaryMarker=True)

# Create a Dipole Dipole ('dd') measuring scheme with 21 electrodes.
# Create empty DataContainer
data = pb.DataContainerERT() 

# Add electrodes
n = 26
spacing = 2
for i in range(n):
    data.createSensor([i * spacing, 0.0]) # 2D, no topography

# Add configurations
cfgs = abmn(n) # create all possible 4P cgfs for 16 electrodes
for i, cfg in enumerate(cfgs):
    data.createFourPointData(i, *map(int, cfg)) # (We have to look into this: Mapping of int necessary since he doesn't like np.int64?)

scheme = data
scheme = pb.createData(elecs=pg.utils.grange(start=-0, end=50, n=26), schemeName='dd')

# Put all electrodes (aka. sensors positions) into the PLC to enforce mesh
# refinement. Due to experience known, its convenient to add further refinement
# nodes in a distance of 10% of electrode spacing, to achieve sufficient
# numerical accuracy.
for pos in scheme.sensorPositions():
    print(pos)
    geom.createNode(pos)
    geom.createNode(pos+pg.RVector3(0, -0.1))

# Create a mesh for the finite element modelling with appropriate mesh quality.
mesh = plc.createMesh(geom, quality=34)

# Optional: take a look at the mesh
pg.show(mesh,boundaryMarker=True)

# Create a map to set resistivity values in the appropriate regions
# [[regionNumber, resistivity], [regionNumber, resistivity], [...]
rhomap = [[1, 100.],
          [2, 50.],
          [3, 1000.],
          [4, 1.]]
#%%
# Initialize the ERTManager (The class name is a subject to further change!)
ert = pb.ERTManager()

# Perform the modeling with the mesh and the measuring scheme itself
# and return a data container with apparent resistivity values,
# geometric factors and estimated data errors specified by the noise setting.
# The noise is also added to the data.
data = ert.simulate(mesh, res=rhomap, scheme=scheme, noiseLevel=2, noiseAbs=1e-6)

# Optional: you can filter all values and tokens in the data container.
print('Simulated rhoa', data('rhoa'), max(data('rhoa')))
data.markInvalid(data('rhoa') < 0)
print('Filtered rhoa', data('rhoa'), max(data('rhoa')))
data.removeInvalid()

# Optional: save the data for further use
data.save('simple.dat')

# Optional: take a look at the data
pb.show(data)

pg.wait()
#%%
# Run the ERTManager to invert the modeled data.
# The necessary inversion mesh is generated automatic.
model = ert.invert(data, paraDX=0.3, maxCellArea=0.2, lam=30, verbose = 1)

# Let the ERTManger show you the model and fitting results of the last
# successful run.
ert.showResultAndFit()
