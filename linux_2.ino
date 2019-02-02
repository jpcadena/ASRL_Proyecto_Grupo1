/*Script para enviar datos del sensor DHT11 desde Arduino Uno mediante el uso del modulo Wifi ESP8266*/
/* Se importan las librerias del sensor y software serial para el uso del modulo WiFi
  Tambien se definen los pines 4, 10 y 11 como constantes y se define el tipo de variable correspondiente al sensor*/
/*Instalar desde el gestor de librerias: DHT by Adafruit e importar por .zip la libreria Adafruit_Sensor*/ 
#include "DHT.h"
#include "SoftwareSerial.h"
#define RX 10
#define TX 11
#define DHTPIN 4
#define DHTTYPE DHT11
 
/*Inicializamos el sensor DHT11*/
DHT dht(DHTPIN, DHTTYPE);

/*se generan las variables referentes a la red ad-hoc y su clave con el nombre del servidor*/
String ssid = ""; /*nombre de la red*/
String password = ""; /*contraseña de la red*/
String host = ""; /*direccion ip del servidor q aloja la base de datos dentro de la misma red*/
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
  dht.begin();
  wifi.begin(9600);
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
  String url = "/proyecto.php"; /*nombre del php alojado en el servidor q ingresa y muestra los datos  en la pagina web*/
  String dato1 = "?Temperatura=";
  String dato2 = "&Humedad=";
  String dato3 = "&UV=";
  // Leemos la humedad relativa
  float hum = dht.readHumidity();
  // Leemos la temperatura en grados centígrados
  float temp = dht.readTemperature();
  // Comprobamos si ha habido algún error en la lectura
  if (isnan(hum) || isnan(temp)) {
    Serial.println("Error obteniendo los datos del sensor DHT11");
    return;
  }
  Serial.print("Temperatura: ");
  Serial.print(temp);
  Serial.print(" Humedad: ");
  Serial.print(hum);
  Serial.println(); 
  delay(15000);  
  
  /* Subiendo datos cada 15 segundos*/
  if (currentMillis - previousMillis >= interval){
    previousMillis = currentMillis;
    String getData = "GET " + url + dato1 + temp + dato2 + hum + dato3 + indice + " HTTP/1.1\r\n" +
               "Host: " + host + "\r\n" +
               "Connection: close\r\n\r\n";
    sendCommand("AT+CIPMUX=1",5,"OK");
    sendCommand("AT+CIPSTART=0,\"TCP\",\""+ host +"\","+ 80,15,"OK");
    sendCommand("AT+CIPSEND=0," +String(getData.length()+0),4,">");
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
    if(wifi.find(readReplay))
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
