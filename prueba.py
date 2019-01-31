#importacion de librerias
import requests as rq #obtener datos de una pagina web
import pymysql #comunicacion con la DB
import RPi.GPIO as GPIO #utilizacion de pines de la RPi
from bs4 import BeautifulSoup as bs #analisis de HTML
import time #tiempo

GPIO.setmode(GPIO.BCM) #se selecciona el modo de identificacion del pin de la RPi
GPIO.setwarnings(False) #deshabilitando las advertencias
GPIO.setup(17, GPIO.OUT) #se configura distintos pines como salida
GPIO.output(17, GPIO.LOW)
GPIO.setup(27, GPIO.OUT)
GPIO.output(27, GPIO.LOW)
GPIO.setup(22, GPIO.OUT)
GPIO.output(22, GPIO.LOW)
GPIO.setup(6, GPIO.OUT)
GPIO.output(6, GPIO.LOW)
GPIO.setup(13, GPIO.OUT)
GPIO.output(13, GPIO.LOW)

tiempo_muestreo = 0 #segundos
while True:
    while tiempo_muestreo<1: #tiempo en segundos, la pagina actualiza el valor cada 5 minutos
        tiempo_muestreo+=1
        time.sleep(1)

    pet = rq.get("http://gye.exa.ec/Current.htm")
    page = bs(pet.content,"html.parser")
    indice = 0.0
    for el in page.select("small"):
        if "index" in el.text:
            info=el.text.split()
            indice = round((float)(info[0])) #VALOR DEL INDICE UV
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
    if indice >= 0 and indice <= 2: #nivel bajo
        GPIO.output(17, GPIO.HIGH) #se da el valor de 1 logico a la salida para encender el led
        print("Nivel bajo")
        time.sleep(53) #se espera 58 segundos
        GPIO.output(17, GPIO.LOW) #se apaga el led
    if indice >= 3 and indice <= 5: #nivel moderado
        GPIO.output(27, GPIO.HIGH)
        print("Nivel moderado")
        time.sleep(53)
        GPIO.output(27, GPIO.LOW)
    if indice >= 6 and indice <= 7:   #nivel alto
        GPIO.output(22, GPIO.HIGH)
        print("Nivel alto")
        time.sleep(53)
        GPIO.output(22, GPIO.LOW)
    if indice >= 8 and indice <= 10: #nivel muy alto
        GPIO.output(6, GPIO.HIGH)
        print("Nivel muy alto")        
        time.sleep(53)
        GPIO.output(6, GPIO.LOW)
    if indice>=11: #nivel extremadamente alto
        GPIO.output(13, GPIO.HIGH)
        print("Nivel extremadamente alto")        
        time.sleep(53)
        GPIO.output(13, GPIO.LOW)
    break