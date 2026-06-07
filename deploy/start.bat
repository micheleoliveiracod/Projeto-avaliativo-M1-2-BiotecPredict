@echo off
setlocal enabledelayedexpansion

set ACTION=%1
if "%ACTION%"=="" set ACTION=start

cd /d "%~dp0"

if "%ACTION%"=="start" (
    echo [BiotecPredict] Iniciando sistema...
    docker compose up -d --build
    echo.
    echo Aguardando servicos ficarem prontos...
    timeout /t 20 /nobreak >nul
    echo.
    echo [OK] Sistema iniciado!
    echo.
    echo   Frontend:  http://localhost
    echo   API:       http://localhost:8000/api
    echo   Swagger:   http://localhost:8000/docs
    echo.
    goto end
)

if "%ACTION%"=="stop" (
    echo [BiotecPredict] Parando sistema...
    docker compose stop
    echo [OK] Sistema parado.
    goto end
)

if "%ACTION%"=="restart" (
    echo [BiotecPredict] Reiniciando sistema...
    docker compose restart
    echo [OK] Sistema reiniciado.
    goto end
)

if "%ACTION%"=="logs" (
    if "%2"=="" (
        docker compose logs -f
    ) else (
        docker compose logs -f %2
    )
    goto end
)

if "%ACTION%"=="status" (
    docker compose ps
    goto end
)

if "%ACTION%"=="clean" (
    echo [AVISO] Isso vai remover todos os containers e dados!
    set /p CONFIRM="Tem certeza? (s/N): "
    if /i "!CONFIRM!"=="s" (
        docker compose down -v
        echo [OK] Sistema e dados removidos.
    ) else (
        echo Operacao cancelada.
    )
    goto end
)

echo Uso: start.bat [start^|stop^|restart^|logs^|status^|clean]
echo.
echo   start    - Iniciar o sistema (default)
echo   stop     - Parar o sistema
echo   restart  - Reiniciar o sistema
echo   logs     - Ver logs (logs backend / logs frontend)
echo   status   - Ver status dos containers
echo   clean    - Remover tudo, incluindo dados

:end
endlocal
