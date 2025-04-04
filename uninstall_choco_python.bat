@echo off
echo Dang go cai dat Chocolatey va Python...
timeout /t 2 /nobreak >nul

:: Gỡ cài đặt Python nếu có
echo Dang kiem tra Python...
for /f "tokens=2 delims==" %%I in ('wmic product where "name like 'Python%%'" get name /format:value') do (
    echo Dang go bo %%I...
    wmic product where name="%%I" call uninstall /nointeractive
)
echo Da go Python xong!

:: Gỡ cài đặt Chocolatey
echo Dang go bo Chocolatey...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Remove-Item -Recurse -Force C:\ProgramData\chocolatey"
setx PATH "%PATH:C:\ProgramData\chocolatey\bin;=%"
echo Da go Chocolatey xong!

echo Da hoan thanh! Vui long khoi dong lai may.
pause
