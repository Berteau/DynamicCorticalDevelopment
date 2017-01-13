from __future__ import division
import visual
from random import *
from visual import *
from cells import Body, Process, Sensor, switch, X, Y, Z, Soma, Node
from Pyramidal import *
import Basket
from Signals import DiffuseSignalSource, distance, compileSignals
import time

#SVZ
svz=visual.box(pos=vector(0.,-1.,0.), size=(200,1,200),color=[0.5,0.5,0.5])

# Housekeeping, create synapse want ads, cells, and endogenous diffuse signals
wantAds = {}
cells = []
endogenousDiffuseSignals = {}

# Set up chemical layers
# Layer 6
endogenousDiffuseSignals["Layer6"] = []
for x in range(-100, 100, 10):
    for y in range(-100, 100, 10):
        endogenousDiffuseSignals["Layer6"].append(DiffuseSignalSource([x,0,y], radius=50, intensity=50))
# Layer 5
endogenousDiffuseSignals["Layer5"] = []
for x in range(-100, 100, 10):
    for y in range(-100, 100, 10):
        endogenousDiffuseSignals["Layer5"].append(DiffuseSignalSource([x,50,y], radius=50, intensity=50))
# Layer 4
endogenousDiffuseSignals["Layer4"] = []
for x in range(-100, 100, 10):
    for y in range(-100, 100, 10):
        endogenousDiffuseSignals["Layer4"].append(DiffuseSignalSource([x,100,y], radius=50, intensity=50))
# Layer3
endogenousDiffuseSignals["Layer3"] = []
for x in range(-100, 100, 10):
    for y in range(-100, 100, 10):
        endogenousDiffuseSignals["Layer3"].append(DiffuseSignalSource([x,150,y], radius=50, intensity=50))
# Layer 2
endogenousDiffuseSignals["Layer2"] = []
for x in range(-100, 100, 10):
    for y in range(-100, 100, 10):
        endogenousDiffuseSignals["Layer2"].append(DiffuseSignalSource([x,200,y], radius=50, intensity=50))
endogenousDiffuseSignals["Layer1"] = []
for x in range(-100, 100, 10):
    for y in range(-100, 100, 10):
        endogenousDiffuseSignals["Layer1"].append(DiffuseSignalSource([x,250,y], radius=50, intensity=50))

# General vertical orientation
for x in range(-100, 100, 25):
    for y in range(-100, 100, 25):
        endogenousDiffuseSignals["verticalOrientation"] = DiffuseSignalSource([x,500,y], radius=1000, intensity=50)

# Add cells
pyramid = LayerIIIPyramidal(initialPosition=[randint(-10,10),0,randint(-10,10)], sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=wantAds, radius=5, connectingRadius=0, debug=False)
cells.append(pyramid)

startTime = time.time()
basketDone = False
secondPyramid = False
secondBasket = False
# Main Loop
while True:    
    visual.rate(100)
    if time.time() - startTime > 3:
        if not basketDone:
            cells.append(Basket.LayerIIIBasket(initialPosition=[randint(-30,30),0,randint(-30,30)], sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=wantAds, radius=5, connectingRadius=0, debug=False))
            cells.append(Basket.LayerIIIBasket(initialPosition=[randint(-30,30),0,randint(-30,30)], sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=wantAds, radius=5, connectingRadius=0, debug=False))
            cells.append(Basket.LayerIIIBasket(initialPosition=[randint(-30,30),0,randint(-30,30)], sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=wantAds, radius=5, connectingRadius=0, debug=False))
            basketDone = True
    if time.time() - startTime > 12:
        if not secondPyramid :
            cells.append(LayerIIIPyramidal(initialPosition=[randint(-10,10),0,randint(-10,10)], sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=wantAds, radius=5, connectingRadius=0, debug=False))
            cells.append(LayerIIIPyramidal(initialPosition=[randint(-30,30),0,randint(-30,30)], sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=wantAds, radius=5, connectingRadius=0, debug=False))
            secondPyramid = True
#    if time.time() - startTime > 24:
#        if not secondBasket:
#            cells.append(Basket.LayerIIIBasket(initialPosition=[randint(-50,70),0,randint(-70,50)], sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=wantAds, radius=5, connectingRadius=0, debug=False))
#            secondBasket = True

    # Compile diffuse signals from space and cells
    totalDiffuseSignals = {}
    compileSignals(totalDiffuseSignals, endogenousDiffuseSignals)
    for cell in cells:
        totalDiffuseSignals = compileSignals(totalDiffuseSignals, cell.fetchDiffuseSignals())

    # Update all cells
    for cell in cells:
        cell.update(totalDiffuseSignals)
