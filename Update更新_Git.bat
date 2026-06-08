@echo off
chcp 65001 >nul
title PY_RIGASSIT Updater

echo.
echo ========================================
echo         PY_RIGASSIT Updater
echo ========================================
echo.

git --version >nul 2>&1
if errorlevel 1 (
echo [ERROR] Git not found.
echo.
echo Please download and install Git from:
echo https://git-scm.com/download/win
echo.
pause
exit /b
)

if not exist ".git" (
echo [ERROR] Not a Git repository.
pause
exit /b
)

echo Cleaning Python cache...

for /r %%i in (**pycache**) do (
if exist "%%i" rd /s /q "%%i"
)

for /r %%i in (*.pyc) do (
del /f /q "%%i" >nul 2>&1
)

echo.
echo Fetching latest version...
echo.

git fetch origin

if errorlevel 1 (
echo [ERROR] Fetch failed.
pause
exit /b
)

echo.
echo Updating files...
echo.

git checkout -f origin/main -- .

if errorlevel 1 (
echo [ERROR] Update failed.
pause
exit /b
)

echo.
echo ========================================
echo Update Complete !!!
echo ========================================

git log -1 --oneline

echo.
pause
