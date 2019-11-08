# Make sure to have the server side running in V-REP:
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19999)
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!
import Lab1_Agents_Task1_World as World
from random import randint
import numpy as np

# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))
timeSinceLastPickup = 0
timeStuck = 0
index = 0
reverseOfPreviousActions = []
clientID = 0 

##----COPIED FROM Lab1_Agents_Task1_World.py TO BE ABLE TO USE IT ON OTHER SENSORS THAN 3 and 5----
def getObstacleDist(sensorHandler_):
        # Get raw sensor readings using API
        rawSR = World.vrep.simxReadProximitySensor(clientID, sensorHandler_, World.vrep.simx_opmode_oneshot_wait)
        #print(rawSR)
        # Calculate Euclidean distance
        if rawSR[1]: # if true, obstacle is within detection range, return distance to obstacle
            return World.math.sqrt(rawSR[2][0]*rawSR[2][0] + rawSR[2][1]*rawSR[2][1] + rawSR[2][2]*rawSR[2][2])
        else: # if false, obstacle out of detection range, return inf.
            return float('inf')
##------------------------------------------------------------------------------------

def returnToPreviousState():
    for reverseOfPreviosAction in reverseOfPreviousActions:
        World.execute(reverseOfPreviosAction["motorspeed"], reverseOfPreviosAction["simulationTime"], reverseOfPreviosAction["clockSpeed"])
    reverseOfPreviousActions.clear()

def readSensorData():
    sensorData = dict(sensorLeft= World.getSensorReading("ultraSonicSensorLeft"), sensorRight = World.getSensorReading("ultraSonicSensorRight"))
    if sensorData["sensorLeft"] == float("inf"):
        sensorData["sensorLeft"] = 1.1
        
    if sensorData["sensorRight"] == float("inf"):
        sensorData["sensorRight"] = 1.1
    return sensorData

def readFrontSensors():
    sensors = []
    for sensorIndex in range(1,9):
        ret_s, newSensor = World.vrep.simxGetObjectHandle(0, 'Pioneer_p3dx_ultrasonicSensor%s'%(sensorIndex),World.vrep.simx_opmode_oneshot_wait)
        sensors.append(dict(index= sensorIndex, distance= getObstacleDist(newSensor)))
        #print("SENSOR TEST: %s\n %s\n"%(ret_s, newSensor))
    return sensors

def calcRepulsingForceVector():
    ultraSonicSensors = readFrontSensors()
    robotDirection = World.robotDirection()
    repVec = 0.0
    repulsiveForceConstant = 0.2
    for sensor in ultraSonicSensors:
        if sensor["index"] < 5:
            repVec += (repulsiveForceConstant * ((World.math.pi/sensor["index"]) + robotDirection )/sensor["distance"])  + World.math.pi/2
        else:
            repVec += (repulsiveForceConstant * (robotDirection - (World.math.pi/sensor["index"]))/sensor["distance"]) + World.math.pi

        print("RECVEC: ID %s VALUE %s TYPE:%s"%(sensor["index"],repVec % (World.math.pi * 2),type(repVec)))  
    return repVec % (World.math.pi * 2)

def calcAttractingForceVector():
    nearestBlock = World.getSensorReading("energySensor").direction + World.math.pi/2
    print("ATTVEC:%s"%(nearestBlock))
    return nearestBlock

def calcDirectionToMove(retractingForceVector, attractingForceVector):
    finalForceVector = retractingForceVec + attractingForceVector
    print("NEWDIRECTION: %s" %(finalForceVector))
    return finalForceVector

def alignRobotToDirection(newDirection):
    while round(World.robotDirection(),2) != round(newDirection,2):
        robotDirection = World.robotDirection()
        if round(robotDirection,2) < round(newDirection,2):
            directionDifference =  newDirection - robotDirection
            World.execute(dict(speedLeft=directionDifference *2, speedRight=-directionDifference *2),40 ,-1)
            reverseOfPreviousActions.append(dict(motorspeed=dict(speedLeft= 2 , speedRight= -2 ),simulationTime=0,clockSpeed=-1))

            #print("ROBOTDIRECTION: %s   TARGETDIRECTION: %s "%(round(robotDirection,2), round(newDirection,2)))
            
        else:
            directionDifference = robotDirection - newDirection 
            World.execute(dict(speedLeft=-directionDifference *2 , speedRight=directionDifference *2 ),40,-1)
            reverseOfPreviousActions.append(dict(motorspeed=dict(speedLeft=directionDifference * 5 , speedRight=-directionDifference * 5),simulationTime=50,clockSpeed=-1))

            #print("ROBOTDIRECTION: %s   TARGETDIRECTION: %s "%(round(robotDirection,2), round(newDirection,2)))
            
        
    

