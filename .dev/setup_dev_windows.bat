@echo off
set "_updir=%~dp0"
for %%a in ("%_updir:~0,-1%") do set "_dir=%%~dpa"
mklink /D %HOMEDRIVE%%HOMEPATH%\AppData\Roaming\QGIS\QGIS4\profiles\default\python\plugins\DsgTools %_dir%DsgTools