@echo off
chcp 65001 >nul 2>&1
setlocal enabledelayedexpansion

title PY_RIGASSIT Cleaning 

cd /d "%~dp0"

echo.
echo ========================================
echo          PY_RIGASSIT Cleaning
echo ========================================
echo.

set "TARGET_DIR=%CD%"

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

echo.
echo ========================================
echo Cleaning complete.
echo ========================================
echo.

pause
exit /b 0