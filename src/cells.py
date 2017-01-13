from __future__ import division
from math import sqrt, e, pi, sin, cos
from visual import *
from scipy import array, mat, dot
from Signals import compileSignals
from CellFunctions import X, Y, Z
import random
import copy

def distance(point1, point2):
    return sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2 + (point1[2] - point2[2])**2)

class CellComponent():
    def __init__(self, position, diffuseSignals):
        self.position = position
        self.diffuseSignals = diffuseSignals
        self.children = []
        self.parents = []
        self.parent = None
    def fetchDiffuseSignals(self):
        totalSignals = {}
        compileSignals(totalSignals, self.diffuseSignals)
        for child in self.children:
            compileSignals(totalSignals, child.fetchDiffuseSignals())
        return totalSignals 
    def addParent(self, parent):
        self.parents.append(parent)
        if self.parent is None:
            self.parent = parent
    def update(self, globalDiffuseSignals):
        for child in self.children:
            child.update(globalDiffuseSignals)

class Body(CellComponent):
    def __init__(self, initialPosition, sensors, switches, surfaceSignals, diffuseSignals, switchFunctions, wantAds, radius=20, connectingRadius=0, color=[1,1,1], debug=False, visible=True):
        CellComponent.__init__(self, initialPosition, diffuseSignals)
        self.wantAds = wantAds
        self.radius = radius
        self.connectingRadius = connectingRadius
        self.color = color
        self.visible = visible
        if self.visible:
            self.rendering = sphere(pos=vector(self.position), radius=self.radius, color=self.color)
        else:
            self.rendering = None
        self.switches = switches
        self.switchFunctions = switchFunctions
        self.sensors = sensors
        self.surfaceSignals = surfaceSignals
        self.diffuseSignals = diffuseSignals
        self.drag = 0.5
        self.force = [0,0,0]
        self.vel = [0,0,0]
        self.debug = debug
        # Post the want ad
        for eachSignal in surfaceSignals:
            if eachSignal in self.wantAds.keys():
                self.wantAds[eachSignal].append(self)
            else:
                self.wantAds[eachSignal] = [self]
                
    def sproutProcess(self, axis, node, diffuseSignalsOverride=None):
        node.position = list(array(self.position) + array(axis))
        node.visible = true
        if diffuseSignalsOverride is not None:
            initialProcess = Process(self, node, diffuseSignalsOverride, color=node.color, radiusBase=node.radius/2.0)
        else:
            initialProcess = Process(self, node, copy.copy(self.diffuseSignals), color=node.color, radiusBase=node.radius/2.0)
        node.addParent(initialProcess)
        self.children.append(initialProcess)
        return initialProcess

    def addSensor(self, sensor):
        self.sensors.append(sensor)

    def addDiffuseSignal(self, signalName, signal):
        self.diffuseSignals[signalName] = signal
        
    def addSurfaceSignal(self, signalName):
        self.surfaceSignals.append(signalName)
        if signalName in self.wantAds.keys():
            self.wantAds[signalName].append(self)
        else:
            self.wantAds[signalName] = [self]
        
    def addSwitch(self, key, switch, switchFunction):
        self.switches[key] = switch
        self.switchFunctions[key] = switchFunction        
