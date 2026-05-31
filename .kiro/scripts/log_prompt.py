"""
Script para registrar prompts em log.
Usado pelo sistema de automação do Kiro.
"""

import logging
from datetime import datetime
from pathlib import Path

# Configurar logging
log_dir = Path(".kiro/logs")
log_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("kiro_prompt")
handler = logging.FileHandler(log_dir / "prompts.log")
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


def log_prompt(prompt_text: str, context: dict = None):
    """
    Registra um prompt em log.
    
    Args:
        prompt_text: Texto do prompt
        context: Contexto adicional (opcional)
    """
    try:
        message = f"Prompt: {prompt_text}"
        if context:
            message += f" | Context: {context}"
        logger.info(message)
    except Exception as e:
        logger.error(f"Erro ao registrar prompt: {e}")


if __name__ == "__main__":
    log_prompt("Script de logging inicializado")
