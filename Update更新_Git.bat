@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

title PY_RIGASSIT Updater

cd /d "%~dp0"

echo.
echo ========================================
echo          PY_RIGASSIT Updater
echo ========================================
echo.

git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git not found.
    echo.
    echo Please download and install Git from:
    echo https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)

if exist ".git" goto UPDATE

echo First time installation detected.
echo.
set /p INSTALL=Install latest version here? (Y/N):

if /i not "!INSTALL!"=="Y" (
    echo Cancelled.
    pause
    exit /b 0
)

echo.
echo Cloning repository...
echo.

git clone https://github.com/yolandaPing/PY_RIGASSIT_update.git temp_clone
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Clone failed.
    pause
    exit /b 1
)

xcopy "temp_clone\*" "." /E /H /Y /Q >nul
if %errorlevel% neq 0 (
    rd /s /q temp_clone 2>nul
    echo.
    echo [ERROR] Copy failed.
    pause
    exit /b 1
)

rd /s /q temp_clone 2>nul

echo.
echo Installation completed.
echo.
pause
exit /b 0

:UPDATE
echo Cleaning Python cache...

for /d /r %%d in (__pycache__) do (
    if exist "%%d" rd /s /q "%%d" 2>nul
)

for /r %%f in (*.pyc) do (
    if exist "%%f" del /f /q "%%f" 2>nul
)

echo.
echo Checking for updates...
echo.

git fetch origin
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Fetch failed.
    pause
    exit /b 1
)

for /f %%i in ('git rev-parse HEAD') do set LOCAL=%%i
for /f %%i in ('git rev-parse origin/main 2^>nul') do set REMOTE=%%i

if "!LOCAL!"=="!REMOTE!" (
    echo.
    echo Already up to date.
    echo.
    pause
    exit /b 0
)

echo.
echo Updating...
echo.

git reset --hard HEAD
git clean -fd

git pull origin main
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Pull failed.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Update completed successfully.
echo ========================================
echo.

git log -1 --pretty=format:"Commit: %%h" 2>nul
echo.
git log -1 --pretty=format:"Message: %%s" 2>nul
echo.
echo.

pause
exit /b 0