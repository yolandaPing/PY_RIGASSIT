@echo off
chcp 65001 >nul 2>&1
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

echo Downloading from %REPO_URL% to %TARGET_DIR% ...

set "ZIP_URL=%REPO_URL%/archive/refs/heads/%BRANCH%.zip"
set "ZIP_FILE=%TEMP%\PY_RIGASSIT_update_%RANDOM%.zip"
set "EXTRACT_TEMP=%TEMP%\PY_RIGASSIT_extract_%RANDOM%"

powershell -Command "& { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%ZIP_URL%' -OutFile '%ZIP_FILE%' -UseBasicParsing }" >nul 2>&1

if not exist "%ZIP_FILE%" (
    echo Failed, trying master branch...
    set "BRANCH=master"
    set "ZIP_URL=%REPO_URL%/archive/refs/heads/%BRANCH%.zip"
    powershell -Command "& { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%ZIP_URL%' -OutFile '%ZIP_FILE%' -UseBasicParsing }" >nul 2>&1
    if not exist "%ZIP_FILE%" (
        echo Error: Cannot download repository.
        pause
        exit /b 1
    )
)

mkdir "%EXTRACT_TEMP%" 2>nul

powershell -Command "& { Expand-Archive -Path '%ZIP_FILE%' -DestinationPath '%EXTRACT_TEMP%' -Force }" >nul 2>&1

if errorlevel 1 (
    echo Error: Expand-Archive failed.
    pause
    exit /b 1
)

for /d %%i in ("%EXTRACT_TEMP%\*") do set "EXTRACTED_FOLDER=%%i"

if not defined EXTRACTED_FOLDER (
    echo Error: Cannot locate extracted folder.
    echo 错误: 无法找到解压后的文件夹.
    pause
    exit /b 1
)


:: Clean old cache
echo Cleaning old cache files...

if exist "%TARGET_DIR%\scripts\user_defined.py" (
    del /f /q "%TARGET_DIR%\scripts\user_defined.py"
    echo Deleted redundant files
)

:: Delete all __pycache__ folders (recursive)
for /d /r "%TARGET_DIR%" %%d in (__pycache__) do (
    if exist "%%d" (
        echo Removing folder %%d
        rmdir /s /q "%%d"
    )
)

:: Delete all user_defined.pyd files (recursive)
for /r "%TARGET_DIR%" %%f in (user_defined.pyd) do (
    if exist "%%f" (
        echo Removing file %%f
        del /f /q "%%f"
    )
)

echo Cleanup completed.


echo Moving files to current directory...
xcopy "%EXTRACTED_FOLDER%\*" "%TARGET_DIR%\" /E /H /Y >nul

rd /s /q "%EXTRACT_TEMP%" 2>nul
del "%ZIP_FILE%" 2>nul

echo ========================================
echo Update completed successfully!
echo Files saved to: %TARGET_DIR%
echo 更新完成!
echo ========================================
pause