#    def addProcess(self, c):

    def update(self, globalDiffuseSignals):
        #Clear some variables
        self.force = [0,0,0]
        switchInputs = {}
        
        # Get the switch inputs from sensors
        for sensor in self.sensors:
            temp = sensor.getOuputs(globalDiffuseSignals, self.debug) # Get the outputs
            # Add them in to temp inputs
            for key in temp.iterkeys():
                try:
                    switchInputs[key] = switchInputs[key] + temp[key]
                except KeyError:
                    switchInputs[key] = temp[key]
                    
        # Now update the switches with the inputs
        for key in self.switches.iterkeys(): # For each switch
            try:
                self.switches[key].update(switchInputs[key], self.debug)
            except KeyError:
                self.switches[key].update(0)
            
        # Act based on the switches
        keyList = self.switches.keys()
        for switch in keyList:
            self.switchFunctions[switch](self, self.switches[switch])
        if self.debug:
            print "Current Force after polling switches", self.force

        # Get force from the efferent children, then update each
        for child in self.children:
            if self.debug:
                tempForce = child.getForce(self)
            else:
                tempForce = child.getForce(self)
            self.force[X] += tempForce[X]
            self.force[Y] += tempForce[Y]
            self.force[Z] += tempForce[Z]
            if self.debug:
                print "Current Force after polling children", self.force
            child.update(globalDiffuseSignals)

        # Get force from the afferent parents, but don't update - they'll be taken care of as children of something else.
        for parent in self.parents:
            if self.debug:
                tempForce = parent.getForce(self)
            else:
                tempForce = parent.getForce(self)
            self.force[X] += tempForce[X]
            self.force[Y] += tempForce[Y]
            self.force[Z] += tempForce[Z]
            if self.debug:
                print "Current Force after polling parents", self.force
                
        # In the future, get force from collisions with things.  For now, all cells are ghosts unless connected.
            
        # Update Kinetics
        drag = [0,0,0]
        drag[X] = self.drag*self.vel[X]
        drag[Y] = self.drag*self.vel[Y]
        drag[Z] = self.drag*self.vel[Z]
        mass = pi * (self.radius**2)
        accelX = (self.force[X]/mass - drag[X]) 
        accelY = (self.force[Y]/mass - drag[Y])
        accelZ = (self.force[Z]/mass - drag[Z])
        self.vel[X] = accelX / 100.0
        self.vel[Y] = accelY / 100.0
        self.vel[Z] = accelZ / 100.0
        if self.debug:
            print "Mass", mass
            print "Drag", drag
            print "Acceleration", accelX, accelY, accelZ
            print "Velocity", self.vel
        
        # Update cell position based on kinetics
        self.position = list(array(self.position) + array(self.vel))
        if self.debug:
            print "Position:",self.position
            
        # Bring any diffuseSignals attached to us into accord
        for signal in self.diffuseSignals.iterkeys():
            self.diffuseSignals[signal].update()

        # Bring rendering into accord
        self.rendering.pos = vector(self.position)
        self.rendering.radius = self.radius
    
    # Define default switch actions - others can be passed in as parameters to the addSwitch function
    def propulsionX(self, switch):
        if self.debug:
            print "X", switch.current
        self.force[X] += switch.current *2* pi * self.radius**2
        
    def propulsionY(self, switch):
        if self.debug:
            print "Y", switch.current
        self.force[Y] += switch.current *2* pi * self.radius**2

    def propulsionZ(self, switch):
        if self.debug:
            print "Z", switch.current
        self.force[Z] += switch.current *2* pi * self.radius**2
        
    def doNothing(self, switch):
        return
                            
class Process(CellComponent):
    def __init__(self, parent, target, diffuseSignals, color=[1,1,1], radiusBase=5):
        CellComponent.__init__(self, parent.position, diffuseSignals)
        self.tensionConstant = 5.0
        self.damping = 1.0
        self.parent = parent
        self.children.append(target)
        self.target = target
        self.axis = [self.target.position[dimension] - self.parent.position[dimension] for dimension in range(len(self.parent.position))]
        self.restLength = distance(self.parent.position, self.target.position)
        self.lastDistance = self.restLength
        self.radiusBase = radiusBase
        self.radius = 1 + self.radiusBase / (1 + e**(self.restLength*0.1))
        self.midpoint = array(self.parent.position) + array(self.axis) / 2
        self.color = color
        self.rendering = cylinder(pos=self.position, axis=[target.position[dimension] - parent.position[dimension] for dimension in range(len(parent.position))], radius=self.radius, color=self.color)

#    def growToFit(self):
#        if distance(self.parent.position, self.target.position) > self.restLength:
#            self.restLength = distance(self.parent.position, self.target.position)
        
    def getForce(self, soma, debug=False):
        force = array([])
        newDistance = distance(self.parent.position, self.target.position)
        stretch = (distance(self.parent.position, self.target.position) - self.restLength)
        soma1v = mat(self.parent.vel)
        vdiff  = mat(self.parent.vel)-mat(self.target.vel)
        if debug:
            print soma1v
            print vdiff
            print mat(self.axis)
        
        vDiff = (array(self.parent.vel)-array(self.target.vel))
        L = array(self.axis)
        ks = self.tensionConstant
        kd = self.damping
        r = self.restLength
        l = newDistance
        springForce = ks*(l - r)
        springDamp = kd*(dot(vDiff,L))
        force = ((springForce + springDamp) * L) / l        
        if debug:
            print "~~~~~~~~~~~~"
            print "currentLength", l
            print "restLength", r
            print "Spring Force", springForce
            print "Spring Damping", springDamp
            print "Stretch:", stretch
            print "Force:",force
        if soma == self.parent:
            return force
        if soma == self.target:
            return -force
        else:
            return [0 for dim in self.rendering.axis]

    def update(self, globalDiffuseSignals):
#        print "Parent", self.parent, "Target", self.target
#        print distance(self.parent.position, self.target.position)
#        print e**(distance(self.parent.position, self.target.position)*0.1)
        self.radius = 1 + self.radiusBase / (1 + e**(distance(self.parent.position, self.target.position)*0.1))
        self.axis = [self.target.position[dimension] - self.parent.position[dimension] for dimension in range(len(self.parent.position))]
        self.midpoint = array(self.parent.position) + array(self.axis) / 2
        self.lastDistance = distance(self.parent.position, self.target.position)
        self.rendering.pos=self.parent.position
        self.rendering.axis = self.axis
        self.rendering.radius=self.radius
        for child in self.children:
            child.update(globalDiffuseSignals)
                    
