from __future__ import division
from cells import *
from math import pi
from visual import *
import random

X = 0
Y = 1
Z = 2

def propulsionX(cellComponent, switch):
    if cellComponent.debug:
        print "X", switch.current
    cellComponent.force[X] += switch.current *2* pi * cellComponent.radius**2
    
def propulsionY(cellComponent, switch):
    if cellComponent.debug:
        print "Y", switch.current
    cellComponent.force[Y] += switch.current *2* pi * cellComponent.radius**2

def propulsionZ(cellComponent, switch):
    if cellComponent.debug:
        print "Z", switch.current
    cellComponent.force[Z] += switch.current *2* pi * cellComponent.radius**2
    
def doNothing(cellComponent, switch):
    return

# Node Functions

    def advance(self, switch):
        if switch.current > 0:
            newPosition = vector(self.position) + norm(vector(self.parents[0].axis)) * switch.current / 50
            self.position = newPosition
            self.parent.restLength = distance(self.parent.position, newPosition)
            
    def synapseFormation(self, switch):
        print "Synapse Switch", switch.current
        if switch.current > random.randint(0,100):
            print "Synapse Passed!"
            print self.wantAds
            potentialMatches = []
            for target in self.switches.keys():
                if self.switches[target] == switch:
                    if target in self.wantAds.keys():
                        potentialMatches = self.wantAds[target] 
                        print potentialMatches
            minimumDistance = self.connectingRadius
            bestMatch = None
            for match in potentialMatches:
                if distance(self.position, match.position) < minimumDistance:
                    print "New Best Match!"
                    bestMatch = match
            print bestMatch
            if bestMatch is not None:
                direction = vector(self.position) - vector(bestMatch.position)
                tempProcess = bestMatch.sproutProcess(direction, self)
                # Delete the key that led to this synapse being formed
                for key in self.switches.keys():
                    if self.switches[key] == switch:
                        del self.switches[key]
#                tempProcess.restLength -= tempProcess.restLength * 0.1
                self.retire(advance=True)

    def retire(self, cone=True, taxis=True, advance=False):
        if "oneTimeBranch" in self.switches.keys():
            self.switches["oneTimeBranch"].rest=-10.0
            self.switches["oneTimeBranch"].current=-10.0
        if "growthCone" in self.switches.keys() and cone:
            self.switches["growthCone"].rest=0.0
            self.switches["growthCone"].current=0.0
        if "chemotaxisX" in self.switches.keys() and taxis:
            self.switches["chemotaxisX"].min = 0.0
            self.switches["chemotaxisX"].max = 0.0
        if "chemotaxisY" in self.switches.keys() and taxis:
            self.switches["chemotaxisY"].min = 0.0
            self.switches["chemotaxisY"].max = 0.0
        if "chemotaxisZ" in self.switches.keys() and taxis:
            self.switches["chemotaxisZ"].min = 0.0
            self.switches["chemotaxisZ"].max = 0.0
        if "advancement" in self.switches.keys() and advance:
            self.switches["advancement"].current=0.0
            self.switches["advancement"].max = 0.0
            self.switches["advancement"].min = 0.0
            self.switches["advancement"].rest=0.0
            self.switches["advancement"].decay = 10.0

    def executeBranch(self):
        # Stop being a growth cone.  Turn off chemotaxis and turn off the growthCone switch
        self.retire()
        # Create two new nodes with the current properties
        theta = random.randint(0,90)
        rotAxis = [random.randint(-10,100), random.randint(-10,100), random.randint(-10,100)]
        leftNodePosition = 1*rotate(norm(vector(self.parent.axis)), angle=theta, axis=rotAxis)
        rightNodePosition = 1*rotate(norm(vector(self.parent.axis)), angle=-theta, axis=rotAxis)
        leftNode = Node(initialPosition=leftNodePosition, sensors=copy.copy(self.sensors), switches={}, surfaceSignals=copy.copy(self.surfaceSignals), diffuseSignals=copy.copy(self.diffuseSignals), switchFunctions=self.switchFunctions.copy(), wantAds=self.wantAds, radius=self.radius, connectingRadius=0, color=self.color)
        rightNode = Node(initialPosition=rightNodePosition, sensors=copy.copy(self.sensors), switches={}, surfaceSignals=copy.copy(self.surfaceSignals), diffuseSignals=copy.copy(self.diffuseSignals), switchFunctions=self.switchFunctions.copy(), wantAds=self.wantAds, radius=self.radius, connectingRadius=0, color=self.color)
        self.copySwitches(leftNode, self.switches, self.switchFunctions)
        self.copySwitches(rightNode, self.switches, self.switchFunctions)
        self.sproutProcess(leftNodePosition, leftNode)
        self.sproutProcess(rightNodePosition, rightNode)
        # Delete the branch switch from the current node.
        for key in self.switches.keys():
            if self.switches[key] == switch:
                del self.switches[key]

    def oneTimeBranch(self, switch):
        if random.randint(0,100) < switch.current: #Stochastic - there is a chance of branching per time step.    
            # Delete the one time branch switch from the current node before it is passed on to others
            for key in self.switches.keys():
                if self.switches[key] == switch:
                    del self.switches[key]
#            self.retire(advance=True)
            self.executeBranch()
            # Stop moving
            self.retire(advance=True)

