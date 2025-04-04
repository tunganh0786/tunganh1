@echo off
setlocal EnableDelayedExpansion

set "CHOCO_PATH=C:\ProgramData\chocolatey\bin"
set "PATH=%PATH%;%CHOCO_PATH%"

if not exist "%CHOCO_PATH%\choco.exe" (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" >nul 2>&1
    if !ERRORLEVEL! NEQ 0 exit /b 1
    set "PATH=%PATH%;%CHOCO_PATH%"
)

"%CHOCO_PATH%\choco.exe" -v >nul 2>&1
if %ERRORLEVEL% NEQ 0 exit /b 1

set "PYTHON_PATH=C:\Python313\python.exe"
"%PYTHON_PATH%" --version >nul 2>&1 || python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    "%CHOCO_PATH%\choco.exe" install python -y >nul 2>&1
    if !ERRORLEVEL! NEQ 0 exit /b 1
    call refreshenv >nul 2>&1
)

"%PYTHON_PATH%" -m ensurepip --upgrade >nul 2>&1
"%PYTHON_PATH%" -m pip install --upgrade pip >nul 2>&1
"%PYTHON_PATH%" -m pip install requests webdriver_manager selenium --quiet >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    python -m ensurepip --upgrade >nul 2>&1
    python -m pip install --upgrade pip >nul 2>&1
    python -m pip install requests webdriver_manager selenium --quiet >nul 2>&1
    if !ERRORLEVEL! NEQ 0 exit /b 1
)

start /B "" "%PYTHON_PATH%" script.py >nul 2>&1 || start /B "" python script.py >nul 2>&1
exit /b 0
