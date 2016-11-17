#!/usr/bin/python
# -*- coding:Utf-8 -*-
 
import RPi.GPIO as GPIO
import time
import socket
import sys
 
HOST = "192.168.1.18"
PORT = 12345
 
#-------------[ CABLAGE ]--------------------
#My_LED = 22
 
Moteur_1_Forward = 38
Moteur_1_Reverse = 40
Moteur_2_Forward = 37
Moteur_2_Reverse = 35
 
#LED_R = 22
#LED_V = 27
#LED_B = 17
 
#-------------[ Initialisation ]--------------
GPIO.setmode(GPIO.BOARD) 
GPIO.setwarnings(False)

GPIO.setup(Moteur_1_Forward, GPIO.OUT)
GPIO.setup(Moteur_1_Reverse, GPIO.OUT)
GPIO.setup(Moteur_2_Forward, GPIO.OUT)
GPIO.setup(Moteur_2_Reverse, GPIO.OUT)
 
#GPIO.setup(LED_R, GPIO.OUT)
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
 
def LED_R_UP() :
    print "LED Rouge Marche"
    GPIO.output(LED_R, GPIO.HIGH)
def LED_V_UP() :
    print "LED Vert Marche"
    GPIO.output(LED_V, GPIO.HIGH)
def LED_B_UP() :
    print "LED Bleu Marche"
    GPIO.output(LED_B, GPIO.HIGH)
def LED_DOWN() :
    print "LED Stop"
    GPIO.output(LED_R, GPIO.LOW)
    GPIO.output(LED_V, GPIO.LOW)
    GPIO.output(LED_B, GPIO.LOW)
 
def MENU() :
    connexion.send( "\n\r" )
    connexion.send( "  A  --> en Avant\n" )
    connexion.send( "  R  --> en Arriere\n" )
    connexion.send( "  D  --> a Droite\n" )
    connexion.send( "  DD --> a Droite (sans stop)\n" )
    connexion.send( "  G  --> a Gauche\n" )
    connexion.send( "  GG --> a Gauche (sans stop)\n" )
    connexion.send( "  S  --> STOP\n" )
    connexion.send( "  1  --> LED Rouge ON\n" )
    connexion.send( "  2  --> LED Vert ON\n" )
    connexion.send( "  3  --> LED Bleu ON\n" )
    connexion.send( "  0  --> LED OFF\n" )
    connexion.send( "  M  --> MENU\n" )
    connexion.send( "\n" )
 
print "GO"
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
      msgClient = connexion.recv(10).rstrip()
      print "C>"+msgClient+"<"
      if msgClient.lower() == "fin" or msgClient =="" or msgClient.lower() == "stop":
         print "Break !!!"
         break
 
      elif msgClient.upper() == "M" :
         MENU()
 
      # Commandes Robot
      elif msgClient.upper() == "A" :
         AVANT()
      elif msgClient.upper() == "R" :
         ARRIERE()
      elif msgClient.upper() == "D" :
         DROITE()
      elif msgClient.upper() == "DD" :
         DROITE_Toute()
      elif msgClient.upper() == "G" :
         GAUCHE()
      elif msgClient.upper() == "GG" :
         GAUCHE_Toute()
      elif msgClient.upper() == "S" :
         STOP()
      elif msgClient.upper() == "1" :
         LED_R_UP()
      elif msgClient.upper() == "2" :
         LED_V_UP()
      elif msgClient.upper() == "3" :
         LED_B_UP()
      elif msgClient.upper() == "0" :
         LED_DOWN()
 
 
   # Fin de la session
   connexion.send("à bientôt !")
   print "Connexion interrompue."
   connexion.close()
 
   # fin du programme
   if msgClient.lower() == "stop":
      break