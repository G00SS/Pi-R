#!/usr/bin/python
# -*- coding:Utf-8 -*-

import RPi.GPIO as GPIO
import time
import socket
import sys

HOST = "0.0.0.0"
PORT = 12345

#-------------[ CABLAGE ]--------------------
#My_LED = 7

Moteur_1_Forward = 3
Moteur_1_Reverse = 5
Moteur_2_Forward = 8
Moteur_2_Reverse = 10

#phare = 11
#LED_V = 27
#LED_B = 17

#-------------[ Initialisation ]--------------
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(Moteur_1_Forward, GPIO.OUT)
GPIO.setup(Moteur_1_Reverse, GPIO.OUT)
GPIO.setup(Moteur_2_Forward, GPIO.OUT)
GPIO.setup(Moteur_2_Reverse, GPIO.OUT)

#GPIO.setup(phare, GPIO.OUT)
#GPIO.setup(LED_V, GPIO.OUT)
#GPIO.setup(LED_B, GPIO.OUT)

#--------------------------------------------
def AVANT() :
    print "Marche Avant"
    GPIO.output(Moteur_1_Forward, GPIO.HIGH)
    GPIO.output(Moteur_2_Forward, GPIO.HIGH)

def ARRIERE() :
    print "Marche Arriere"
    GPIO.output(Moteur_1_Reverse, GPIO.HIGH)
    GPIO.output(Moteur_2_Reverse, GPIO.HIGH)
    time.sleep(0.5)
    STOP()

def DROITE() :
    print "tourne a droite"
    GPIO.output(Moteur_1_Forward, GPIO.HIGH)
    GPIO.output(Moteur_2_Reverse, GPIO.HIGH)
    time.sleep(0.25)
    STOP()

def DROITE_Toute() :
    print "tourne a droite"
    GPIO.output(Moteur_1_Forward, GPIO.HIGH)
    GPIO.output(Moteur_2_Reverse, GPIO.HIGH)

def GAUCHE() :
    print "tourne a gauche"
    GPIO.output(Moteur_1_Reverse, GPIO.HIGH)
    GPIO.output(Moteur_2_Forward, GPIO.HIGH)
    time.sleep(0.25)
    STOP()

def GAUCHE_Toute() :
    print "tourne a gauche"
    GPIO.output(Moteur_1_Reverse, GPIO.HIGH)
    GPIO.output(Moteur_2_Forward, GPIO.HIGH)


def STOP () :
    print "stop"
    GPIO.output(Moteur_1_Forward, GPIO.LOW)
    GPIO.output(Moteur_2_Forward, GPIO.LOW)
    GPIO.output(Moteur_1_Reverse, GPIO.LOW)
    GPIO.output(Moteur_2_Reverse, GPIO.LOW)

def phare_UP() :
    print "Les phares sont allumés"
    GPIO.output(phare, GPIO.HIGH)
def LED_V_UP() :
    print "LED Vert Marche"
    GPIO.output(LED_V, GPIO.HIGH)
def LED_B_UP() :
    print "LED Bleu Marche"
    GPIO.output(LED_B, GPIO.HIGH)
#def phare_DOWN() :
#    print "Les phares sont éteints"
#    GPIO.output(phare, GPIO.LOW)
#   GPIO.output(LED_V, GPIO.LOW)
#   GPIO.output(LED_B, GPIO.LOW)

def MENU() :
    connexion.send( "\n\r" )
    connexion.send( "  A  --> en Avant\n" )
    connexion.send( "  R  --> en Arriere\n" )
    connexion.send( "  D  --> a Droite\n" )
    connexion.send( "  DD --> a Droite (sans stop)\n" )
    connexion.send( "  G  --> a Gauche\n" )
    connexion.send( "  GG --> a Gauche (sans stop)\n" )
    connexion.send( "  S  --> STOP\n" )
    connexion.send( "  1  --> Allumer les phares\n" )
    connexion.send( "  2  --> LED Vert ON\n" )
    connexion.send( "  3  --> LED Bleu ON\n" )
    connexion.send( "  0  --> Eteindre les phares\n" )
    connexion.send( "  M  --> MENU\n" )
    connexion.send( "\n" )

print "Pi-R attend les ordres !\n"
print "Start\n"

# Creation du socket
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Liaison du socket avec l'interface
try:
   mySocket.bind((HOST, PORT))
except socket.error:
   print "La liaison du socket à l'adresse choisie a échoué."
   sys.exit()

# --------------------------------------
while 1:

   print "Serveur en attente ..."
   mySocket.listen(5)

   # Etablissement de la connexion :
   connexion, adresse = mySocket.accept()
   print "Client connecté, adresse IP %s, port %s" % (adresse[0], adresse[1])

   # Envoi d'un message qu client :
   connexion.send("\nPi-R control server\n\n")
   MENU()

   # Reception des message client
   while 1:
      msgClient = connexion.recv(10).strip()
      print "C>"+msgClient+"<"
      if msgClient.lower() == "fin" or msgClient =="" or msgClient.lower() == "stop":
        print "Break !!!"
        connexion.close()
        break

      elif msgClient.upper() == "M" :
         MENU()

      # Commandes Robot
      elif msgClient == "FORWARD" :
         AVANT()
      elif msgClient == "BACK" :
         ARRIERE()
      elif msgClient == "RIGHT" :
         DROITE()
      elif msgClient == "RI_GHT" :
         DROITE_Toute()
      elif msgClient == "LEFT" :
         GAUCHE()
      elif msgClient == "LE_FT" :
         GAUCHE_Toute()
      elif msgClient == "STOP" :
         STOP()
#      elif msgClient.upper() == "1" :
#         phare_UP()
#      elif msgClient.upper() == "2" :
#         LED_V_UP()
#      elif msgClient.upper() == "3" :
#         LED_B_UP()
#      elif msgClient.upper() == "0" :
#         phare_DOWN()


   # Fin de la session
   connexion.send("Tu t'es bien amusé ? Au revoir et à bientôt !")
   print "Connexion interrompue, fin du test"
   connexion.close()

   # fin du programme
   if msgClient.lower() == "stop":
      break