# Sensor class
class Sensor():
    def __init__(self, parent, signalNames, targets, gradient=False, axis=-1, threshold=0):
        self.signalNames = signalNames
        self.targets = targets #Pairing of target keys with target weights
        self.threshold = threshold
        self.parent = parent #Body
        self.isGradient = gradient
        self.axis = [0,0,0]
        self.axis[axis] = 0.5
        
    def getOuputs(self, signals, debug=False):
        outputs = {}
        for key in self.targets.iterkeys():
            outputs[key] = 0
        if self.isGradient:
            for name in self.signalNames:
                try:
                    signalStrength = sum([source.sampleAtLocation(self.parent.position) for source in signals[name]])
                    gradientStrength = sum([source.sampleAtLocation(list(array(self.parent.position)+ array(self.axis))) for source in signals[name]]) - signalStrength
                    if debug:
                        print "Sensor checking position:", list(array(self.parent.position)+ array(self.axis))
                        print "signalStrength", signalStrength
                        print "gradientStrength", gradientStrength
                    if abs(gradientStrength) > self.threshold:
                        for key in self.targets.iterkeys():
                            outputs[key] += gradientStrength * self.targets[key]
                except KeyError:
                    outputs[key] += 0
            return outputs
        else:
            for name in self.signalNames:
                try:
                    signalStrength = sum([source.sampleAtLocation(self.parent.position) for source in signals[name]])
                    if signalStrength > self.threshold:
                        for key in self.targets.iterkeys():
                                
                                    outputs[key] += signalStrength * self.targets[key] # signal strength times weight
                except KeyError:
                    outputs[key] += 0
            return outputs

class switch():
    def __init__(self, min, max, decay, rest, current):
        self.min = min
        self.max = max
        self.decay = decay
        self.rest = rest
        self.current = current

    def update(self, input, debug = False):
        iPlus = 0
        iMinus = 0
        if input >= 0:
            iPlus = input
        elif input < 0:
            iMinus = input
        if debug:
            print "~~~~~~~~~~"
            print "Input", input
            print "Switch change", self.decay*(self.rest - self.current) + iPlus * (self.max - self.current) - iMinus*(self.min + self.current)
            print "Switch decay", self.decay*(self.rest - self.current)
            print "Switch Reversal", iMinus*(self.min + self.current)
            print "Current value", self.current
        delta = self.decay*(self.rest - self.current) + iPlus * (self.max - self.current) + iMinus*(-self.min + self.current)
        self.current = self.current + delta / 100
#        if switch > 
        
        
class Node(Body):
    def __init__(self, initialPosition, sensors, switches, surfaceSignals, diffuseSignals, switchFunctions, wantAds, radius=2, connectingRadius=0, color=[1,1,1], debug=False):
        Body.__init__(self, initialPosition, sensors, switches, surfaceSignals, diffuseSignals, switchFunctions, wantAds, radius, connectingRadius, color, debug)
        self.parent = None
            
    def advance(self, switch):
        if switch.current > 0:
#            print switch.current
#            self.parents[0].restLength += switch.current / 100
            newPosition = vector(self.position) + norm(vector(self.parents[0].axis)) * switch.current / 50
            self.position = newPosition
#            print "Growing to fit"
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

    def copySwitches(self, target, switches, switchFunctions):
        for key in switches.keys():
            target.addSwitch(key, switch(min=switches[key].min, max=switches[key].max, decay=switches[key].decay, rest=switches[key].rest, current=switches[key].current), switchFunction=switchFunctions[key])

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
    
    def branchInPlace(self, switch):
        if random.randint(0,100) < switch.current: #Stochastic - there is a chance of branching per time step.                    
            # Will the new branches be terminal?
            stepParent = self
            steps = 0
            while not isinstance(stepParent, Soma):
                stepParent = stepParent.parent
                steps += 1
            if random.randint(0,9) < steps:
                # Delete the branch switch from the current node.
                for key in self.switches.keys():
                    if self.switches[key] == switch:
                        del self.switches[key]    
                # Stop advancement based growth
                self.retire(advance=True)
            else:            
                # Reset branching probabilitiy
                switch.current = -20
            self.executeBranch()
            # Stop advancement-based growth
            self.retire(advance=True)
            
#    def BranchAndCease(self):
#        
    def update(self, globalDiffuseSignals):
#        if "growthCone" in self.switches.keys():
#            if self.switches["growthCone"].current > 1:
#                    self.parent.growToFit()
        Body.update(self, globalDiffuseSignals)
        for child in self.children:
            child.update(globalDiffuseSignals)
        
# Define soma
class Soma(Body):
    def __init__(self, initialPosition, sensors, switches, surfaceSignals, diffuseSignals, switchFunctions, wantAds, radius=10, connectingRadius=0, color=[1,1,1], debug=False):
        Body.__init__(self, initialPosition, sensors, switches, surfaceSignals, diffuseSignals, switchFunctions, wantAds, radius, connectingRadius, color, debug)

    def grow(self, switch):
        self.radius = self.radius + (switch.current / 1000)
