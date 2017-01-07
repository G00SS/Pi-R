#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Test des 3 LED du tableau d'activités

import RPi.GPIO as GPIO		# bibliothèque pour utiliser les GPIO
import time 			# bibliothèque pour gestion du temps

#-------------[ CABLAGE ]--------------------
# Témoin connexion au WLAN1
LAN = 31
# Témoin activation du service de streaming
STREAM = 33
# Témoin activation de l'Acces Point Wifi (WLAN0)
AP = 35


#-------------[ Initialisation ]--------------
GPIO.setmode(GPIO.BOARD) 	# mode de numérotation des pins
GPIO.setwarnings(False) # disable warnings

GPIO.setup(LAN,GPIO.OUT) 	# la pin 31 réglée en sortie (output)
GPIO.setup(STREAM,GPIO.OUT) 	# la pin 33 réglée en sortie (output)
GPIO.setup(AP,GPIO.OUT) 	# la pin 35 réglée en sortie (output)


#--------------------------------------------
while True: 			# boucle répétée jusqu'à l'interruption du programme
	GPIO.output(AP,GPIO.HIGH) 	# sortie au niveau logique haut (3.3 V)
	time.sleep(1) 			# on ne change rien pendant 1 seconde
	GPIO.output(LAN,GPIO.HIGH) 	# sortie au niveau logique haut (3.3 V)
	time.sleep(1) 			# on ne change rien pendant 1 seconde
	GPIO.output(STREAM,GPIO.HIGH) 	# sortie au niveau logique haut (3.3 V)
	time.sleep(2) 			# on ne change rien pendant 2 secondes
	GPIO.output(LAN,GPIO.LOW) 	# sortie au niveau logique bas (0 V)
	time.sleep(1) 			# on ne change rien pendant 1 seconde
	GPIO.output(STREAM,GPIO.LOW) 	# sortie au niveau logique bas (0 V)
	time.sleep(1) 			# on ne change rien pendant 1 seconde
	GPIO.output(AP,GPIO.LOW) 	# sortie au niveau logique bas (0 V)
	time.sleep(2) 			# on ne change rien pendant 2 secondes

