# coding: utf8
#!/usr/bin/python
################################################################
####################     IMPORT CLASSES     ####################
################################################################
# robot
import dbus
import dbus.mainloop.glib
from optparse import OptionParser
# local classes
from project import movement as Movement
from project import parameters as Parameters
from project import robot as Robot
from threading import Thread
# global variables
speed = 75
rangeBlack = 350
rangeWhite = 700
resetTimer = 100

################################################################
######################     MAIN CLASS     ######################
################################################################

"""
    Robot configuration: connect it to the computer
"""
def config():
    print("Config function starting...")
    parser = OptionParser()
    parser.add_option("-s", "--system", action="store_true", dest="system", default=False,help="use the system bus instead of the session bus")
 
    (options, args) = parser.parse_args()
 
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
 
    if options.system:
        bus = dbus.SystemBus()
        print("option system")
    else:
        bus = dbus.SessionBus()
        print("not option system")

    # Create Aseba network 
    network = dbus.Interface(bus.get_object('ch.epfl.mobots.Aseba', '/'), dbus_interface='ch.epfl.mobots.AsebaNetwork')
    print("Aseba Network: DONE")
    print("Config function done, NEXT...")
    return network

"""
    Init parameters: robot speed, white/black ranges
"""
def initParameters():
    print("InitParameters function starting...")
    parameters = Parameters.Parameters(speed, rangeWhite, rangeBlack)
    print(parameters.toString())
    print("InitParameters function done, NEXT...")
    return parameters

"""
    Init movement: by default: NONE (no moving)
"""
def initMovement():
    print("InitMovement function starting...")
    movement = Movement.Movement.STRAIGHT
    print("Movement > Current movement:", movement)
    print("InitMovement function done, NEXT...")
    return movement

"""
    Start the simulation
"""
def startSimulation(parameters, movement, network):
    print("Start the simulation...")

    robot = Robot.Robot(parameters, movement, network, resetTimer)
    f1 = Thread(target=robot.initialiseRangeAndCenter)
    f1.start()
    

    print("Simulation done, END...")


"""
    Main class
"""
if __name__ == "__main__":
    network = config()
    parameters = initParameters()
    movement = initMovement()
    startSimulation(parameters, movement, network)