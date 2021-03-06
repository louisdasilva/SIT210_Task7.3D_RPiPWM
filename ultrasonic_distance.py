# REFERENCES:
# Code adapted and modified from:
# Ultrasonic Sensor: https://tutorials-raspberrypi.com/raspberry-pi-ultrasonic-sensor-hc-sr04/
# PWM functionality: https://www.electronicwings.com/raspberry-pi/raspberry-pi-pwm-generation-using-python-and-c

import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)
 
#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO_LED = 12
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_LED, GPIO.OUT)
LED_pwm = GPIO.PWM(GPIO_LED, 1000)
LED_pwm.start(0)
 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
 
if __name__ == '__main__':
    try:
        while True:
            dist = distance()
            led_brightness = 50 - dist # The led will start to brighten once an object is within 50cm
            led_duty_cycle = led_brightness / 50 * 100 # get the distance of object as a percentage
            if(led_duty_cycle >= 0 and led_duty_cycle <= 100): # the sensor can read much further, we want to filter out anything further
                LED_pwm.ChangeDutyCycle(led_duty_cycle)
            else: # anything further than 50cm will give percentage outside of 0 - 100%, ignore it and switch LED off
                LED_pwm.ChangeDutyCycle(0)
            print ("Measured Distance = %.1f cm" % dist)
            print ("Duty Cycle = ", led_duty_cycle)
            time.sleep(1)
 
        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()