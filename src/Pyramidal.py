from __future__ import division
import cells
import Signals
from math import pi
from random import *
from visual import *
from CellFunctions import X,Y,Z
from pylab import *

# Define pyramidal utility functions, to be called from the soma, the dendrites, axon, cones, branches, and synapses

def generateBasalDendrite(component, relativeOrientation):
    # Generate the tip
    tipPosition = array(component.position) + array(relativeOrientation)
    basalTip = cells.Node(initialPosition=tipPosition, sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=component.wantAds, radius=1.1, connectingRadius=0, color=[0.7,0.0,0.0], debug=False)    
    # Horizontal Orientation Sensor
    basalTip.addSensor(cells.Sensor(basalTip, ["horizontalOrientation"],  targets={"advancement":1.0}, gradient=False, threshold = 23.5))    
    
    # Generate the switches
    # A chance of branching after a distance
    for i in range(randint(1,2)):
        basalTip.addSwitch("oneTimeBranch", cells.switch(min=-10, max=randint(0,3), decay=0.2, rest=1.0, current=randint(-3,0)), switchFunction=cells.Node.oneTimeBranch)
    #Fade growth by distance from body
    basalTip.addSwitch("advancement", cells.switch(min=0, max=2, decay=0.01, rest=0.0, current=0.0), switchFunction=cells.Node.advance)       
    basalTip.addSurfaceSignal("Pyramid")
    tempProcess = component.sproutProcess(relativeOrientation, basalTip, diffuseSignalsOverride=component.childSignals)
   
def generateApicalDendrite(component, relativeOrientation):
    # Generate the tip
    tipPosition = array(component.position) + array(relativeOrientation)
    apicalTip = cells.Node(initialPosition=tipPosition, sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=component.wantAds, radius=1.4, connectingRadius=10, color=component.color, debug=False)    
    # Horizontal Orientation Sensor
    apicalTip.addSensor(cells.Sensor(apicalTip, ["Layer2"],  targets={"advancement":-2.0, "branchAtTheTop":10}, gradient=False, threshold = 1.0))    
    
    # Generate the switches
    # A chance of branching after a distance
    apicalTip.addSwitch("oneTimeBranch", cells.switch(min=-10, max=randint(-4,1), decay=0.1, rest=1.0, current=randint(-8,-5)), switchFunction=cells.Node.oneTimeBranch)
    # Stop when we hit layer 2
    apicalTip.addSwitch("advancement", cells.switch(min=0, max=4, decay=3, rest=4.0, current=0.0), switchFunction=cells.Node.advance)       
    apicalTip.addSwitch("branchAtTheTop", cells.switch(min=-3, max=2, decay=3, rest=-3.0, current=-30.0), switchFunction=cells.Node.oneTimeBranch)       
    apicalTip.addSurfaceSignal("Pyramid")
    component.sproutProcess(relativeOrientation, apicalTip, diffuseSignalsOverride=component.childSignals)

def generateAxon(component, relativeOrientation):
        growthConePosition = array(component.position) + array(relativeOrientation)
        growthCone = cells.Node(initialPosition=growthConePosition, sensors=[], switches={}, surfaceSignals=[], diffuseSignals={}, switchFunctions={}, wantAds=component.wantAds, radius=1.4, connectingRadius=10, color=[1.0,0.7,0.0], debug=False)    
        # Sensors
#        growthCone.addSensor(cells.Sensor(growthCone, ["layerIVPyramid"],  targets={"Basket":-10.0}, gradient=False, threshold = 15.0))    
        growthCone.addSensor(cells.Sensor(growthCone, ["ExcitatoryAttractor"],  targets={"Basket":3.0}, gradient=False, threshold = 0.1))    
        growthCone.addSensor(cells.Sensor(growthCone, ["ExcitatoryAttractor"],  targets={"chemotaxisX":30.0}, gradient=True, axis=X, threshold = 0.01))
        growthCone.addSensor(cells.Sensor(growthCone, ["ExcitatoryAttractor"],  targets={"chemotaxisY":30.0}, gradient=True, axis=Y, threshold = 0.01))
        growthCone.addSensor(cells.Sensor(growthCone, ["ExcitatoryAttractor"],  targets={"chemotaxisZ":30.0}, gradient=True, axis=Z, threshold = 0.01))
        growthCone.addSensor(cells.Sensor(growthCone, ["Layer6"],  targets={"advancement":-2.0}, gradient=False, threshold = 5.0))    
        # Switches
        growthCone.addSwitch("chemotaxisX", cells.switch(min=-8, max=8, decay=0.6, rest=0.0, current=0.0), switchFunction=cells.Body.propulsionX)
        growthCone.addSwitch("chemotaxisY", cells.switch(min=-8, max=8, decay=0.6, rest=0.0, current=0.0), switchFunction=cells.Body.propulsionY)
        growthCone.addSwitch("chemotaxisZ", cells.switch(min=-8, max=8, decay=0.6, rest=0.0, current=0.0), switchFunction=cells.Body.propulsionZ)
        growthCone.addSwitch("oneTimeBranch", cells.switch(min=-2, max=1, decay=0.2, rest=1.0, current=randint(-1,0)), switchFunction=cells.Node.oneTimeBranch)
#        growthCone.addSwitch("oneTimeBranch", cells.switch(min=-8, max=1, decay=0.1, rest=1.0, current=randint(-8,-1)), switchFunction=cells.Node.oneTimeBranch)
        growthCone.addSwitch("advancement", cells.switch(min=0, max=3, decay=3, rest=3.0, current=3.0), switchFunction=cells.Node.advance)       
        growthCone.addSwitch("Basket", cells.switch(min=0, max=10, decay=0.5, rest=0.0, current=0.0), switchFunction = cells.Node.synapseFormation)
        component.sproutProcess(relativeOrientation, growthCone, diffuseSignalsOverride={})


