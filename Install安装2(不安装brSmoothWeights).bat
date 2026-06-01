@echo off
chcp 65001

REM Copyright (c) 2025 Yolanda Ping

rem Get the "Documents" directory.
FOR /F "tokens=2* delims= " %%A IN ('REG QUERY "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v "Personal"') DO SET Documents=%%B

set INSTALL_DIR=%cd%

echo  ==========================Installer PY_RIGASSIT Tool=============================
echo.  
echo  Module installer for Autodesk Maya
echo  Name..: PY_RIGASSIT
echo  Author: Yolanda Ping
echo  e-mail: YOLANDAPING1224@GMAIL.COM
echo  Date..: 2024-09-08 : 15 :27
echo.
echo  This version supports Maya Version: 2017,2018,2019,2020,2022,2023,2024,2025,2026
echo.
echo  RBF supports Maya Version: 2017,2018,2019,2020,2022,2023,2024,2025
echo.
echo  Copyright (c) 2025 Yolanda Ping
echo  ==========================Installer PY_RIGASSIT Tool=============================
echo.


set OUTPUT=%Documents%\maya\modules\PY_RIGASSIT.mod
set BRS_OUTPUT=%Documents%\maya\modules\brSmoothWeights.mod
set BRD_PATH=%INSTALL_DIR%\scripts\utilityToolKit\brSmoothWeights

rem Create the global modules directory if it doesn't exist.
if not exist %Documents%\maya\modules mkdir %Documents%\maya\modules

rem List of Maya versions
set "versions=2017 2018 2019 2020 2022 2023 2024 "

echo  是否安装PY_RIGASSI 在当前路径 [" %cd% "]  安装输入y / 取消输入n 
@REM set /p input= " > 是否安装PY_RIGASSI 在当前路径 [" %cd% "]  安装输入y / 取消输入n ? [ y/n ] :"
set /p input= " >>> Whether to install PY_RIGASSIT Tool [" %cd% "]  yes/no ? [ y/n ] :"

echo  ---------------------------------------------------------------------------------

@REM echo 您的maya是否需要安装brSmoothWeights： 如果maya之前安装了的输入n，没有的安装的属于y！！！ [ y/n ] :"

@REM set /p brt_input= " >>> Whether to install brSmoothWeights Tool [" %BRD_PATH% "] ? [ y/n ] :"

@REM rem Check if the file exists and set brt_input accordingly
@REM if exist "%BRS_OUTPUT%" (
@REM     set brt_input=n
@REM ) else (
@REM     set brt_input=y
@REM )


if /i "%input%"=="y" (

    (
    echo + MAYAVERSION:2017 PY_RIGASSIT any %INSTALL_DIR% 
    echo plug-ins: plug-ins/2017
    echo [r] icons: icons
    echo scripts: scripts/py27
    echo MAYA_SCRIPT_PATH +:= scripts
    echo.    
    echo + MAYAVERSION:2018 PY_RIGASSIT any %INSTALL_DIR% 
    echo plug-ins: plug-ins/2018
    echo [r] icons: icons
    echo scripts: scripts/py27
    echo MAYA_SCRIPT_PATH +:= scripts
    echo.
    echo + MAYAVERSION:2019 PY_RIGASSIT any %INSTALL_DIR% 
    echo plug-ins: plug-ins/2019
    echo [r] icons: icons
    echo scripts: scripts/py27
    echo MAYA_SCRIPT_PATH +:= scripts
    echo.
    echo + MAYAVERSION:2020 PY_RIGASSIT any %INSTALL_DIR% 
    echo plug-ins: plug-ins/2020
    echo [r] icons: icons
    echo scripts: scripts/py27
    echo MAYA_SCRIPT_PATH +:= scripts
    echo.
    echo + MAYAVERSION:2022 PY_RIGASSIT any %INSTALL_DIR% 
    echo plug-ins: plug-ins/2022
    echo [r] icons: icons
    echo scripts: scripts/py37
    echo MAYA_SCRIPT_PATH +:= scripts
    echo.
    echo + MAYAVERSION:2023 PY_RIGASSIT any %INSTALL_DIR% 
    echo plug-ins: plug-ins/2023
    echo scripts: scripts/py39
    echo MAYA_SCRIPT_PATH +:= scripts 
    echo.
    echo + MAYAVERSION:2024 PY_RIGASSIT any %INSTALL_DIR% 
    echo plug-ins: plug-ins/2024
    echo scripts: scripts/py310
    echo MAYA_SCRIPT_PATH +:= scripts 
    echo.
    echo + MAYAVERSION:2025 PY_RIGASSIT any %INSTALL_DIR% 
    echo plug-ins: plug-ins/2025
    echo scripts: scripts/py311
    echo MAYA_SCRIPT_PATH +:= scripts 
    echo.
    echo + MAYAVERSION:2026 PY_RIGASSIT any %INSTALL_DIR% 
    echo plug-ins: plug-ins/2026
    echo scripts: scripts/py311
    echo MAYA_SCRIPT_PATH +:= scripts 
    echo.

    ) > "%OUTPUT%"
    echo.
    rem Print INSTALL_DIR and Mod to the screen
    echo INSTALL_DIR PY_RIGASSIT is set to: %INSTALL_DIR%
    echo PY_RIGASSIT MOD is set to: %OUTPUT%

    
    @REM if /i "%brt_input%"=="y" (
    @REM     (
    @REM         for %%V in (%versions%) do (
    @REM             echo + MAYAVERSION:%%V brSmoothWeights  any %BRD_PATH%
    @REM             echo plug-ins: plug-ins/win64/%%V
    @REM             echo [r] icons: icons
    @REM             echo [r] scripts: scripts
    @REM             echo.
    @REM         )
    @REM     ) > "%BRS_OUTPUT%"
    @REM     echo.
    @REM     rem Print INSTALL_DIR and Mod to the screen
    @REM     echo brSmoothWeights INSTALL_DIR is set to: %BRD_PATH%
    @REM     echo brSmoothWeights MOD is set to: %BRS_OUTPUT%

    @REM     )else (
    @REM         echo.
    @REM         @REM echo  brSmoothWeights Tool 安装取消.
    @REM     )

        echo.
        echo  =================================================================================
        echo  PY_RIGASSIT Tool installed successfully 安装完成!
        echo.
        )else (
            echo.
            echo  PY_RIGASSIT Tool installation canceled 取消.
            )


rem For binary modules, create a module for each version, including a bunch of versions that don't
rem exist yet.  This way, when users update for future versions, they won't always need to rerun
rem install.bat.  This creates a bunch of noise in the module file, but that's not intended to be
rem edited by hand.  This would be a lot nicer if Maya modules allowed substitutions in paths.
rem
rem These entries have a different module name py_RIGASSIT) than the entry above, since Maya will
rem only load entries from the first matching entry.
rem
rem will only work on Windows, so there's no point including those here.

endlocal
pause
