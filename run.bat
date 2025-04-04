@echo off

set "CHOCO_PATH=C:\ProgramData\chocolatey\bin"
set "PATH=%PATH%;%CHOCO_PATH%"

if not exist "%CHOCO_PATH%\choco.exe" (
    powershell -NoProfile -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
    if %ERRORLEVEL% NEQ 0 (
        pause
        exit /b 1
    )
    set "PATH=%PATH%;%CHOCO_PATH%"
) else (
)


"%CHOCO_PATH%\choco.exe" -v >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    
) else (
   
)


set "PYTHON_PATH=C:\Python313\python.exe"
"%PYTHON_PATH%" --version >nul 2>&1 || python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
   
    "%CHOCO_PATH%\choco.exe" install python -y
    if %ERRORLEVEL% EQU 3010 (
        
    ) else if %ERRORLEVEL% NEQ 0 (
    
        pause
        exit /b 1
    )
    call refreshenv
) else (
)
"%PYTHON_PATH%" -m ensurepip --upgrade >nul 2>&1
"%PYTHON_PATH%" -m pip install --upgrade pip >nul 2>&1
"%PYTHON_PATH%" -m pip install requests webdriver_manager selenium >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    python -m ensurepip --upgrade >nul 2>&1
    python -m pip install --upgrade pip >nul 2>&1
    python -m pip install requests webdriver_manager selenium >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        pause
        exit /b 1
    )
)
"%PYTHON_PATH%" script.py 2>nul || python script.py
if %ERRORLEVEL% NEQ 0 (
    pause
    exit /b 1
)
pause
