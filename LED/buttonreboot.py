#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import subprocess
from time import sleep

#-------------[ CABLAGE ]--------------------
# Switch connecté entre GPIO 17 (pin 11) et GND
SWITCH = 11

# LED connectée entre GPIO 18 (pin 12) et GND
LED = 12


#-------------[ Initialisation ]--------------
GPIO.setmode(GPIO.BOARD) # on met RPi.GPIO en mode notation BCM
GPIO.setwarnings(False) # disable warnings

# on initialise le GPIO 17 en mode entrée
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED,GPIO.OUT)
GPIO.output(LED,GPIO.LOW) # LED éteint

# On définit nos durées
long_press = 1
very_long_press = 4

# fonction arrêt du Pi
def shutdown():
    subprocess.call(['sudo shutdown -h now "Arrêt du système par bouton GPIO" &'], shell=True)

# fonction reboot du Pi
def reboot():
    subprocess.call(['sudo reboot "Reboot du système par bouton GPIO" &'], shell=True)

#--------------------------------------------
# notre fonction de gestion du bouton
def system_button(SWITCH):
    # cette variable servira a stocker le temps d'enfoncement du switch
    button_press_timer = 0

    while True:
      if (GPIO.input(SWITCH) == False) : # le bouton est enfoncé
	button_press_timer += 0.2 # ... on enregistre le temps que cela dure
        if (button_press_timer > very_long_press) :
	   GPIO.output(LED,GPIO.HIGH)   # Annonce le shutdown
           print "very long press : ", button_press_timer
           shutdown()
           
        elif (button_press_timer > long_press):
	   print "Reboot armed : ", button_press_timer
           GPIO.output(LED,GPIO.LOW)   # Informe reboot armé
        else:  # Traite le premier allumage
	  GPIO.output(LED,GPIO.HIGH)

      else: # le bouton a été relâché, on compte combien de temps cela a dure
	GPIO.output(LED,GPIO.LOW)
        if (button_press_timer > very_long_press):
           print "very long press : ", button_press_timer
           shutdown()

        elif (button_press_timer > long_press):
	   print "long press : ", button_press_timer
           reboot()

        elif (button_press_timer > 0.2):
	   print "short press : ", button_press_timer
	   # do nothing

        button_press_timer = 0
        GPIO.output(LED,GPIO.LOW)
      # on attend 0.2 secondes avant la boucle suivante afin de réduire la charge sur le CPU
      sleep(0.2)


#--------------------------------------------	  

# on met le bouton en écoute par interruption, détection falling edge sur le canal choisi, et un débounce de 200 millisecondes
GPIO.add_event_detect(SWITCH, GPIO.FALLING, callback=system_button, bouncetime=200)

# ici vous pouvez mettre du code qui sera exécuté normalement, sans influence de la fonction bouton
try:
    while True:
        # faites ce qui vous plaît
        sleep (2)

# on réinitialise en entrée les ports GPIO utilisés en sortie de script
# NB: ce script n'est pas sensé se terminer avant que le buzzer ait fait son oeuvre.
except KeyboardInterrupt:
    GPIO.cleanup()  # reinitialisation GPIO lors d'une sortie CTRL+C
GPIO.cleanup()      # reinitialisation GPIO lors d'une sortie normale
