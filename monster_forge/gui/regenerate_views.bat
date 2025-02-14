@echo off

echo.
echo Converting all .ui files in "%~dp0view\qt_designer" to .py using pyuic5...
echo.

for %%F in ("%~dp0\view\qt_designer\*.ui") do (
    echo Processing %%~nxF...
    pyuic5 "%%F" -o "%~dp0\view\%%~nF.py"
)

echo.
echo Conversion complete!
pause