class LayerIIIPyramidal(cells.Soma):
    def __init__(self, initialPosition, sensors, switches, surfaceSignals, diffuseSignals, switchFunctions, wantAds, radius=10, connectingRadius=0, color=[0.7,0.0,0.0], debug=False):
        cells.Soma.__init__(self, initialPosition, sensors, switches, surfaceSignals, diffuseSignals, switchFunctions, wantAds, radius, connectingRadius, color, debug)
        # Sensors
        self.addSensor(cells.Sensor(self, ["verticalOrientation"],  targets={"chemotaxisY":15.0}, gradient=True, axis=Y, threshold = 0.0))    
        self.addSensor(cells.Sensor(self, ["Layer3"],  targets={"chemotaxisY":-30.0, "triggerDendrites":10.0}, gradient=False, threshold = randint(2,10)))

        # Switches
        self.addSwitch("triggerDendrites", cells.switch(min=0, max=11, decay=0.0, rest=0.0, current=0.0), switchFunction=self.triggerDendrites)
        self.addSwitch("sproutBasals", cells.switch(min=0, max=8, decay=0.0, rest=0.0, current=0.0), switchFunction=self.sproutBasals)
        self.addSwitch("chemotaxisY", cells.switch(min=0, max=14, decay=0.3, rest=4.0, current=0.0), switchFunction=cells.Body.propulsionY)
#        self.addSwitch("sproutAxon", cells.switch(min=0, max=200, decay=0.1, rest=0.0, current=200.0), switchFunction=sproutBasals))

        # Diffuse Signals from the Soma
        self.diffuseSignals["horizontalOrientation"] = Signals.DiffuseSignalSource(self.position, radius=70, intensity=25, tiedTo=self)
        self.diffuseSignals["LayerIIIPyramid"] = Signals.DiffuseSignalSource(self.position, radius=70, intensity=25, tiedTo=self)
        self.diffuseSignals["BDNF"] = Signals.DiffuseSignalSource(self.position, radius=10, intensity=10)
        self.childSignals = {}
        self.childSignals["BDNF"] = self.diffuseSignals["BDNF"]
        self.addSurfaceSignal("Pyramid")
        
    def triggerDendrites(self, component, switch):
        if switch.current  > 10:
            self.switches["sproutBasals"].current = 8
            self.sproutApical()
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

    def sproutApical(self):
        offset = (self.radius) * vector(uniform(-0.05, 0.1),uniform(0.9, 1.0),uniform(-0.1, 0.05))
#        print "Sprouting apical dendrite at offset:", offset
        generateApicalDendrite(self, offset)

    def sproutAxon(self):
        offset = (self.radius) * vector(uniform(-0.05, 0.1),uniform(-0.9, -1.0),uniform(-0.1, 0.05))
#        print "Sprouting axon at offset:", offset
        generateAxon(self, offset)


class GeneralPyramidal(cells.Soma):
    def __init__(self, initialPosition, wantAds, target=["Layer4"], radius=10, connectingRadius=0, color=[0.7,0.0,0.0], debug=False):
        sensors = []
        switches = {}
        surfaceSignals = []
        diffuseSignals = {}
        switchFunctions = {}
        cells.Soma.__init__(self, initialPosition, sensors, switches, surfaceSignals, diffuseSignals, switchFunctions, wantAds, radius, connectingRadius, color, debug)
        # Sensors
        self.addSensor(cells.Sensor(self, ["verticalOrientation"],  targets={"chemotaxisY":15.0}, gradient=True, axis=Y, threshold = 0.0))    
        self.addSensor(cells.Sensor(self, [target, "layer3"],  targets={"chemotaxisY":-30.0, "triggerDendrites":10.0}, gradient=False, threshold = 1.0))

        # Switches
        self.addSwitch("triggerDendrites", cells.switch(min=0, max=11, decay=0.0, rest=0.0, current=0.0), switchFunction=self.triggerDendrites)
        self.addSwitch("sproutBasals", cells.switch(min=0, max=8, decay=0.0, rest=0.0, current=0.0), switchFunction=self.sproutBasals)
        self.addSwitch("chemotaxisY", cells.switch(min=0, max=14, decay=0.4, rest=8.0, current=0.0), switchFunction=cells.Body.propulsionY)
#        self.addSwitch("sproutAxon", cells.switch(min=0, max=200, decay=0.1, rest=0.0, current=200.0), switchFunction=sproutBasals))

        # Diffuse Signals from the Soma
        self.diffuseSignals["horizontalOrientation"] = Signals.DiffuseSignalSource(self.position, radius=70, intensity=25, tiedTo=self)
        self.diffuseSignals["BDNF"] = Signals.DiffuseSignalSource(self.position, radius=30, intensity=30)
        self.childSignals = {}
        self.childSignals["BDNF"] = self.diffuseSignals["BDNF"]
        self.addSurfaceSignal("Pyramid")
        
    def triggerDendrites(self, component, switch):
        if switch.current  > 10:
            self.switches["sproutBasals"].current = 8
            self.sproutApical()
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

    def sproutApical(self):
        offset = (self.radius) * vector(uniform(-0.05, 0.1),uniform(0.9, 1.0),uniform(-0.1, 0.05))
#        print "Sprouting apical dendrite at offset:", offset
        generateApicalDendrite(self, offset)

    def sproutAxon(self):
        offset = (self.radius) * vector(uniform(-0.05, 0.1),uniform(-0.9, -1.0),uniform(-0.1, 0.05))
#        print "Sprouting axon at offset:", offset
        generateAxon(self, offset)
