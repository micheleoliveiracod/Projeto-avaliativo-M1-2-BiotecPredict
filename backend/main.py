"""
BiotecPredict - Plataforma de Manufatura Preditiva
Entry point da aplicação FastAPI
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Criar aplicação FastAPI
app = FastAPI(
    title="BiotecPredict",
    description="Plataforma de Manufatura Preditiva com Machine Learning",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["Health"])
def health_check():
    """
    Verificar saúde da aplicação.
    
    Returns:
        dict: Status da aplicação
    """
    return {
        "status": "ok",
        "service": "BiotecPredict",
        "version": "0.1.0"
    }


@app.get("/", tags=["Root"])
def root():
    """
    Endpoint raiz da API.
    
    Returns:
        dict: Informações da API
    """
    return {
        "message": "BiotecPredict API",
        "version": "0.1.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
