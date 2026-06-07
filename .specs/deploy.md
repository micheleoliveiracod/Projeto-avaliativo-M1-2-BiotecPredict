# Deploy - BiotecPredict

**Versão**: 0.1.0  
**Data**: 24 de Maio de 2026  
**Status**: ✅ Deploy Local Configurado

---

## 🎯 Objetivo

Guia completo para deploy do BiotecPredict em ambiente local com Docker Compose, contendo backend FastAPI e frontend React. O banco de dados é SQLite (arquivo local, sem container necessário).

---

## 📋 Pré-requisitos ✅

### Windows ✅
- ✅ Docker Desktop instalado (https://www.docker.com/products/docker-desktop)
- ✅ Docker Compose (incluído no Docker Desktop)
- ✅ Mínimo 4GB RAM disponível
- ✅ Portas 80, 8000 disponíveis

### Mac/Linux ✅
- ✅ Docker instalado
- ✅ Docker Compose instalado
- ✅ Mínimo 4GB RAM disponível

---

## 🚀 Início Rápido (3 passos) ✅

### 1. Abra Terminal/CMD

**Windows**: Pressione `Win + R`, digite `cmd`, Enter  
**Mac/Linux**: Abra Terminal

### 2. Navegue até deploy

```bash
cd "c:\Users\miche\Projetos GitHub\projeto-avaliativo-m1-2-biotecpredict\deploy"
```

### 3. Execute o script

**Windows**:
```cmd
start.bat
```

**Mac/Linux**:
```bash
chmod +x start.sh
./start.sh
```

**Pronto!** Sistema rodando em http://localhost

---

## 📁 Arquivos de Deploy

| Arquivo | Descrição |
|---------|-----------|
| `docker-compose.yml` | Orquestração: backend + frontend + volumes (SQLite + modelos ML) |
| `Dockerfile.backend` | Python 3.13-slim + uvicorn; health check em /health |
| `Dockerfile.frontend` | Build Node 18 → servido por nginx Alpine |
| `nginx.conf` | Proxy /api e /health para backend:8000; fallback SPA para React Router |
| `start.bat` | start / stop / restart / logs / status / clean (Windows) |
| `start.sh` | Mesmo para Mac/Linux |
| `../.env.example` | Template de variáveis (na raiz do projeto — copie para `.env`) |

---

## 🐳 Containers Inclusos (2 Total)

```
┌─────────────────────────────────────────────────────┐
│  1. FastAPI Backend    2. React Frontend (nginx)    │
│  SQLite persistido em volume Docker                 │
└─────────────────────────────────────────────────────┘
```

### 1. FastAPI Backend
- **Porta**: 8000 (apenas localhost)
- **Função**: API REST
- **Endpoints**: /api/v1/*

### 2. React Frontend
- **Porta**: 3000 (apenas localhost)
- **Função**: Interface web
- **Build**: Vite otimizado

---

## 🌐 Acessar o Sistema

| Serviço | URL | Acesso |
|---------|-----|--------|
| **Frontend** | http://localhost | Local |
| **API** | http://localhost:8000/api | Local |
| **Swagger** | http://localhost:8000/docs | Local |
| **ReDoc** | http://localhost:8000/redoc | Local |

---

## 🎮 Comandos Disponíveis

### Windows
```cmd
start.bat start    # Iniciar sistema
start.bat stop     # Parar sistema
start.bat restart  # Reiniciar sistema
start.bat logs     # Ver logs
start.bat status   # Ver status
start.bat clean    # Limpar tudo (remove dados)
```

### Mac/Linux
```bash
./start.sh start    # Iniciar sistema
./start.sh stop     # Parar sistema
./start.sh restart  # Reiniciar sistema
./start.sh logs     # Ver logs
./start.sh status   # Ver status
./start.sh clean    # Limpar tudo (remove dados)
```

### Ver Logs de um Serviço Específico

```bash
# Windows
start.bat logs backend
start.bat logs frontend
# Mac/Linux
./start.sh logs backend
./start.sh logs frontend
```

---

## 🔧 Configuração

### Arquivo .env

Criado automaticamente na primeira execução com valores padrão:

```env
ENVIRONMENT=dev
DEBUG=false
DB_USER=biotech_user
DB_PASSWORD=biotech_password
SECRET_KEY=change-me-in-production-min-32-chars
```

Para alterar, edite `deploy/.env` e reinicie:

```bash
start.bat restart  # Windows
./start.sh restart # Mac/Linux
```

### Gerar SECRET_KEY Seguro

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -base64 32
```

---

## 💾 Backup Automático

Banco de dados é automaticamente feito backup diariamente em:

```
deploy/backups/backup-YYYYMMDD-HHMMSS.sql
```

Retenção: 30 dias

### Backup Manual

```bash
cp biotecpredict.db backup/biotecpredict-$(date +%Y%m%d-%H%M%S).db
```

### Restaurar Backup

```bash
cp backup/biotecpredict-YYYYMMDD-HHMMSS.db biotecpredict.db
```

---

## 🛑 Parar o Sistema

### Parar temporariamente (dados preservados)

```bash
start.bat stop     # Windows
./start.sh stop    # Mac/Linux
```

Para reiniciar:

```bash
start.bat start    # Windows
./start.sh start   # Mac/Linux
```

### Remover tudo (incluindo dados)

```bash
start.bat clean    # Windows
./start.sh clean   # Mac/Linux
```

⚠️ **CUIDADO**: Isso remove todos os dados!

---

## 📋 Checklist de Deploy

- [ ] Docker Desktop instalado
- [ ] Arquivo `.env` criado
- [ ] Executado `start.bat` (ou `start.sh`)
- [ ] Aguardado 20-30 segundos
- [ ] Acessado http://localhost
- [ ] Verificado status em http://localhost:8000/health
- [ ] Logs verificados (sem erros)
- [ ] Backup automático configurado

---

## 🔐 Segurança

### Portas Expostas
- ✅ 80 (HTTP) - Frontend
- ❌ 8000 (Backend) - Apenas localhost
- ✅ SQLite - arquivo local (sem porta de rede exposta)

### Security Headers
- ✅ CORS configurado
- ✅ Rate limiting (100 req/min por IP)

---

## 🚀 Próximos Passos

1. ✅ Clonar repositório
2. ✅ Configurar `.env`
3. ✅ Executar `start.bat` (ou `start.sh`)
4. ✅ Acessar http://localhost
5. ✅ Fazer upload de CSV
6. ✅ Visualizar resultados

---

**Versão**: 0.1.0  
**Data**: 23 de Maio de 2026  
**Status**: ✅ Deploy 100% Funcional (Local)