;Sievx Software
;Script de instalacion profesional edicion
;Version: 1.0
;Editor: Angel Vyuur

[Setup]
AppId={{1FEC57A0-B287-4C11-9999-EDD5E3BBBF00}
AppName=Sievx Software
AppVersion=1.0
AppPublisher=Angel Vyuur
DefaultDirName={commonpf32}\Sievx Software
DefaultGroupName=Sievx Software
DisableProgramGroupPage=yes
OutputBaseFilename=Sievx_Software-Setup-1.0
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "installpython"; Description: "Instalar dependencias de Python (pyodbc, pyserial)"; GroupDescription: "Tareas adicionales:"; Flags: checkedonce

[Files]
;Direcciones de archivos fuente
Source: "C:\Sievx_Software\bin\lanzador.bat"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "C:\Sievx_Software\access\*"; DestDir: "{app}\access"; Flags: ignoreversion recursesubdirs
Source: "C:\Sievx_Software\python\*"; DestDir: "{app}\python"; Flags: ignoreversion recursesubdirs
Source: "C:\Sievx_Software\arduino\*"; DestDir: "{app}\arduino"; Flags: ignoreversion recursesubdirs
Source: "C:\Sievx_Software\reportes\*"; DestDir: "{app}\reportes"; Flags: ignoreversion recursesubdirs
Source: "C:\Sievx_Software\docs\*"; DestDir: "{app}\docs"; Flags: ignoreversion recursesubdirs

[Icons]
;Acceso directo en el escritorio.
Name: "{autodesktop}\Sievx Software"; Filename: "{app}\bin\lanzador.bat"; IconFilename: "{app}\access\db-recolector.accdb"

[Registry]
;Establecimiento de elevacion de administrador al lanzar.
Root: "HKLM"; Subkey: "Software\Microsoft\Windows NT\CurrentVersion\AppCompatFlags\Layers"; ValueType: String; ValueName: "{app}\bin\lanzador.bat"; ValueData: "~ RUNASADMIN"; Flags: uninsdeletevalue

[Run]
;Casillas opcionales.
Filename: "{cmd}"; Parameters: "/c python -m pip install pyodbc pyserial"; StatusMsg: "Instalando dependencias (pyodbc, pyserial)..."; Tasks: installpython; Flags: runhidden
Filename: "{app}\bin\lanzador.bat"; Description: "Ejecutar Sievx Software"; Flags: postinstall shellexec skipifsilent