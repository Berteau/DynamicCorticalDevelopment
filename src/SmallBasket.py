from __future__ import division
import cells
import Signals
from math import pi
from random import *
from visual import *
from cells import X,Y,Z
from pylab import *
'''
Created on Apr 24, 2010

@author: stefan
'''

# Define Basket utility functions, to be called from the soma, the dendrites, axon, cones, branches, and synapses

def generateDendrites(component, relativeOrientation):
   # Generate the tip
   tipPosition = array(component.position) + array(relativeOrientation)
   basalTip = cells.Node(initialPosition=tipPosition, sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=component.wantAds, radius=1.1, connectingRadius=0, color=[0.7,0.0,0.0], debug=False)    
   
   # Generate the switches
   # A chance of branching after a distance, and slowing down over time
   for i in range(randint(0,2)):
       basalTip.addSwitch("oneTimeBranch", cells.switch(min=-1000, max=1, decay=0.1, rest=1.0, current=randint(-3,1)), switchFunction=cells.Node.oneTimeBranch)
   #Fade growth by distance from body
   basalTip.addSwitch("advancement", cells.switch(min=0, max=2, decay=0.1, rest=0.0, current=0.0), switchFunction=cells.Node.advance)       
   tempProcess = component.sproutProcess(relativeOrientation, basalTip)
   tempProcess.debug = True
   
def generateApicalDendrite(component, relativeOrientation):
   # Generate the tip
   tipPosition = array(component.position) + array(relativeOrientation)
   apicalTip = cells.Node(initialPosition=tipPosition, sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=component.wantAds, radius=1.4, connectingRadius=10, color=component.color, debug=False)    
   # Horizontal Orientation Sensor
   apicalTip.addSensor(cells.Sensor(apicalTip, ["Layer2"],  targets={"advancement":-2.0, "branchAtTheTop":10}, gradient=False, threshold = 1.0))    

   # Generate the switches
   # A chance of branching after a distance
   apicalTip.addSwitch("oneTimeBranch", cells.switch(min=-10, max=randint(-4,1), decay=0.1, rest=1.0, current=randint(-8,-4)), switchFunction=cells.Node.oneTimeBranch)
   # Stop when we hit layer 2
   apicalTip.addSwitch("advancement", cells.switch(min=0, max=4, decay=3, rest=4.0, current=0.0), switchFunction=cells.Node.advance)       
   apicalTip.addSwitch("branchAtTheTop", cells.switch(min=-3, max=2, decay=3, rest=-3.0, current=-30.0), switchFunction=cells.Node.oneTimeBranch)       
   tempProcess = component.sproutProcess(relativeOrientation, apicalTip)
   tempProcess.debug = True

class LayerIIIBasket(cells.Soma):
    def __init__(self, initialPosition, sensors, switches, surfaceSignals, diffuseSignals, switchFunctions, wantAds, radius=10, connectingRadius=0, color=[0.0,0.0,0.8], debug=False):
        cells.Soma.__init__(self, initialPosition, sensors, switches, surfaceSignals, diffuseSignals, switchFunctions, wantAds, radius, connectingRadius, color, debug)
        # Sensors
        self.addSensor(cells.Sensor(self, ["verticalOrientation"],  targets={"chemotaxisY":15.0}, gradient=True, axis=Y, threshold = 0.0))    
        self.addSensor(cells.Sensor(self, ["Layer3"],  targets={"chemotaxisY":-30.0, "triggerDendrites":10.0}, gradient=False, threshold = randint(2,10)))

        # Switches
        self.addSwitch("triggerDendrites", cells.switch(min=0, max=11, decay=0.0, rest=0.0, current=0.0), switchFunction=self.triggerDendrites)
        self.addSwitch("sproutBasal", cells.switch(min=0, max=8, decay=0.0, rest=0.0, current=0.0), switchFunction=self.sproutBasals)
        self.addSwitch("chemotaxisY", cells.switch(min=0, max=8, decay=0.6, rest=4.0, current=0.0), switchFunction=cells.Body.propulsionY)
#        self.addSwitch("sproutAxon", cells.switch(min=0, max=200, decay=0.1, rest=0.0, current=200.0), switchFunction=sproutBasals))
        
    def triggerDendrites(self, component, switch):
        if switch.current  > 10:
            
            self.sproutDescending()
            self.sproutAxon()
            for key in self.switches.keys():
                if self.switches[key] == switch:
                    del self.switches[key]
        
    def sproutBasals(self, component, switch):
        if randint(0,100) < switch.current:
            switch.current -= 1
            offset = (self.radius)*rotate(vector(1,(random() - 0.7),0), ((2*pi/8) * switch.current)+random()-0.5, vector(0,1,0))
            print "Sprouting basal dendrite at offset:", offset
            generateBasalDendrite(self, offset)

    def sproutApical(self):
        offset = (self.radius) * vector(uniform(-0.05, 0.1),uniform(0.9, 1.0),uniform(-0.1, 0.05))
        print "Sprouting apical dendrite at offset:", offset
        generateApicalDendrite(self, offset)
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

#    # Attempt to place the tip relative to the vertical orientation
#    if "verticalOrientation" in component.diffuseSignals.keys():
#        signalStrength = sum([source.sampleAtLocation(component.position) for source in component.diffuseSignals["verticalOrientation"]])
#        gradientStrength = sum([source.sampleAtLocation(list(array(component.position)+ array(component.axis))) for source in component.diffuseSignals["verticalOrientation"]]) - signalStrength    
#        tipPosition = [random.randint(-, high=None, size=None)]