@echo off
:: Sprawdzanie uprawnień administratora
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if %errorlevel% neq 0 (
    echo Uruchamianie jako administrator...
    goto UACPrompt
) else (
    goto gotAdmin
)

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    exit /b

:gotAdmin
    del "%temp%\getadmin.vbs"
    pushd "%CD%"
    CD /D "%~dp0"
:: Poniżej znajduje się miejsce na Twoje polecenia
    cd /D "C:\Gry\PycharmProjects\SKANER\LOGISTICS"
    cmd /K
