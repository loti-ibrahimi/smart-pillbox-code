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
            time.sleep(10) # sleep 10 seconds.

            # Schedule Met
            grove_rgb_lcd.setRGB(0,255,0)
            grove_rgb_lcd.setText("**** ALERT ****\nSchedule Met")
            time.sleep(5)

            # Schedule Alert
            grove_rgb_lcd.setRGB(255,255,255)
            grove_rgb_lcd.setText('Please Check\nPill Compartment')
            time.sleep(10)

            # Schedule Details
            pillType = 'pill_A'
            pillQuantity = 2
            lcd_string = 'Pill: '+ pillType +'\nQuantity: '+ str(pillQuantity)
            grove_rgb_lcd.setText(lcd_string)
            time.sleep(10)

            # Checking schedules.
            grove_rgb_lcd.setRGB(255,183,41)
            grove_rgb_lcd.setText("* Pillbox Open *\nNo Schedule Met")
            time.sleep(10) # sleep 10 seconds.

    except KeyboardInterrupt as e:
            # since we're exiting the program
            # it's better to leave the LCD with a blank text
            grove_rgb_lcd.setRGB(255,255,255) 
            grove_rgb_lcd.setText("Bye now.")
            break