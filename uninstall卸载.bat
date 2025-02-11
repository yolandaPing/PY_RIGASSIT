@echo off

rem Get the "Documents" directory.
FOR /F "tokens=2* delims= " %%A IN ('REG QUERY "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v "Personal"') DO SET Documents=%%B

set INSTALL_DIR=%cd%

echo  ==========================Uninstall PY_RIGASSIT Tool=============================
echo.  
echo  Module uninstall for Autodesk Maya
echo  Name..: PY_RIGASSIT
echo  Author: Yolanda Ping
echo  e-mail: YOLANDAPING1224@GMAIL.COM
echo  Date..: 2024-09-08 : 15 :27
echo.
echo  This version supports Maya Version: 2017,2018,2019,2020,2022,2023,2024
echo.
echo  ==========================Uninstall PY_RIGASSIT Tool=============================
echo.

rem List of Maya versions
set "versions=2017 2018 2019 2020 2022 2023 2024 "

set /p input=" >>> Do you want to uninstall PY_RIGASSIT Tool [" %cd% "] yes/no ?  [ y/n ] :  "
set /p brt_input=" >>> Do you want to uninstall brSmoothWeights Tool [" %cd% "] yes/no ? [ y/n ] :  "

if /i "%input%"=="y" (

    if exist %Documents%\maya\modules\PY_RIGASSIT.mod del %Documents%\maya\modules\PY_RIGASSIT.mod
    for %%V in (%versions%) do (
                    if exist %Documents%\maya\%%V\modules\PY_RIGASSIT.mod del %Documents%\maya\%%V\modules\PY_RIGASSIT.mod
                    if exist %Documents%\maya\%%V\zh_CN\modules\PY_RIGASSIT.mod del %Documents%\maya\%%V\zh_CN\modules\PY_RIGASSIT.mod
                )

    if /i "%brt_input%"=="y" (if exist %Documents%\maya\modules del %Documents%\maya\modules\brSmoothWeights.mod)else (
            echo.
            echo  brSmoothWeights Tool uninstall canceled.
            )

    echo  PY_RIGASSIT Tool unInstalled successfully !

)else (
            echo.
            echo  PY_RIGASSIT Tool uninstall canceled.
            )

pause
