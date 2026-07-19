#!/bin/bash
set -e

ACTION="${1:-start}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

case "$ACTION" in
  start)
    echo "[BiotecPredict] Iniciando sistema..."
    docker compose up -d --build
    echo ""
    echo "Aguardando serviços ficarem prontos..."
    sleep 20
    echo ""
    echo "[OK] Sistema iniciado!"
    echo ""
    echo "  Frontend:  http://localhost"
    echo "  API:       http://localhost:8000/api"
    echo "  Swagger:   http://localhost:8000/docs"
    echo ""
    ;;
  stop)
    echo "[BiotecPredict] Parando sistema..."
    docker compose stop
    echo "[OK] Sistema parado."
    ;;
  restart)
    echo "[BiotecPredict] Reiniciando sistema..."
    docker compose restart
    echo "[OK] Sistema reiniciado."
    ;;
  logs)
    if [ -z "$2" ]; then
      docker compose logs -f
    else
      docker compose logs -f "$2"
    fi
    ;;
  status)
    docker compose ps
    ;;
  clean)
    echo "[AVISO] Isso vai remover os containers e o modelo de ML treinado!"
    echo "O banco de dados NÃO é apagado - fica em backend/data/Biotecpredict.db."
    read -p "Tem certeza? (s/N): " CONFIRM
    if [[ "$CONFIRM" =~ ^[sS]$ ]]; then
      docker compose down -v
      echo "[OK] Containers e modelo de ML removidos. Banco de dados preservado."
    else
      echo "Operação cancelada."
    fi
    ;;
  *)
    echo "Uso: ./start.sh [start|stop|restart|logs|status|clean]"
    echo ""
    echo "  start    - Iniciar o sistema (default)"
    echo "  stop     - Parar o sistema"
    echo "  restart  - Reiniciar o sistema"
    echo "  logs     - Ver logs (logs backend / logs frontend)"
    echo "  status   - Ver status dos containers"
    echo "  clean    - Remover tudo, incluindo dados"
    ;;
esac
