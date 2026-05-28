@echo off
echo ================================================
echo  wuma-proxy build script
echo ================================================
echo.

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed.
    echo   Download from https://www.python.org/downloads/
    echo   CHECK "Add Python to PATH" during install!
    pause
    exit /b 1
)

echo [1/3] Python found:
python --version
echo.

echo [2/3] Installing required packages...
pip install websockets pyinstaller
if errorlevel 1 (
    echo [ERROR] Package install failed. Check internet connection.
    pause
    exit /b 1
)
echo.

echo [3/3] Building exe...
pyinstaller --onefile --console --name wuma-proxy wuma_proxy.py
if errorlevel 1 (
    echo [ERROR] Build failed.
    pause
    exit /b 1
)
echo.
echo Build complete!
echo Output: dist\wuma-proxy.exe
echo.
pause