while robot: # main Control loop
    #######################################################
    # Perception Phase: Get information about environment #
    #######################################################
    simulationTime = World.getSimulationTime()
    if simulationTime%1000==0:
        # print some useful info, but not too often
        print ('Time:',simulationTime,\
               'ultraSonicSensorLeft:',World.getSensorReading("ultraSonicSensorLeft"),\
               "ultraSonicSensorRight:", World.getSensorReading("ultraSonicSensorRight"))

    ##############################################
    # Reasoning: figure out which action to take #
    ##############################################
    
    energyBlocks = World.findEnergyBlocks()
    directionToNearestEnergyBlock = energyBlocks[index][3]
    distanceToNearestEnergyBlock = energyBlocks[index][2]
    sensorData = dict(sensorLeft= World.getSensorReading("ultraSonicSensorLeft"), sensorRight = World.getSensorReading("ultraSonicSensorRight"))
    
    directionOfRobot= World.robotDirection()
    # print("RobotDirection: %s, BlockDirection: %s, Difference: %s"%(directionOfRobot,directionToNearestEnergyBlock,directionOfRobot - directionToNearestEnergyBlock))
    # print ('Time:',simulationTime,\
    #            'ultraSonicSensorLeft:',World.getSensorReading("ultraSonicSensorLeft"),\
    #            "ultraSonicSensorRight:", World.getSensorReading("ultraSonicSensorRight"))

    # if(World.getSimulationTime() - timeSinceLastPickup > 100000):
    #     index +=1
    #     timeSinceLastPickup = World.getSimulationTime()

    # Check if driving straight into a wall
    #currentSensorData=readSensorData()

    retractingForceVec = calcRepulsingForceVector()
    retractingForceVec = calcAttractingForceVector()   

    targetDirection = calcDirectionToMove(retractingForceVec, retractingForceVec)
    if(round(directionOfRobot,2) != round(targetDirection,2)):
        alignRobotToDirection(targetDirection)
    World.execute(dict(speedLeft= 4 , speedRight=4 ),1500,-1)
    World.collectNearestBlock()
    
    #print("MOVING TO 0: RobotDirection:%s"%(World.robotDirection()))
    #
    
    print("MOVING TO Pi RobotDirection:%s"%(World.robotDirection()))
    #for energyblock in energyBlocks:
    #   alignRobotToDirection(energyblock[3] +(World.math.pi/2))

    '''if distanceToNearestEnergyBlock < 0.5:
        motorSpeed = dict(speedLeft=0, speedRight=0)
        World.collectNearestBlock()
        index =0
        timeSinceLastPickup = World.getSimulationTime()
    elif round(directionToNearestEnergyBlock,1) < 0 :
        World.execute(dict(speedLeft= directionToNearestEnergyBlock , speedRight=-directionToNearestEnergyBlock ),50,-1)
        reverseOfPreviousActions.append(dict(motorspeed=dict(speedLeft= -directionToNearestEnergyBlock , speedRight=directionToNearestEnergyBlock ),simulationTime=50,clockSpeed=-1))
       # motorSpeed = dict(speedLeft= directionToNearestEnergyBlock , speedRight=-directionToNearestEnergyBlock )
        
    elif round(directionToNearestEnergyBlock,1) > 0 :
        World.execute(dict(speedLeft= directionToNearestEnergyBlock , speedRight=-directionToNearestEnergyBlock),50,-1)
        reverseOfPreviousActions.append(dict(motorspeed=dict(speedLeft= -directionToNearestEnergyBlock , speedRight=directionToNearestEnergyBlock ),simulationTime=50,clockSpeed=-1))
    else:
        World.execute(dict(speedLeft= (-0.5) + currentSensorData["sensorLeft"] * 3, speedRight= (-0.5) + currentSensorData["sensorRight"] * 3 ),50,-1)
        reverseOfPreviousActions.append(dict(motorspeed=dict(speedLeft=-currentSensorData["sensorLeft"] *3, speedRight=-currentSensorData["sensorRight"]* 3 ),simulationTime=50,clockSpeed=-1))
       # motorSpeed = dict(speedLeft=sensorData["sensorLeft"] *3, speedRight=sensorData["sensorRight"]* 3 )
    

    if currentSensorData["sensorLeft"] < 0.2 and currentSensorData["sensorRight"] < 0.2:
        timeStuck +=1
        print("Stucktick: %s" %(timeStuck))
    if timeStuck == 20:
        #index += 1
        returnToPreviousState()
        timeStuck=0
    '''
    


        
    ########################################
    # Action Phase: Assign speed to wheels #
    ########################################
    # assign speed to the wheels
    #World.setMotorSpeeds(motorSpeed)
    # try to collect energy block (will fail if not within range)
    if simulationTime%10000==0:
        print ("Trying to collect a block...",World.collectNearestBlock())
SENSORS: [{'sensorHandle': 35, 'distance': 0.7763301525494896}, 
{'sensorHandle': 34, 'distance': inf},
{'sensorHandle': 33, 'distance': inf}, 
{'sensorHandle': 32, 'distance': 0.9433327344800936}, 
{'sensorHandle': 31, 'distance': inf}, 
{'sensorHandle': 30, 'distance': inf}, 
{'sensorHandle': 29, 'distance': inf}, 
{'sensorHandle': 28, 'distance': 0.9840285129662414}]