import RPi.GPIO as GPIO
from time import sleep
import pigpio
import DHT22




# The script as below using BCM GPIO 00..nn numbers
GPIO.setmode(GPIO.BCM)

#Initiate GPIO for pigpio
pi = pigpio.pi()

#Water pump Heat and relay
#setup temp and humiditysensor
dht22 = DHT22.sensor(pi,4)
waterheat = 18
GPIO.setup(waterheat, GPIO.OUT)
GPIO.output(waterheat, GPIO.LOW)

#Light sensor and relay
#LIght sensor 0 = light threshold hit 1 = light threshold not hit
lightsensor = 17
lightrelay = 22
GPIO.setup(17, GPIO.IN)
GPIO.setup(lightrelay, GPIO.OUT)

#Watering pump relay and Moisture sensor
plantpump = 24
plantpumsensor = 23
compostpump = 21
GPIO.setup(plantpump, GPIO.OUT)
GPIO.setup(plantpumsensor, GPIO.IN)
GPIO.setup(compostpump, GPIO.OUT)
GPIO.output(plantpump, GPIO.LOW)
GPIO.output(compostpump, GPIO.LOW)

#Do a coupole triggers to catch sensor
dht22.trigger()
sleep(3)
dht22.trigger()


#1 hour
sleepTime = 3600



def readDHT22():
    #Get a new reading
    dht22.trigger()
    #Save our values
    humidity = '%.2f' % (dht22.humidity())
    temp = '%.2f' % (dht22.temperature())
    return (humidity, temp)

while True:
    #main loop
        i = 0
    #temp and humidity loop
        humidity, temperature = readDHT22()
        tempc = float(temperature)
        tempf = float(tempc * (9/5)+32)
        print (humidity, "%")
        print (tempf, "F")
        
        if tempf < 65:
            GPIO.output(waterheat, GPIO.HIGH)
            print("water heater on")
        else:
            GPIO.output(waterheat, GPIO.LOW)
            print("water heater off")
            
    #light sensor loop
        #if GPIO.input(lightsensor) == 0:
        #    GPIO.output(lightrelay, GPIO.HIGH)
        #else:
        #    GPIO.output(lightrelay, GPIO.LOW)
            
    #Compost water light water 2 times a day for 1 min
        if i % 12 == 0:
            GPIO.output(compostpump, GPIO.HIGH)
            time.sleep(60)
            print("compost watering")
            GPIO.output(compostpump, GPIO.LOW)
        else:
            GPIO.output(compostpump, GPIO.LOW)

    # plant water once every 3 days heavy for 30 min (sprinkler?)
        if i % 72 == 0:
            if plantpumsensor < 20:
                GPIO.output(plantpump, GPIO.HIGH)
                time.sleep(1800)
                print("plants watered")
                GPIO.output(plantpump, GPIO.LOW)
            else
                GPIO.output(plantpump, GPIO.LOW)
        else:
            GPIO.output(plantpump, GPIO.LOW)

            
    # add and print counter   
        i = i + 1
        print("counter =", i)
        
    # print local time   
        localtime = time.localtime()
        result = time.strftime("%I:%M:%S %p", localtime)
        print(result)
        
        sleep(sleepTime)


