@echo off
echo Starting Core Integrator Demo Services...
echo.

echo Starting Noopur Service (Port 5001)...
start "Noopur Service" cmd /k "cd external\CreatorCore-Task && python app.py"

timeout /t 3 /nobreak >nul

echo Starting Mock CreatorCore (Port 5002)...
start "Mock CreatorCore" cmd /k "cd tests\mocks && python creatorcore_mock.py"

timeout /t 3 /nobreak >nul

echo Verifying services...
curl http://localhost:5001/history
echo.
curl http://localhost:5002/system/health
echo.

echo Demo services are ready!
pause