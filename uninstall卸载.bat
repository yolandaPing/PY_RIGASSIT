@echo off
chcp 65001 >nul
setlocal

title Uninstall PY_RIGASSIT

for /f "tokens=2*" %%A in (
    'reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v Personal'
) do set "Documents=%%B"

set "versions=2017 2018 2019 2020 2021 2022 2023 2024 2025 2026"

echo.
echo ==========================================================
echo                PY_RIGASSIT Uninstaller
echo ==========================================================
echo.

set /p input=^>^>^> Confirm uninstall PY_RIGASSIT ? [y/n] :

if /i not "%input%"=="y" (
    echo.
    echo Cancelled.
    pause
    exit /b
)

echo.
echo Removing module files...
echo.

if exist "%Documents%\maya\modules\PY_RIGASSIT.mod" (
    del /f /q "%Documents%\maya\modules\PY_RIGASSIT.mod"
)

for %%V in (%versions%) do (
    if exist "%Documents%\maya\%%V\modules\PY_RIGASSIT.mod" (
        del /f /q "%Documents%\maya\%%V\modules\PY_RIGASSIT.mod"
    )
    if exist "%Documents%\maya\%%V\zh_CN\modules\PY_RIGASSIT.mod" (
        del /f /q "%Documents%\maya\%%V\zh_CN\modules\PY_RIGASSIT.mod"
    )
    if exist "%Documents%\maya\%%V\prefs\shelves\shelf_PY_RIGASSIT.mel" (
        del /f /q "%Documents%\maya\%%V\prefs\shelves\shelf_PY_RIGASSIT.mel"
    )
    if exist "%Documents%\maya\%%V\prefs\icons\PY_RIGASSIT*" (
        del /f /q "%Documents%\maya\%%V\prefs\icons\PY_RIGASSIT*"
    )
    if exist "%Documents%\maya\%%V\prefs\PY_RIGASSIT*" (
        del /f /q "%Documents%\maya\%%V\prefs\PY_RIGASSIT*"
    )
)

echo.
echo ==========================================================
echo            PY_RIGASSIT Uninstall Complete
echo ==========================================================
echo.

echo Done.
echo Maya configs removed.
echo Modules removed.
echo Shelf removed.
echo Icons removed.

echo.
pause