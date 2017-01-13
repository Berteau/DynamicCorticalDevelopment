from __future__ import division
import cells
import Signals
from math import pi
from random import *
from visual import *
from CellFunctions import X,Y,Z
from pylab import *
'''
Created on Apr 24, 2010

@author: stefan
'''

# Define Basket utility functions, to be called from the soma, the dendrites, axon, cones, branches, and synapses

def generateBasalDendrite(component, relativeOrientation):
   # Generate the tip
   tipPosition = array(component.position) + array(relativeOrientation)
   basalTip = cells.Node(initialPosition=tipPosition, sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=component.wantAds, radius=1.1, connectingRadius=0, color=[0.0,0.0,0.8], debug=False)    
   
   # Generate the switches
   # A chance of branching after a distance, and slowing down over time
   for i in range(randint(0,2)):
       basalTip.addSwitch("oneTimeBranch", cells.switch(min=-4, max=1, decay=0.3, rest=1.0, current=randint(-2,1)), switchFunction=cells.Node.oneTimeBranch)
   #Fade growth by distance from body
   basalTip.addSwitch("advancement", cells.switch(min=0, max=5, decay=0.15, rest=0.0, current=2.0), switchFunction=cells.Node.advance)       
   tempProcess = component.sproutProcess(relativeOrientation, basalTip)
   
def generateDescendingDendrite(component, relativeOrientation):
       # Generate the tip
       tipPosition = array(component.position) + array(relativeOrientation)
       apicalTip = cells.Node(initialPosition=tipPosition, sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=component.wantAds, radius=1.4, connectingRadius=10, color=component.color, debug=False)    
       # Horizontal Orientation Sensor
       apicalTip.addSensor(cells.Sensor(apicalTip, ["Layer6"],  targets={"advancement":-2.0}, gradient=False, threshold = 1.0))    
       # Generate the switches
       # A chance of branching after a distance
       apicalTip.addSwitch("oneTimeBranch", cells.switch(min=-10, max=randint(-4,1), decay=0.1, rest=1.0, current=randint(-9,-6)), switchFunction=cells.Node.oneTimeBranch)
       # Stop when we hit layer 6
       apicalTip.addSwitch("advancement", cells.switch(min=0, max=5, decay=3, rest=5.0, current=0.0), switchFunction=cells.Node.advance)       
       tempProcess = component.sproutProcess(relativeOrientation, apicalTip)

def generateAxon(component, relativeOrientation):
        growthConePosition = array(component.position) + array(relativeOrientation)
        growthCone = cells.Node(initialPosition=growthConePosition, sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=component.wantAds, radius=1.4, connectingRadius=10, color=[0,0.7,1.0], debug=False)    
        # Sensors
        growthCone.addSensor(cells.Sensor(growthCone, ["horizontalOrientation"],  targets={"advancement":10.0}, gradient=False, threshold = 0))
        growthCone.addSensor(cells.Sensor(growthCone, ["horizontalOrientation"],  targets={"chemotaxisX":20.0}, gradient=True, axis=X, threshold = 0))
        growthCone.addSensor(cells.Sensor(growthCone, ["horizontalOrientation"],  targets={"chemotaxisY":20.0}, gradient=True, axis=Y, threshold = 0))
        growthCone.addSensor(cells.Sensor(growthCone, ["horizontalOrientation"],  targets={"chemotaxisZ":20.0}, gradient=True, axis=Z, threshold = 0))
        growthCone.addSensor(cells.Sensor(growthCone, ["BDNF"],  targets={"chemotaxisX":30.0}, gradient=True, axis=X, threshold = 0.01))
        growthCone.addSensor(cells.Sensor(growthCone, ["BDNF"],  targets={"chemotaxisY":30.0}, gradient=True, axis=Y, threshold = 0.01))
        growthCone.addSensor(cells.Sensor(growthCone, ["BDNF"],  targets={"chemotaxisZ":30.0}, gradient=True, axis=Z, threshold = 0.01))
        growthCone.addSensor(cells.Sensor(growthCone, ["BDNF"],  targets={"advancement":15.0}, gradient=False, threshold = 0.01))
        growthCone.addSensor(cells.Sensor(growthCone, ["BDNF"],  targets={"Pyramid":80.0}, gradient=False, threshold = 0.01))
        growthCone.addSensor(cells.Sensor(growthCone, ["horizontalOrientation"],  targets={"Pyramid":40.0}, gradient=False, threshold = 0))
        # Switches
        growthCone.addSwitch("oneTimeBranch", cells.switch(min=-2, max=100, decay=0.2, rest=100.0, current=100), switchFunction=cells.Node.oneTimeBranch)
        growthCone.addSwitch("oneTimeBranch", cells.switch(min=-8, max=1, decay=0.2, rest=1.0, current=randint(-2,-1)), switchFunction=cells.Node.oneTimeBranch)
        growthCone.addSwitch("advancement", cells.switch(min=0, max=6, decay=3, rest=3.0, current=6.0), switchFunction=cells.Node.advance)       
        growthCone.addSwitch("chemotaxisX", cells.switch(min=-8, max=8, decay=0.6, rest=0.0, current=0.0), switchFunction=cells.Body.propulsionX)
        growthCone.addSwitch("chemotaxisY", cells.switch(min=-8, max=8, decay=0.6, rest=0.0, current=0.0), switchFunction=cells.Body.propulsionY)
        growthCone.addSwitch("chemotaxisZ", cells.switch(min=-8, max=8, decay=0.6, rest=0.0, current=0.0), switchFunction=cells.Body.propulsionZ)
        growthCone.addSwitch("Pyramid", cells.switch(min=0, max=90, decay=0.5, rest=0.0, current=0.0), switchFunction = cells.Node.synapseFormation)
        tempProcess = component.sproutProcess(relativeOrientation, growthCone)
