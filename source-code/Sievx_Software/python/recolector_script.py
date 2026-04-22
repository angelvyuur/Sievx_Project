import serial
import pyodbc
import time
from datetime import datetime
import os
import sys

#Enrutamiento dinamico
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
RUTA_DB_ACCESS = os.path.join(ROOT_DIR, 'access', 'db-recolector.accdb')
RUTA_REPORTES = os.path.join(ROOT_DIR, 'reportes')
RUTA_ARCHIVO_COMANDO_ACCESS = os.path.join(ROOT_DIR, 'python', 'lectura_access', 'comando_access.txt')

#Hardware configuracion
PUERTO_SERIAL_ARDUINO = 'COM3' 
BAUDIOS = 9600
UMBRAL_ETANOL = 170

def mostrar_bienvenida():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Sievx Software")
    print(" ")
    print("Version de compilacion:")
    print("Version 1.0")
    print(" ")
    print("MODULO DE EXTRACCION AUTOMATIZADA CON GESTION DE SEGURIDAD MEDIANTE HMI Y BASE DE DATOS RELACIONAL PARA ESTACIONES DE ENSENANZA TECNICA V1.0")
    print(" ")
    print("__________")
    print(" ")
    print("\nInstrucciones de uso:")
    print("- No desconecte el Arduino mientras el sistema corre.")
    print("- La base de datos de Access se abrira automaticamente en un momento.")
    print("- Al finalizar sesión, debe cerrar esta ventana para poder iniciar el sistema nuevamente.")
    print("\nCredenciales de acceso:")
    print("AdminGlobal; 123456 [Nivel 1]")
    print("Operador; 654321 [Nivel 2]")
    print("Consultor; 444444 [Nivel 3]")
    print(" ")
    print("Elementos físicos:")
    print("Arduino UNO o similar")
    print("Sensor MQ adecuado a la emisión a revisar")
    print("Motor con ventilador DC 9-12V")
    print("Fuente externa de alimentacion DC 9-12V")
    print("Relevador DC 5V")
    print("Comunicacion y alimentacion entre PC y Arduino")
    print("Dos servo motores PWM")
    print(" ")
    print("Elementos de programa:")
    print("Sievx Software")
    print(" ")
    print("----------")
    print("Requisitos:")
    print("Sievx Software")
    print("Access")
    print("Python")
    print("Arduino IDE")
    print("Módulo")
    print("----------")

def enviar_comando_arduino(comando, ser):
    try:
        if ser.is_open:
            ser.write(f"{comando}\n".encode('utf-8'))
    except Exception as e:
        print(f"Error Serial: {e}")

def generar_reporte_txt(tipo, valor):
    if not os.path.exists(RUTA_REPORTES): os.makedirs(RUTA_REPORTES)
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    ruta = os.path.join(RUTA_REPORTES, f"Reporte_{fecha}.txt")
    with open(ruta, 'w') as f:
        f.write(f"EVENTO: {tipo}\nFECHA: {fecha}\nVALOR: {valor}\nUMBRAL: {UMBRAL_ETANOL}")

#Logica central
mostrar_bienvenida()

try:
    #Comunicacion serial
    ser = serial.Serial(PUERTO_SERIAL_ARDUINO, BAUDIOS, timeout=1)
    time.sleep(2)
    
    #Comunicacion con Access
    conn_str = f"DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={RUTA_DB_ACCESS};"
    cnxn = pyodbc.connect(conn_str)
    cursor = cnxn.cursor()
    
    print("[Bien] Arduino detectado en " + PUERTO_SERIAL_ARDUINO)
    print("[Bien] Base de Datos conectada.")
    print("\nSISTEMA EN EJECUCION - MONITOREANDO SENSOR...")

    estado_actual = 0 # 0 = Vigilancia; 1 = Succion

    while True:
        if ser.in_waiting > 0:
            linea = ser.readline().decode('utf-8', errors='ignore').strip()
            if linea.startswith("SENSOR:"):
                try:
                    valor = int(linea.split(":")[1])
                    cursor.execute("INSERT INTO LecturasEtanol (FechaHora, Valor) VALUES (?, ?)", datetime.now(), valor)
                    cnxn.commit()

                    #Control automatico
                    if estado_actual == 0 and valor >= UMBRAL_ETANOL:
                        enviar_comando_arduino("ACTIVAR_MOTOR", ser)
                        enviar_comando_arduino("CERRAR_COMPUERTAS", ser)
                        estado_actual = 1
                        generar_reporte_txt("SUCCION_INICIADA", valor)
                    
                    elif estado_actual == 1 and valor < UMBRAL_ETANOL:
                        enviar_comando_arduino("APAGAR_MOTOR", ser)
                        enviar_comando_arduino("ABRIR_COMPUERTAS", ser)
                        estado_actual = 0
                        generar_reporte_txt("VIGILANCIA_REANUDADA", valor)

                    #Control manual (Access)
                    if os.path.exists(RUTA_ARCHIVO_COMANDO_ACCESS):
                        with open(RUTA_ARCHIVO_COMANDO_ACCESS, 'r+') as f_cmd:
                            cmd = f_cmd.read().strip()
                            if cmd == "ACTIVAR_MOTOR_MANUAL":
                                enviar_comando_arduino("ACTIVAR_MOTOR", ser)
                                enviar_comando_arduino("CERRAR_COMPUERTAS", ser)
                                estado_actual = 1
                            elif cmd == "APAGAR_MOTOR_MANUAL":
                                enviar_comando_arduino("APAGAR_MOTOR", ser)
                                enviar_comando_arduino("ABRIR_COMPUERTAS", ser)
                                estado_actual = 0
                            f_cmd.seek(0)
                            f_cmd.truncate(0)
                except: pass
        time.sleep(0.1)

except Exception as e:
    print("----------")
    print(f"\nHubo un error")
    print(f"Detalles: {e}")
    print("----------")
    print("\nPresione alguna tecla para salir de esta ventana...")
    input()
finally:
    if 'ser' in locals(): ser.close()
    if 'cnxn' in locals(): cnxn.close()