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
clientID = 0 
amountOfBlocksLeft = len(World.findEnergyBlocks())

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
    ret_s, sensorLeft = World.vrep.simxGetObjectHandle(0, 'Pioneer_p3dx_ultrasonicSensor4',World.vrep.simx_opmode_oneshot_wait)
    ret_s, sensorRight = World.vrep.simxGetObjectHandle(0, 'Pioneer_p3dx_ultrasonicSensor5',World.vrep.simx_opmode_oneshot_wait)
    sensorData = dict(sensorLeft= getObstacleDist(sensorLeft), sensorRight = getObstacleDist(sensorRight) )
    if sensorData["sensorLeft"] == float('inf'):
        sensorData["sensorLeft"] = 1.1
        
    if sensorData["sensorRight"] == float('inf'):
        sensorData["sensorRight"] = 1.1
    return sensorData
def readParallellRightSensors():
    sensors= []
    for sensorIndex in range (8,10):
        ret_s, newSensor = World.vrep.simxGetObjectHandle(0, 'Pioneer_p3dx_ultrasonicSensor%s'%(sensorIndex),World.vrep.simx_opmode_oneshot_wait)
        sensors.append(dict(index= sensorIndex, distance= getObstacleDist(newSensor)))
    if sensors[0]["distance"] == float('inf'):
        sensors[0]["distance"]  = 1.1
    
    if sensors[1]["distance"]  == float('inf'):
        sensors[1]["distance"]  = 1.1
    
    return sensors

def followWall():
    stopFollowWall = False
    comparisonDistanceToNearestEnergyBlock = World.getSensorReading("energySensor").distance
    timeOutCounter = 0
    while not stopFollowWall:
        timeOutCounter += 1 
        print(timeOutCounter)
        if timeOutCounter > 5000:
            break
        distanceToNearestEnergyBlock = World.getSensorReading("energySensor").distance
        leftAndRightSensorData = readLeftAndRightSensorData()
        parallelRightSensors = readParallellRightSensors()
        print("Parallell Sensors: %s" % parallelRightSensors)
        print("FrontSensors : %s" % leftAndRightSensorData)
        differenceBetweenParallelSensors = parallelRightSensors[0]["distance"] - parallelRightSensors[1]["distance"]
        # Check if robot should try to go for new block or if robot can pick up plock.
        if (distanceToNearestEnergyBlock + 0.3 < comparisonDistanceToNearestEnergyBlock) or (distanceToNearestEnergyBlock < 0.5):
            stopFollowWall = True
            break
        # Align so follow wall by using sensor 8 and 9, parallell sensors on the right of the robot
        if ((round(differenceBetweenParallelSensors,2) < 0) or  (parallelRightSensors[0]["distance"] >  0.6 and parallelRightSensors[1]["distance"] > 0.6 and leftAndRightSensorData["sensorLeft"] > 0.4)) :
            
            World.setMotorSpeeds(dict(speedLeft= 0 , speedRight=  0.1 + (abs(differenceBetweenParallelSensors) ) ) )
        elif round(differenceBetweenParallelSensors,2 ) > 0 and leftAndRightSensorData["sensorLeft"] > 0.4 :
            
            World.setMotorSpeeds(dict(speedLeft = 1 +  (differenceBetweenParallelSensors * 2 ), speedRight=0  ) )
        else:
            World.setMotorSpeeds(dict(speedLeft= 1 - (1.1-leftAndRightSensorData["sensorLeft"]) * 2   , speedRight=  1 + (1.1-leftAndRightSensorData["sensorLeft"]) * 2 ) )
        


    

while robot: # main Control loop
    #######################################################
    # Perception Phase: Get information about environment #
    #######################################################
    directionToNearestEnergyBlock = World.getSensorReading("energySensor").direction
    distanceToNearestEnergyBlock = World.getSensorReading("energySensor").distance
    leftAndRightSensorData = readLeftAndRightSensorData()
    frontSensorsLeftAndRight = readFrontSensors()
    timeSinceLastPickup += 1
    ##############################################
    # Reasoning: figure out which action to take #
    ##############################################

    if timeSinceLastPickup > 50000:
        World.execute(dict(speedLeft=randint(-3,3), speedRight=randint(-3,3)),5000 ,-1)
        timeSinceLastPickup = 0

    # Check if stuck in front of a wall
    if (leftAndRightSensorData["sensorLeft"]) < 0.3 and  (leftAndRightSensorData["sensorRight"]  < 0.3) or (frontSensorsLeftAndRight["sensorLeft"]) < 0.3 and  (frontSensorsLeftAndRight["sensorRight"]  < 0.3) :
            timeStuck +=  1
            print("Time stuck:%s " % (timeStuck))
            if timeStuck == 20:
                followWall()
                timeStuck=0

    # Check if robot can pick up block
    if distanceToNearestEnergyBlock < 0.5:
        motorSpeed = dict(speedLeft=0, speedRight=0)
        pickup = World.collectNearestBlock()
        if pickup == 'Energy collected :)':
            amountOfBlocksLeft -= 1
            print("Amount of blocks left: %s"% amountOfBlocksLeft)
            if(amountOfBlocksLeft < 1):
                print("I'm Done! :)")

    # Align to nearest block and move towards it 
    elif round(directionToNearestEnergyBlock,1) <  0:
        World.setMotorSpeeds(dict(speedLeft= directionToNearestEnergyBlock , speedRight=-directionToNearestEnergyBlock ) )
    elif round(directionToNearestEnergyBlock,1) > 0 :
        World.setMotorSpeeds(dict(speedLeft= directionToNearestEnergyBlock , speedRight=-directionToNearestEnergyBlock ) )
    else:
        if(leftAndRightSensorData["sensorLeft"] > 0.2 and leftAndRightSensorData["sensorRight"] >0.2):
            World.setMotorSpeeds(dict(speedLeft= 2  , speedRight= 2 ) )
        else:
            World.setMotorSpeeds(dict(speedLeft= 2 - (2.2 - leftAndRightSensorData["sensorRight"])  , speedRight= 2 - (2.2 - leftAndRightSensorData["sensorLeft"]) ) )
    