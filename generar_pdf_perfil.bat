@echo off
setlocal

cd /d "%~dp0"

echo =========================================
echo Generador de PDF del perfil
echo =========================================

set "PYTHON_CMD="

where py >nul 2>&1
if not errorlevel 1 (
  set "PYTHON_CMD=py -3"
)

if not defined PYTHON_CMD (
  where python >nul 2>&1
  if not errorlevel 1 (
    set "PYTHON_CMD=python"
  )
)

if not defined PYTHON_CMD (
  echo [ERROR] No se encontro Python ni el launcher py en el PATH.
  echo Instala Python y vuelve a intentarlo.
  pause
  exit /b 1
)

echo Usando interprete: %PYTHON_CMD%

if not exist "generar_pdf_perfil.py" (
  echo [ERROR] No se encontro generar_pdf_perfil.py en esta carpeta.
  pause
  exit /b 1
)

echo.
echo Verificando dependencias de Python...
%PYTHON_CMD% -c "import playwright" >nul 2>&1
if errorlevel 1 (
  echo Instalando dependencias desde requirements.txt...
  %PYTHON_CMD% -m pip install -r requirements.txt
  if errorlevel 1 (
    echo [ERROR] No fue posible instalar dependencias.
    pause
    exit /b 1
  )
)

echo Verificando navegador Chromium de Playwright...
%PYTHON_CMD% -m playwright install chromium
if errorlevel 1 (
  echo [ERROR] No se pudo instalar/verificar Chromium para Playwright.
  pause
  exit /b 1
)

echo.
echo Ejecutando script de generacion...
%PYTHON_CMD% "generar_pdf_perfil.py"
if errorlevel 1 (
  echo.
  echo [ERROR] La generacion del PDF fallo.
  echo Revisa el mensaje anterior para ver la causa exacta.
  pause
  exit /b 1
)

echo.
echo [OK] PDF generado correctamente: cv.pdf
echo.
exit /b 0
