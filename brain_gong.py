# ------------__ Hacking STEM – brain_gong.py – micro:bit __-----------
#  For use with the Building Models to Understand and Mitigate Brain Injury
#  lesson plan available from Microsoft Education Workshop at
#  https://education.microsoft.com/hackingStem/lesson/ecaf3891
#  http://aka.ms/hackingSTEM
#
#  Overview: This project reads voltage on 5 GPIO pins and writes those values 
#  to serial. It also tares (zeros out) the readings on start up, and reads 
#  serial and looks for keywords.
#
#  This project uses a BBC micro:bit microcontroller, information at:
#  https://microbit.org/
#
#  Comments, contributions, suggestions, bug reports, and feature
#  requests are welcome! For source code and bug reports see:
#  https://github.com/microsoft/hackingstem-braingong-microbit
#
#  Copyright 2018, Adi Azulay
#  Microsoft EDU Workshop - HackingSTEM
#  MIT License terms detailed in LICENSE.txt
# ===---------------------------------------------------------------===

from microbit import *

# Setup & Config
display.off()  # Turns off LEDs to free up additional input pins
uart.init(baudrate=9600)  # Sets serial baud rate
DATA_RATE = 10 # Frequency of code looping
EOL = '\n' # End of Line Character

# These constants are the pins used on the micro:bit for the sensors 
BRAIN_SENSOR_PIN1 = pin0
BRAIN_SENSOR_PIN2 = pin1
BRAIN_SENSOR_PIN3 = pin2
BRAIN_SENSOR_PIN4 = pin3
BRAIN_SENSOR_PIN5 = pin4

#TODO Remove this function
def tare(pin):
    # Each sensor has some level of variablity in the readings it outputs. This 
    # function shifts the base line up or down so the starting value is close to 0
    tare_value = pin.read_analog()
    return tare_value

brain_sensor_1_tare = tare(BRAIN_SENSOR_PIN1)
brain_sensor_2_tare = tare(BRAIN_SENSOR_PIN2)
brain_sensor_3_tare = tare(BRAIN_SENSOR_PIN3)
brain_sensor_4_tare = tare(BRAIN_SENSOR_PIN4)
brain_sensor_5_tare = tare(BRAIN_SENSOR_PIN5)

def process_sensors():
    # This function reads voltage of from each pin attached to a pressure sensor 
    # and then subtracts the tare value we calculated for it earlier.
    global brain_sensor_1, brain_sensor_2, brain_sensor_3, brain_sensor_4, brain_sensor_5
    brain_sensor_1 = BRAIN_SENSOR_PIN1.read_analog() - brain_sensor_1_tare
    brain_sensor_2 = BRAIN_SENSOR_PIN2.read_analog() - brain_sensor_2_tare
    brain_sensor_3 = BRAIN_SENSOR_PIN3.read_analog() - brain_sensor_3_tare
    brain_sensor_4 = BRAIN_SENSOR_PIN4.read_analog() - brain_sensor_4_tare
    brain_sensor_5 = BRAIN_SENSOR_PIN5.read_analog() - brain_sensor_5_tare


#=============================================================================#
#---------------The Code Below Here is for Excel Communication----------------#
#=============================================================================#

# Array to hold the serial data
parsedData = [0] * 5

def getData():
    #   This function gets data from serial and builds it into a string
    global parsedData, builtString
    builtString = ""
    while uart.any() is True:
        byteIn = uart.read(1)
        if byteIn == b'\n':
            continue
        byteIn = str(byteIn)
        splitByte = byteIn.split("'")
        builtString += splitByte[1]
    parseData(builtString)
    return (parsedData)

def parseData(s):
    #   This function seperates the string into an array
    global parsedData
    if s != "":
        parsedData = s.split(",")

#=============================================================================#
#------------------------------Main Program Loop------------------------------#
#=============================================================================#
while (True):
    process_sensors()
    serial_in_data = getData()
    if (serial_in_data[0] != "#pause"):
        #uart is the micro:bit command for serial
        uart.write('{},{},{},{},{}'.format(brain_sensor_1, brain_sensor_2, brain_sensor_3, brain_sensor_4, brain_sensor_5)+EOL)

    sleep(DATA_RATE)
