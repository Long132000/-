@echo off
 
set "key=HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProfileList"
 
for /f "delims=" %%i in (
    'reg query "%key%"^| findstr /i /c:"%key%\\"'
    ) do (
    reg query "%%~i" /v "CentralProfile">nul 2>&1 && reg delete "%%~i" /f
)