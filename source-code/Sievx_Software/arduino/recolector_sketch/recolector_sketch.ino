#include <Servo.h>

//Pines de Conexion.
const int pinSensorEtanol = A0;   
const int pinReleMotor = 8;       
const int pinServo1 = 9; 
const int pinServo2 = 10; 

Servo servo1;
Servo servo2;

int valorEtanol = 0;
String comando = "";
const int CERRADA = 0; 
const int ABIERTA = 120; 

void setup() {
  Serial.begin(9600);
  
  pinMode(pinReleMotor, OUTPUT);
  digitalWrite(pinReleMotor, HIGH); //Apagado inicial (High por rele comun).

  servo1.attach(pinServo1);
  servo2.attach(pinServo2);
  
  //Posición inicial de vigilancia.
  servo1.write(ABIERTA);
  servo2.write(ABIERTA);

  delay(1000);
  Serial.println("ARDUINO_LISTO");
}

void loop() {
  //Lectura y envio constante.
  valorEtanol = analogRead(pinSensorEtanol);
  Serial.print("SENSOR:");
  Serial.println(valorEtanol);

  //Escucha de comandos desde Python.
  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      procesarComando(comando);
      comando = "";
    } else {
      comando += c;
    }
  }
  delay(2000); //Frecuencia de muestreo.
}

void procesarComando(String cmd) {
  cmd.trim();
  if (cmd == "ACTIVAR_MOTOR") {
    digitalWrite(pinReleMotor, LOW); 
  } else if (cmd == "APAGAR_MOTOR") {
    digitalWrite(pinReleMotor, HIGH);
  } else if (cmd == "CERRAR_COMPUERTAS") {
    servo1.write(CERRADA);
    servo2.write(CERRADA);
  } else if (cmd == "ABRIR_COMPUERTAS") {
    servo1.write(ABIERTA);
    servo2.write(ABIERTA);
  }
}