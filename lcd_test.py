#!/usr/bin/python3

'''
Author: Loti Ibrahimi (20015453)
Course: BSc (Hons) in the Internet of Things.

Script Overview:
* Sim[ply testing LCD different event displays.
'''

import time
import grove_rgb_lcd

while True:
    try:
            # Checking schedules.
            grove_rgb_lcd.setRGB(100,255,255)
            grove_rgb_lcd.setText("Checking \n schedules..")
            time.sleep(10) # sleep 60 seconds.

            # Schedule Met
            grove_rgb_lcd.setText("**** ALERT ****\nSchedule Met")
            grove_rgb_lcd.setRGB(0,255,0)
            time.sleep(5)

            # Schedule Alert
            grove_rgb_lcd.setRGB(255,255,255)
            grove_rgb_lcd.setText('Pill Compartment\nhas been lit.')
            time.sleep(10)
            pillType = 'pill_A'
            pillQuantity = 2
            lcd_string = 'Pill: '+ pillType +'\nQuantity: '+ str(pillQuantity)
            # Schedule Details
            grove_rgb_lcd.setText(lcd_string)
            time.sleep(10)

    except KeyboardInterrupt as e:
            # since we're exiting the program
            # it's better to leave the LCD with a blank text
            grove_rgb_lcd.setRGB(255,255,255) 
            grove_rgb_lcd.setText("Bye now.")
            break