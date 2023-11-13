@ECHO OFF

SET FILE_NAME=videogrep

IF EXIST "%FILE_NAME%.exe" (
	DEL "%FILE_NAME%.exe"
)

python.exe -m PyInstaller %FILE_NAME%.spec

IF EXIST "dist\%FILE_NAME%.exe" (
	COPY /Y "dist\%FILE_NAME%.exe" .
) ELSE (
	ECHO Build FAILED
)

RMDIR /S /Q build
RMDIR /S /Q dist

REM PAUSE