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
# connect to the server
robot = World.init()
# print important parts of the robot
print(sorted(robot.keys()))
timeSinceLastPickup = 0
timeStuck = 0

index = 0
def trySolveBeingStuck():
    randChoice = (-1)**randint(0,1)
    World.execute(dict(speedLeft= randChoice, speedRight= -randChoice),500,-1)
    World.execute(dict(speedLeft= 2, speedRight= 2),5000,-1)
        
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
    if sensorData["sensorLeft"] < 0.2 and sensorData["sensorRight"] < 0.2:
        timeStuck +=1
        print("Stucktick: %s" %(timeStuck))
        if timeStuck == 20:
            index += 1
            #trySolveBeingStuck()
            timeStuck=0
            
    if sensorData["sensorLeft"] == float("inf"):
        sensorData["sensorLeft"] = 1.1
        
    if sensorData["sensorRight"] == float("inf"):
        sensorData["sensorRight"] = 1.1
        
    if distanceToNearestEnergyBlock < 0.5:
        motorSpeed = dict(speedLeft=0, speedRight=0)
        World.collectNearestBlock()
        index =0
        timeSinceLastPickup = World.getSimulationTime()
    elif round(directionToNearestEnergyBlock,1) < 0 :
        motorSpeed = dict(speedLeft= directionToNearestEnergyBlock , speedRight=-directionToNearestEnergyBlock )
        
    elif round(directionToNearestEnergyBlock,1) > 0 :
        motorSpeed = dict(speedLeft= directionToNearestEnergyBlock, speedRight=-directionToNearestEnergyBlock)
    else:
        motorSpeed = dict(speedLeft=sensorData["sensorLeft"] *3, speedRight=sensorData["sensorRight"]* 3 )
        
   
    


        
    ########################################
    # Action Phase: Assign speed to wheels #
    ########################################
    # assign speed to the wheels
    World.setMotorSpeeds(motorSpeed)
    # try to collect energy block (will fail if not within range)
    if simulationTime%10000==0:
        print ("Trying to collect a block...",World.collectNearestBlock())