#        tempProcess.target.oneTimeBranch()

class LayerIIIBasket(cells.Soma):
    def __init__(self, initialPosition, sensors, switches, surfaceSignals, diffuseSignals, switchFunctions, wantAds, radius=10, connectingRadius=0, color=[0.0,0.0,0.8], debug=False, axonNow=False):
        cells.Soma.__init__(self, initialPosition, sensors, switches, surfaceSignals, diffuseSignals, switchFunctions, wantAds, radius, connectingRadius, color, debug)
        self.axonNow = axonNow
        # Sensors
        self.addSensor(cells.Sensor(self, ["verticalOrientation"],  targets={"chemotaxisY":15.0}, gradient=True, axis=Y, threshold = 0.0))    
        if axonNow:
            self.addSensor(cells.Sensor(self, ["Layer6"],  targets={"chemotaxisY":-10.0, "triggerDendrites":10.0}, gradient=False, threshold = randint(0,3)))
        else:
            self.addSensor(cells.Sensor(self, ["Layer3"],  targets={"chemotaxisY":-40.0, "triggerDendrites":10.0}, gradient=False, threshold = randint(0,3)))

        # Switches
        self.addSwitch("triggerDendrites", cells.switch(min=0, max=11, decay=0.0, rest=0.0, current=0.0), switchFunction=self.triggerDendrites)
        self.addSwitch("sproutBasals", cells.switch(min=0, max=8, decay=0.0, rest=0.0, current=0.0), switchFunction=self.sproutBasals)
        self.addSwitch("chemotaxisY", cells.switch(min=0, max=14, decay=0.3, rest=4.0, current=0.0), switchFunction=cells.Body.propulsionY)
#        self.addSwitch("sproutAxon", cells.switch(min=0, max=200, decay=0.1, rest=0.0, current=200.0), switchFunction=sproutBasals))
        self.addSurfaceSignal("Basket")
        self.diffuseSignals["ExcitatoryAttractor"] = Signals.DiffuseSignalSource(self.position, radius=50, intensity=20, tiedTo=self)
        
    def triggerDendrites(self, component, switch):
        if switch.current  > 10:
            self.switches["sproutBasals"].current = 8
            self.sproutDescending()
            self.sproutAxon()
            for key in self.switches.keys():
                if self.switches[key] == switch:
                    del self.switches[key]
        
    def sproutBasals(self, component, switch):
        if randint(0,100) < switch.current:
            switch.current -= 1
            offset = (self.radius)*rotate(vector(1,(random() - 0.7),0), ((2*pi/8) * switch.current)+random()-0.5, vector(0,1,0))
#            print "Sprouting basal dendrite at offset:", offset
            generateBasalDendrite(self, offset)

    def sproutDescending(self):
        offset = (self.radius) * vector(uniform(-0.05, 0.1),uniform(-0.9, -1.0),uniform(-0.1, 0.05))
#        print "Sprouting descending dendrite at offset:", offset
        generateDescendingDendrite(self, offset)
        
    def sproutAxon(self):
        offset = (self.radius) * vector(uniform(-0.05, 0.1),uniform(0.9, 1.0),uniform(-0.1, 0.05))
#        print "Sprouting axon at offset:", offset
        generateAxon(self, offset)
