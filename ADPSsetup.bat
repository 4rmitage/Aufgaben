@echo off
REM filepath: c:\Python\Aufgaben-1\ADPSsetup.bat
REM Startet PowerShell als Administrator und führt das ADPSsetup.ps1-Skript aus

set SCRIPT_PATH=%~dp0ADPSsetup.ps1

powershell -Command "Start-Process PowerShell -ArgumentList '-NoProfile -ExecutionPolicy Bypass -File \"%SCRIPT_PATH%\"' -Verb RunAs"