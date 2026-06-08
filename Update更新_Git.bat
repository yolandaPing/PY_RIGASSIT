@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

title PY_RIGASSIT Updater

:: ========================================
:: Config
:: ========================================

set REPO_URL=https://github.com/yolandaPing/PY_RIGASSIT_update.git
set BRANCH=main

:: ========================================

echo.
echo ========================================
echo         PY_RIGASSIT Updater
echo ========================================
echo.

:: Check Git
git --version >nul 2>&1

if errorlevel 1 (
echo [ERROR] Git not found.
echo.
echo Please install Git:
echo https://git-scm.com/download/win
echo.
pause
exit /b 1
)

:: First install
if not exist ".git" (

```
echo First installation detected...
echo Initializing repository...
echo.

git init

git remote remove origin >nul 2>&1

git remote add origin %REPO_URL%

git fetch origin

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to connect GitHub.
    pause
    exit /b 1
)

git reset --hard origin/%BRANCH%
```

)

:: Clean Python cache
echo Cleaning Python cache...
echo.

for /d /r %%i in (**pycache**) do (
if exist "%%i" rd /s /q "%%i"
)

for /r %%i in (*.pyc) do (
del /f /q "%%i" >nul 2>&1
)

:: Update
echo Fetching latest version...
echo.

git fetch origin

if errorlevel 1 (
echo.
echo [ERROR] Fetch failed.
pause
exit /b 1
)

echo Updating files...
echo.

git reset --hard origin/%BRANCH%

if errorlevel 1 (
echo.
echo [ERROR] Update failed.
pause
exit /b 1
)

echo.
echo ========================================
echo        Update Complete 
echo ========================================
echo.

git log -1 --oneline

echo.
pause
exit /b 0
