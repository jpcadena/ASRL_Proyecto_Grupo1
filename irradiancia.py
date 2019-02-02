"""#importacion de librerias numpy para funciones matematicas
import numpy as np
from sympy import Integral, integrate

x = symbol('x')

#se establece conexion con los datos proporcionados de la DB, usuario y contrasena
mySQLconnection = mysql.connector.connect(host='localhost',
                         database='proyecto',
                         user='jpcadena',
                         password='root1234')
#extra es la irradiancia solar global a la longitud de la onda lambda a nivel de la superficie ##aqui deberia ser la potencia a partir de la
sql_select_Query1 = "select VoltajeA0 from valores order by id DESC limit 1" #se realiza una consulta al campo Voltaje proveniente del pin A0 en la tabla Valores de la DB proyecto
sql_select_Query2 = "select VoltajeA1 from valores order by id DESC limit 1" #se realiza una consulta al campo Voltaje proveniente del pin A1 en la tabla Valores de la DB proyecto
cursor = mySQLconnection.cursor() #se genera un cursor
cursor.execute(sql_select_Query1) #se ejecuta la sentencia de consulta
#se obtiene el valor de la variable deseada de la base de datos y se lo almacena en una variable local de python
VoltajePanel = cursor.fetchone()[0]
cursor = mySQLconnection.cursor()
cursor.execute(sql_select_Query2)
VoltajeResistencia = cursor.fetchone()[0]

#Primero se halla la corriente por el resistor a partir de I=V/R donde V es VoltajeResistencia y R la resistencia conocida de 1000 KOhms
#VoltajeResistencia = VoltajePanel - VoltajeRef
Intensidad = VoltajeResistencia/100000

#Ahora se obtiene la potencia mediante P=V*I donde V es VoltajePanel e I es Intensidad calculada anteriormente
Potencia = VoltajePanel*Intensidad

#Luego se calcula la irradiancia solar con la ecuacion Ir=P/A donde P es la potencia del panel y A el area del mismo que es 0,015189 m^2
Irradiancia = Potencia/0.015189

#definiendo la variable longitud de onda Lambda como un vector definido para los rayos UV-A y UV-B entre 280 y 400 nm
#l = np.linspace(280e-9, 400e-9)

#Definiendo el coeficiente de accion eritematica como una funcion por partes
elambda1 = 1
elambda2 = np.power(10, 0.094*((298e-9)-x))
elambda3 = np.power(10, 0.015*((139e-9)-x))

#Calculando las integrales por partes de la irradiancia eritematica
Ieritematica1 = Irradiancia*Integral(elambda1, (x, 280e-9, 298e-9))
Ieritematica2 = Irradiancia*Integral(elambda2, (x, 299e-9, 328e-9))
Ieritematica3 = Irradiancia*Integral(elambda3, (x, 329e-9, 400e-9))

#Sumando las 3 integrales
IeritematicaTotal = Ieritematica1 + Ieritematica2 + Ieritematica3

#UV=Ieritematica*ker donde ker es una constante igual a 40 m^2/W 
UV = Ieritematica*40"""