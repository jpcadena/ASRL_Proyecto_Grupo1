#importacion de librerias
import requests as rq #obtener datos de una pagina web
import pymysql #comunicacion con la DB
import RPi.GPIO as GPIO #utilizacion de pines de la RPi
from bs4 import BeautifulSoup as bs #analisis de HTML
import time #tiempo
import math

GPIO.setmode(GPIO.BCM) #se selecciona el modo de identificacion del pin de la RPi
GPIO.setwarnings(False) #deshabilitando las advertencias
GPIO.setup(17, GPIO.OUT) #se configura distintos pines como salida
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)

tiempo_muestreo = 0 #segundos
while True:
    while tiempo_muestreo<1: #tiempo en segundos, la pagina actualiza el valor cada 5 minutos. se coloco 1 segundo para agilitar el proceso
        tiempo_muestreo+=1
        time.sleep(1) #espera de 1 segundo
    #web scraping. dura alrededor de 6 segundos, dependiendo de la conexion a Internet y la velocidad de ejecucion de este proceso
    pet = rq.get("http://gye.exa.ec/Current.htm")
    page = bs(pet.content,"html.parser")
    indice = 0.0
    for el in page.select("small"):
        if "index" in el.text:
            info=el.text.split()
            indice = math.floor((float)(info[0])) #VALOR DEL INDICE UV
            break
    print("El indice UV es:", indice)
    tiempo_muestreo = 0

    #se establece conexion con los datos proporcionados de la DB, usuario y contrasena
    mySQLconnection = pymysql.connect(host='localhost',
                             database='proyecto',
                             user='jpcadena',
                             password='root1234')

    cursor = mySQLconnection.cursor() #se genera un cursor
    #se realiza una actualizacion en el campo UV de la ultima fila de la tabla valores
    sql_update_query = "UPDATE valores SET UV=%s ORDER BY id DESC LIMIT 1"
    cursor = mySQLconnection.cursor()
    cursor.execute(sql_update_query, indice)
    mySQLconnection.commit() #cuando se altera la tabla se debe realizar un commit
    cursor.close()
    mySQLconnection.close()

    #condicionales para el rango del indice UV
    if indice >= 0 and indice <= 2: #nivel bajo con led verde
        GPIO.output(27, GPIO.LOW) #se apagan los otros leds por si el proceso ya se ha realizado anteriormente
        GPIO.output(22, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(17, GPIO.HIGH) #se da el valor de 1 logico a la salida para encender el led
        print("Nivel bajo")
        time.sleep(53) #se espera 53 segundos
    if indice >= 3 and indice <= 5: #nivel moderado con led amarillo
        GPIO.output(17, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(27, GPIO.HIGH)
        print("Nivel moderado")
        time.sleep(53)
    if indice >= 6 and indice <= 7:   #nivel alto con led naranja
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(22, GPIO.HIGH)
        print("Nivel alto")
        time.sleep(53)
    if indice >= 8 and indice <= 10: #nivel muy alto con led rojo
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(13, GPIO.LOW)
        GPIO.output(6, GPIO.HIGH)
        print("Nivel muy alto")
        time.sleep(53)
    if indice>=11: #nivel extremadamente alto con ledo azul que representa al morado
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
        GPIO.output(22, GPIO.LOW)
        GPIO.output(6, GPIO.LOW)
        GPIO.output(13, GPIO.HIGH)
        print("Nivel extremadamente alto")
        time.sleep(53)
