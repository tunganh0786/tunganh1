@echo off
 echo Starting setup...
 
 :: Set Chocolatey path manually
 set "CHOCO_PATH=C:\ProgramData\chocolatey\bin"
 set "PATH=%PATH%;%CHOCO_PATH%"
 
 :: Check if Chocolatey is installed
 if not exist "%CHOCO_PATH%\choco.exe" (
     echo Chocolatey not found. Installing Chocolatey...
     powershell -NoProfile -ExecutionPolicy Bypass -Command "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))"
     if %ERRORLEVEL% NEQ 0 (
         echo Failed to install Chocolatey. Exiting...
         pause
         exit /b 1
     )
     echo Chocolatey installed successfully. Updating PATH...
     set "PATH=%PATH%;%CHOCO_PATH%"
 ) else (
     echo Chocolatey is already installed.
 )
 
 :: Verify Chocolatey is working
 
 "%CHOCO_PATH%\choco.exe" -v >nul 2>&1
 if %ERRORLEVEL% NEQ 0 (
     echo Chocolatey is installed but not functioning correctly. Please restart your shell or check installation.
     
 ) else (
     echo Chocolatey version check successful.
    
 )
 
 :: Check if Python is installed (try python --version or default Chocolatey install path)
 
 set "PYTHON_PATH=C:\Python313\python.exe"
 "%PYTHON_PATH%" --version >nul 2>&1 || python --version >nul 2>&1
 if %ERRORLEVEL% NEQ 0 (
     echo Python not found. Installing Python via Chocolatey...
    
     "%CHOCO_PATH%\choco.exe" install python -y
     if %ERRORLEVEL% EQU 3010 (
         echo Python installed successfully, but a reboot is recommended.
         
     ) else if %ERRORLEVEL% NEQ 0 (
         echo Failed to install Python with unexpected error. Exiting...
     
         pause
         exit /b 1
     )
     call refreshenv
 ) else (
     echo Python is already installed.
 )
 
 :: Install required Python libraries
 echo Installing required Python libraries...
 "%PYTHON_PATH%" -m ensurepip --upgrade >nul 2>&1
 "%PYTHON_PATH%" -m pip install --upgrade pip >nul 2>&1
 "%PYTHON_PATH%" -m pip install requests webdriver_manager selenium >nul 2>&1
 if %ERRORLEVEL% NEQ 0 (
     echo Failed to install required libraries. Trying with python command...
     python -m ensurepip --upgrade >nul 2>&1
     python -m pip install --upgrade pip >nul 2>&1
     python -m pip install requests webdriver_manager selenium >nul 2>&1
     if %ERRORLEVEL% NEQ 0 (
         echo Failed to install Python libraries. Please install them manually.
         pause
         exit /b 1
     )
 )
 echo Libraries installed successfully.
 
 :: Run script.py
 echo Running script.py...
 "%PYTHON_PATH%" script.py 2>nul || python script.py
 if %ERRORLEVEL% NEQ 0 (
     echo Failed to run script.py. Please check if script.py exists and Python is working.
     pause
     exit /b 1
 )
bỏ hết các dòng thông báo giúp tôi
