from __future__ import division
import cells
from cells import X,Y,Z
from pylab import *
'''
Created on Apr 24, 2010

@author: stefan
'''

# Define pyramidal utility functions, to be called from the soma, the dendrites, axon, cones, branches, and synapses

def generateBasalDendrite(component):
    # Attempt to place the tip relative to the vertical orientation
    if "verticalOrientation" in component.diffuseSignals.keys():
        signalStrength = sum([source.sampleAtLocation(component.position) for source in component.diffuseSignals["verticalOrientation"]])
        gradientStrength = sum([source.sampleAtLocation(list(array(component.position)+ array(component.axis))) for source in component.diffuseSignals["verticalOrientation"]]) - signalStrength
        print gradientStrength
    
   # Generate the tip
    basalTip = cells.Node(initialPosition=component.position, sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=component.wantAds, radius=1, connectingRadius=10, debug=False)

    
    # Generate the sensors
    
    # Generate the switches
    # A chance of branching after a distance
    basalTip.addSwitch("oneTimeBranch", cells.switch(min=-1000, max=4, decay=0.1, rest=-1000.0, current=0.0), switchFunction=cells.Node.oneTimeBranch)
    
    component.switches["growToSupportProcess"].current = 10

#    
#def fadeChemotaxisY(component, switch):
#    switch.current / 100
#
#def growToSupportProcess(component):
#    
#def generateApicalDendrite(component):
#    
#
#def secreteHorizontalOrientingSignal(component, switch):
#    
#def sproutBasals(component, switch):
#    if switch == 0.0:
#        
#        self.
#    
#def stopDendrites(component, switch):
#        
#def sproutApicalDendrite
#    
#
#
#class LayerIIIPyramidal(cells.Soma):
#    def __init__(self, initialPosition, sensors, switches, surfaceSignals, diffuseSignals, switchFunctions, wantAds, radius=10, connectingRadius=0, color=[1,1,1], debug=False):
#        cells.Soma.__init__(self, initialPosition, sensors, switches, surfaceSignals, diffuseSignals, switchFunctions, wantAds, radius, connectingRadius, color, debug)
#        self.addSwitch("horizontalOrienting", cells.switch(min=0, max=200, decay=0.3, rest=0.0, current=0.0), switchFunction=secreteHorizontalOrientingSignal)
#        self.addSwitch("sproutBasals", cells.switch(min=0, max=200, decay=0.1, rest=0.0, current=200.0), switchFunction=sproutBasals)
#
#
#
## Create Soma
#pyramid = Soma(initialPosition=[0,0,0], sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=wantAds, radius=5, connectingRadius=0, debug=True)
#
## Add switches
#
## Add sensors
#targetCell.addSensor(Sensor(targetCell, ["targetAttractor"],  targets={"chemotaxisX":15.0}, gradient=True, axis=X, threshold = 0.01))
#targetCell.addSensor(Sensor(targetCell, ["targetAttractor"],  targets={"chemotaxisY":15.0}, gradient=True, axis=Y, threshold = 0.01))
#targetCell.addSensor(Sensor(targetCell, ["targetAttractor"],  targets={"chemotaxisZ":15.0}, gradient=True, axis=Z, threshold = 0.01))
#targetCell.addSensor(Sensor(targetCell, ["targetAttractor"], targets={"expressStageTwoSensors":10.0}, gradient=False, threshold = 10.0))
#targetCell.addDiffuseSignal("Attractor", DiffuseSignalSource([60,20,20], 1000, 50, tiedTo=targetCell))
#targetCell.addSurfaceSignal("postSynaptic")
## Add switches
#targetCell.addSwitch("chemotaxisX", switch(min=-2, max=2, decay=0.6, rest=0.0, current=0.0), switchFunction=Body.propulsionX)
#targetCell.addSwitch("chemotaxisY", switch(min=-2, max=2, decay=0.6, rest=0.0, current=0.0), switchFunction=Body.propulsionY)
#targetCell.addSwitch("chemotaxisZ", switch(min=-2, max=2, decay=0.6, rest=0.0, current=0.0), switchFunction=Body.propulsionZ)
