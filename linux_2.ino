/*Script para enviar datos del sensor DHT11 desde Arduino Uno mediante el uso del modulo Wifi ESP8266*/
/* Se importan las librerias del sensor y del modulo WiFi
  Tambien se definen los pines 10, 11 como constantes*/
#include <DHT11.h>
//#include <ESP8266WiFi.h>
#include "SoftwareSerial.h"
#define RX 10
#define TX 11

/* se asigna la variable del sensor como salida al pin digital D4*/
DHT11 dht11(4);

/*se generan las variables referentes a la red ad-hoc y su clave con el nombre del servidor*/
String ssid = "Free.Wifi"; //Free.Wifi
String password = "cafecito24"; //cafecito24
String host = "192.168.43.45"; //192.168.43.45
int countTrueCommand, countTimeCommand;
boolean found = false;
unsigned long previousMillis = 0;
const long interval = 16000;

/*se establece conexion mediante comandos AT del ESP8266*/
SoftwareSerial wifi(RX,TX); 
void sendCommand(String command, int maxTime, char readReplay[]);
void setup()
{
  Serial.begin(9600);
  wifi.begin(9600);
  /*wifi.println("AT");
  delay(1000);
  wifi.println("AT+CWMODE=1");
  delay(1000);
  wifi.println("AT+CWJAP=\"Free.Wifi\",\"cafecito24\"");
  delay(5000);*/
  sendCommand("AT",5,"OK");
  sendCommand("AT+CWMODE=1",5,"OK");
  sendCommand("AT+CWJAP=\""+ ssid +"\",\""+ password +"\"",20,"OK");
}

void loop()
{
 /*se declaran las variables de interes para calculos posteriores*/
  unsigned long currentMillis = millis();
  int err;
  int indice = 0;
  float temp, hum;
  String url = "/proyecto.php";
  String dato1 = "?Temperatura=";
  String dato2 = "&Humedad=";
  String dato3 = "&UV=";
  if ((err = dht11.read(hum, temp)) == 0)
  {
    Serial.print("Temperatura: ");
    Serial.print(temp);
    Serial.print(" Humedad: ");
    Serial.print(hum);
    Serial.println();
  }
  delay(1000);
  
  /* Subiendo datos cada 60 segundos*/
  if (currentMillis - previousMillis >= interval){
    previousMillis = currentMillis;
    String getData = "GET " + url + dato1 + temp + dato2 + hum + dato3 + indice + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n";
    sendCommand("AT+CIPMUX=1",5,"OK");
    sendCommand("AT+CIPSTART=0,\"TCP\",\""+ host +"\","+ 80,15,"OK");
    sendCommand("AT+CIPSEND=0," +String(getData.length()+11),4,">");
    wifi.println(getData);
    countTrueCommand++;
    sendCommand("AT+CIPCLOSE=0",5,"OK");
  }
}

// Envío de comandos al módulo WIFI
void sendCommand(String command, int maxTime, char readReplay[]){
  Serial.print(countTrueCommand);
  Serial.print(". at command => ");
  Serial.print(command);
  Serial.print(" ");
  while(countTimeCommand < (maxTime*1))
  {
    wifi.println(command);//at+cipsend
    delay(1000);
    if(wifi.find(readReplay))//ok
    {
      found = true;
      break;
    }  
    countTimeCommand++;
  }  
  if(found == true)
  {
    Serial.println("OYI");
    countTrueCommand++;
    countTimeCommand = 0;
  }  
  if(found == false)
  {
    Serial.println("Fail");
    countTrueCommand = 0;
    countTimeCommand = 0;
  }  
  found = false;
}
