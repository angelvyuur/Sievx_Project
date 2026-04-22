@echo off
cd /d "%~dp0"
title Sistema Sievx Software

echo [1/2] Iniciando Motor de Comunicacion (Python)...
:: Se abrio Python en una nueva ventana.
start /min python "..\\python\\recolector_script.py"

echo [2/2] Abriendo Interfaz de Control (Access)...
:: Se abrio la base de datos de Access.
start "" "..\\access\\db-recolector.accdb"

echo.
echo Sistema iniciado correctamente
timeout /t 8
exit