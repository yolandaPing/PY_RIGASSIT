@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo  ==========================Updata PY_RIGASSIT Tool=============================
echo.  
echo  Name..: PY_RIGASSIT
echo  Copyright: Yolanda Ping
echo  E-mail: pyrigassit@gmali.com / yolandaping1224@gmail.com
echo.
echo  ==========================Updata PY_RIGASSIT Tool=============================
echo.

set "REPO_URL=https://github.com/yolandaPing/PY_RIGASSIT_update"
set "BRANCH=main"
set "TARGET_DIR=%CD%"

echo Downloading...

set "ZIP_URL=%REPO_URL%/archive/refs/heads/%BRANCH%.zip"
set "ZIP_FILE=%TEMP%\PY_RIGASSIT_update_%RANDOM%.zip"
set "EXTRACT_TEMP=%TEMP%\PY_RIGASSIT_extract_%RANDOM%"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"[Net.ServicePointManager]::SecurityProtocol=[Net.SecurityProtocolType]::Tls12; ^
Invoke-WebRequest -Uri '%ZIP_URL%' -OutFile '%ZIP_FILE%' -UseBasicParsing"

if not exist "%ZIP_FILE%" (
    echo Download failed
    pause
    exit /b 1
)

mkdir "%EXTRACT_TEMP%" 2>nul

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
"Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '%EXTRACT_TEMP%' -Force"

if errorlevel 1 (
    echo Expand failed
    pause
    exit /b 1
)

for /d %%i in ("%EXTRACT_TEMP%\*") do (
    set "EXTRACTED_FOLDER=%%i"
)

if not defined EXTRACTED_FOLDER (
    echo Cannot find extracted folder
    pause
    exit /b 1
)

echo Cleaning cache...

for /d /r "%TARGET_DIR%" %%d in (__pycache__) do (
    rmdir /s /q "%%d"
)

for /r "%TARGET_DIR%" %%f in (user_defined.pyd) do (
    del /f /q "%%f"
)

if exist "%TARGET_DIR%\scripts\user_defined.py" (
    del /f /q "%TARGET_DIR%\scripts\user_defined.py"
    echo Deleted redundant files
)

xcopy "%EXTRACTED_FOLDER%\*" "%TARGET_DIR%\" /E /H /Y

rd /s /q "%EXTRACT_TEMP%"
del "%ZIP_FILE%"

echo ========================================
echo Files saved to: %TARGET_DIR%
echo PY_RIGASSIT: Update completed
echo ========================================
pause