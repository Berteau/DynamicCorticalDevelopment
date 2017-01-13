from __future__ import division
from visual import *
from math import exp, sqrt

def compileSignals(totalSignals, signalDict):
    for signalName in signalDict.keys():
        try: #check to see if key exists
            totalSignals[signalName]
        except KeyError:
            totalSignals[signalName] = []            
        # Append signals to the key
        if isinstance(signalDict[signalName], list):
            for signal in signalDict[signalName]:
                totalSignals[signalName].append(signal)
        else:
            totalSignals[signalName].append(signalDict[signalName])
    return totalSignals

def distance(point1, point2):
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)

class DiffuseSignalSource():
    def __init__(self, position, radius, intensity, tiedTo = None, visible=False):
        self.position = position
        self.radius = radius
        self.sd = self.radius*10 # / 2.3
        self.sigma = 1 / self.sd
        self.intensity = intensity
        self.tiedTo = tiedTo #Body
        self.visible = visible
        if self.visible:
            self.rendering = sphere(pos=vector([20,10,10]), radius=2, color=color.green)
        
    def sampleAtLocation(self, sampleLocation):
        return self.intensity * exp(-self.sigma * distance(self.position, sampleLocation)**2)
    
    def update(self):
        if self.tiedTo is not None:
            self.position = self.tiedTo.position
        if self.visible:
            self.rendering.pos = vector(self.position)