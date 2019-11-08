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
#import numpy as np

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

def readLeftAndRightSensorData():
    ret_s, sensorLeft = World.vrep.simxGetObjectHandle(0, 'Pioneer_p3dx_ultrasonicSensor3',World.vrep.simx_opmode_oneshot_wait)
    ret_s, sensorRight = World.vrep.simxGetObjectHandle(0, 'Pioneer_p3dx_ultrasonicSensor6',World.vrep.simx_opmode_oneshot_wait)
    sensorData = dict(sensorLeft= getObstacleDist(sensorLeft), sensorRight = getObstacleDist(sensorRight) )
    if sensorData["sensorLeft"] == float('inf'):
        sensorData["sensorLeft"] = 1.1
        
    if sensorData["sensorRight"] == float('inf'):
        sensorData["sensorRight"] = 1.1
    return sensorData

def readFrontSensors():
    sensors = []
    for sensorIndex in range(1,9):
        ret_s, newSensor = World.vrep.simxGetObjectHandle(0, 'Pioneer_p3dx_ultrasonicSensor%s'%(sensorIndex),World.vrep.simx_opmode_oneshot_wait)
        sensors.append(dict(index= sensorIndex, distance= getObstacleDist(newSensor)))
        
    return sensors

def calcRepulsingForceVector():
    ultraSonicSensors = readFrontSensors()
    robotDirection = World.robotDirection()
    repVec = 0.0
    repulsiveForceConstant = 0.5
    for sensor in ultraSonicSensors:
        #print("SENSOR: ID %s VALUE %s"%(sensor["index"],sensor["distance"]))  
        if sensor["index"] < 5:
            repVec = World.normaliseAngle( repVec + repulsiveForceConstant * ((World.math.pi)/sensor["index"]) /sensor["distance"])  
        else:
            repVec = World.normaliseAngle(repVec + repulsiveForceConstant * ((-World.math.pi)/sensor["index"])/sensor["distance"]) 
        
        #print("RECVEC: ID %s VALUE %s TYPE:%s"%(sensor["index"],repVec % (World.math.pi * 2),type(repVec)))  
    return repVec # % (World.math.pi/2)

def calcAttractingForceVector():
    nearestBlock = World.getSensorReading("energySensor") 
    
    #print("ATTVEC Direction :%s  RELATIVE X: %s, RELATIVE Y: %s"%(nearestBlock.direction, nearestBlockRelative_X, nearestBlockRelative_Y ))
    return  World.normaliseAngle( nearestBlock.direction + World.robotDirection())

def calcDirectionToMove(retractingForceVector, attractingForceVector):
    finalForceVector = World.normaliseAngle(retractingForceVector + attractingForceVector)
    print("NEWDIRECTION: %s" %(finalForceVector))
    return finalForceVector

def alignRobotToDirection(newDirection):
    while round(World.robotDirection(),2) != round(newDirection,2):
        robotDirection = World.robotDirection()
        if round(robotDirection,2) < round(newDirection,2):
            directionDifference =  newDirection - robotDirection
            World.execute(dict(speedLeft=directionDifference *2, speedRight=-directionDifference *2),40 ,-1)
            reverseOfPreviousActions.append(dict(motorspeed=dict(speedLeft=directionDifference *2, speedRight=-directionDifference *2),simulationTime=40,clockSpeed=-1))

            #print("ROBOTDIRECTION: %s   TARGETDIRECTION: %s "%(round(robotDirection,2), round(newDirection,2)))
            
        else:
            directionDifference = robotDirection - newDirection 
            World.execute(dict(speedLeft=-directionDifference *2 , speedRight=directionDifference *2 ),40,-1)
            reverseOfPreviousActions.append(dict(motorspeed=dict(speedLeft=-directionDifference *2 , speedRight=directionDifference *2 ),simulationTime=40,clockSpeed=-1))

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
    
    
    directionOfRobot= World.robotDirection()
    # if(World.getSimulationTime() - timeSinceLastPickup > 100000):
    #     index +=1
    #     timeSinceLastPickup = World.getSimulationTime()

    # Check if driving straight into a wall
    #currentSensorData=readSensorData()
    leftAndRightSensorData = readLeftAndRightSensorData()
    if (leftAndRightSensorData["sensorLeft"]) < 0.2 and  (leftAndRightSensorData["sensorRight"]  < 0.2) :
            timeStuck +=  1
            if timeStuck == 20:
                returnToPreviousState()
                timeStuck=0
    if timeSinceLastPickup > 500000:
        returnToPreviousState()
        timeSinceLastPickUp = 0

    retractingForceVec = calcRepulsingForceVector()
    attractingForceVec = calcAttractingForceVector()   
    targetDirection = calcDirectionToMove(retractingForceVec, attractingForceVec)
    
    alignRobotToDirection(targetDirection)
    
    #print(leftAndRightSensorData)
    World.setMotorSpeeds(dict(speedLeft= leftAndRightSensorData["sensorLeft"] * 2 , speedRight=leftAndRightSensorData["sensorRight"] * 2 ) )#
    reverseOfPreviousActions.append(dict(motorspeed=dict(speedLeft= leftAndRightSensorData["sensorLeft"] * 2 , speedRight=leftAndRightSensorData["sensorRight"] * 2 ),simulationTime=10,clockSpeed=-1))


    nearestBlockDistance =  World.getSensorReading("energySensor").distance
    if nearestBlockDistance < 0.5 : 
        World.collectNearestBlock()
        timeSinceLastPickUp = 0
    timeSinceLastPickup += 1
    #print("MOVING TO 0: RobotDirection:%s"%(World.robotDirection()))
    #
    
    print("MOVING TO Pi RobotDirection:%s"%(World.robotDirection()))
    #for energyblock in energyBlocks:
    #   alignRobotToDirection(energyblock[3] +(World.math.pi/2))
    
    


        
    ########################################
    # Action Phase: Assign speed to wheels #
    ########################################
    # assign speed to the wheels
    #World.setMotorSpeeds(motorSpeed)
    # try to collect energy block (will fail if not within range)
    #if simulationTime%10000==0:
    #     print ("Trying to collect a block...",World.collectNearestBlock())
