@echo off
rem Double-click to verify and flash the Traditional Chinese firmware.
setlocal
cd /d "%~dp0"

set "PY="
py -3 --version >nul 2>&1 && set "PY=py -3"
if not defined PY python --version >nul 2>&1 && set "PY=python"
if not defined PY goto nopython

%PY% -c "import esptool" >nul 2>&1
if errorlevel 1 goto install

goto run

:install
echo.
echo This one-time step needs the esptool package (Python).
choice /c YN /m "Install it now with pip"
if errorlevel 2 goto cancel
%PY% -m pip install --upgrade esptool
if errorlevel 1 goto pipfail

:run
%PY% flash.py %*
if errorlevel 1 goto failed
echo.
pause
exit /b 0

:cancel
echo Cancelled.
pause
exit /b 0

:pipfail
echo.
echo Install failed. Run this manually, then double-click again:
echo   %PY% -m pip install --upgrade esptool
pause
exit /b 1

:failed
echo.
echo Flashing failed. See the messages above.
pause
exit /b 1

:nopython
echo.
echo Python was not found.
echo Install Python 3 from python.org and tick "Add Python to PATH",
echo then double-click this file again. Opening the download page...
start https://www.python.org/downloads/
pause
exit /b 1
