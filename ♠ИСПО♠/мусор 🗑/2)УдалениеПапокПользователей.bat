@echo off
setlocal enableextensions enabledelayedexpansion

rem местонахождение директории для очистки
set sTargetFolder=C:\Users

rem Поддиректория (или файл), которая НЕ должна удаляться
set sExcludeFilesOrFolders="Default" "ssimoyanov" "istepanov" "sgogolev" "ashavrov" "echukavin" "user" "operator" "Public" "adm" "admin" "yukostin"

for /f "tokens=*" %%i in ('dir "%sTargetFolder%" /b /a:-d') do (
	set /a bDelete = 1
	
	for %%j in (%sExcludeFilesOrFolders%) do (
		if /i "%%i" equ "%%~j" set /a bDelete = 0
	)
	
	if !bDelete! equ 1 del /f /q "%sTargetFolder%\%%i"
)

for /f "tokens=*" %%i in ('dir "%sTargetFolder%" /b /a:d') do (
	set /a bDelete = 1
	
	for %%j in (%sExcludeFilesOrFolders%) do (
		if /i "%%i" equ "%%~j" set /a bDelete = 0
	)
	
	if !bDelete! equ 1 rd /s /q "%sTargetFolder%\%%i"
)

endlocal


setlocal enableextensions enabledelayedexpansion

rem местонахождение директории для очистки
set sTargetFolder=C:\Users

rem Поддиректория (или файл), которая НЕ должна удаляться
set sExcludeFilesOrFolders="Default" "istepanov" "sgogolev" "ssimoyanov" "ashavrov" "echukavin" "user" "operator" "Public" "adm" "admin" "yukostin"

for /f "tokens=*" %%i in ('dir "%sTargetFolder%" /b /a:-d') do (
	set /a bDelete = 1
	
	for %%j in (%sExcludeFilesOrFolders%) do (
		if /i "%%i" equ "%%~j" set /a bDelete = 0
	)
	
	if !bDelete! equ 1 del /f /q "%sTargetFolder%\%%i"
)

for /f "tokens=*" %%i in ('dir "%sTargetFolder%" /b /a:d') do (
	set /a bDelete = 1
	
	for %%j in (%sExcludeFilesOrFolders%) do (
		if /i "%%i" equ "%%~j" set /a bDelete = 0
	)
	
	if !bDelete! equ 1 rd /s /q "%sTargetFolder%\%%i"
)

endlocal


exit /b 0