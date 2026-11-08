@echo off
REM Run the Django development server on Windows

setlocal
cd config
python manage.py runserver
endlocal
