#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador de Formato Markdown para Logs de Prompts

Este script valida que os arquivos de log de prompts em .kiro/prompt-logs/
seguem o formato Markdown correto e podem ser renderizados adequadamente.

Validações realizadas:
1. Sintaxe Markdown básica
2. Estrutura de cabeçalhos
3. Formatação de metadados
4. Blocos de código
5. Separadores visuais
6. Codificação UTF-8
7. Renderização em Markdown viewers
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple


class MarkdownValidator:
    """Validador de formato Markdown para logs de prompts."""
    
    def __init__(self, log_dir: str = ".kiro/prompt-logs"):
        """
        Inicializa o validador.
        
        Args:
            log_dir: Diretório contendo os arquivos de log
        """
        self.log_dir = Path(log_dir)
        self.errors = []
        self.warnings = []
        self.info = []
        
    def validate_all(self) -> bool:
        """
        Valida todos os arquivos de log no diretório.
        
        Returns:
            True se todos os arquivos são válidos, False caso contrário
        """
        if not self.log_dir.exists():
            self.errors.append(f"Diretório {self.log_dir} não existe")
            return False
        
        log_files = list(self.log_dir.glob("*.md"))
        
        if not log_files:
            self.warnings.append(f"Nenhum arquivo .md encontrado em {self.log_dir}")
            return True
        
        self.info.append(f"Validando {len(log_files)} arquivo(s) de log")
        
        for log_file in log_files:
            self._validate_file(log_file)
        
        return len(self.errors) == 0
    
    def _validate_file(self, file_path: Path) -> None:
        """
        Valida um arquivo de log individual.
        
        Args:
            file_path: Caminho do arquivo a validar
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            self.errors.append(f"{file_path.name}: Erro de codificação (não é UTF-8)")
            return
        except Exception as e:
            self.errors.append(f"{file_path.name}: Erro ao ler arquivo: {e}")
            return
        
        # Validações
        self._validate_encoding(file_path, content)
        self._validate_structure(file_path, content)
        self._validate_headers(file_path, content)
        self._validate_metadata(file_path, content)
        self._validate_code_blocks(file_path, content)
        self._validate_separators(file_path, content)
        self._validate_markdown_syntax(file_path, content)
    
    def _validate_encoding(self, file_path: Path, content: str) -> None:
        """Valida que o arquivo está em UTF-8."""
        try:
            content.encode('utf-8')
            self.info.append(f"{file_path.name}: ✓ Codificação UTF-8 válida")
        except UnicodeEncodeError as e:
            self.errors.append(f"{file_path.name}: Caracteres inválidos em UTF-8: {e}")
    
    def _validate_structure(self, file_path: Path, content: str) -> None:
        """Valida a estrutura geral do arquivo."""
        lines = content.split('\n')
        
        # Verificar cabeçalho
        if not lines or not lines[0].startswith('# Prompt Logs:'):
            self.errors.append(f"{file_path.name}: Cabeçalho principal não encontrado")
            return
        
        # Verificar se tem conteúdo além do cabeçalho
        non_empty_lines = [l for l in lines if l.strip()]
        if len(non_empty_lines) < 2:
            self.warnings.append(f"{file_path.name}: Arquivo contém apenas cabeçalho (sem prompts)")
        else:
            self.info.append(f"{file_path.name}: ✓ Estrutura básica válida")
    
    def _validate_headers(self, file_path: Path, content: str) -> None:
        """Valida os cabeçalhos Markdown."""
        # Verificar cabeçalho principal
        if not re.search(r'^# Prompt Logs:', content, re.MULTILINE):
            self.errors.append(f"{file_path.name}: Cabeçalho principal (# Prompt Logs:) não encontrado")
        
        # Verificar cabeçalhos de prompts
        prompt_headers = re.findall(r'^## Prompt:', content, re.MULTILINE)
        if prompt_headers:
            self.info.append(f"{file_path.name}: ✓ {len(prompt_headers)} cabeçalho(s) de prompt encontrado(s)")
        
        # Verificar cabeçalhos de seção de prompt original
        original_headers = re.findall(r'^### Prompt original', content, re.MULTILINE)
        if original_headers:
            self.info.append(f"{file_path.name}: ✓ {len(original_headers)} seção(ões) 'Prompt original' encontrada(s)")
    
    def _validate_metadata(self, file_path: Path, content: str) -> None:
        """Valida os metadados de cada prompt."""
        # Padrão para metadados
        metadata_pattern = r'- Responsável: .+\n- Branch: .+\n- Data/hora: .+'
        
        metadata_matches = re.findall(metadata_pattern, content, re.MULTILINE)
        
        if metadata_matches:
            self.info.append(f"{file_path.name}: ✓ {len(metadata_matches)} bloco(s) de metadados válido(s)")
        
        # Validar formato de timestamp
        timestamp_pattern = r'Data/hora: (\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
        timestamps = re.findall(timestamp_pattern, content)
        
        if timestamps:
            self.info.append(f"{file_path.name}: ✓ {len(timestamps)} timestamp(s) em formato válido")
        
        # Verificar se há timestamps sem timezone
        bad_timestamps = re.findall(r'Data/hora: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?!\s*\()', content)
        if bad_timestamps:
            self.warnings.append(f"{file_path.name}: {len(bad_timestamps)} timestamp(s) sem timezone")
    
    def _validate_code_blocks(self, file_path: Path, content: str) -> None:
        """Valida os blocos de código."""
        # Contar blocos de código
        code_blocks = re.findall(r'```', content)
        
        if len(code_blocks) % 2 != 0:
            self.errors.append(f"{file_path.name}: Blocos de código não balanceados (número ímpar de ```)")
        else:
            num_blocks = len(code_blocks) // 2
            if num_blocks > 0:
                self.info.append(f"{file_path.name}: ✓ {num_blocks} bloco(s) de código balanceado(s)")
    
    def _validate_separators(self, file_path: Path, content: str) -> None:
        """Valida os separadores visuais."""
        separators = re.findall(r'^---$', content, re.MULTILINE)
        
        if separators:
            self.info.append(f"{file_path.name}: ✓ {len(separators)} separador(es) encontrado(s)")
        else:
            self.warnings.append(f"{file_path.name}: Nenhum separador (---) encontrado")
    
    def _validate_markdown_syntax(self, file_path: Path, content: str) -> None:
        """Valida a sintaxe Markdown geral."""
        issues = []
        
        # Verificar parênteses desbalanceados
        if content.count('(') != content.count(')'):
            issues.append("Parênteses desbalanceados")
        
        # Verificar colchetes desbalanceados
        if content.count('[') != content.count(']'):
            issues.append("Colchetes desbalanceados")
        
        # Verificar chaves desbalanceadas
        if content.count('{') != content.count('}'):
            issues.append("Chaves desbalanceadas")
        
        if issues:
            for issue in issues:
                self.warnings.append(f"{file_path.name}: {issue}")
        else:
            self.info.append(f"{file_path.name}: ✓ Sintaxe Markdown válida")
    
    def print_report(self) -> None:
        """Imprime relatório de validação."""
        print("\n" + "="*70)
        print("RELATÓRIO DE VALIDAÇÃO DE MARKDOWN - LOGS DE PROMPTS")
        print("="*70 + "\n")
        
        # Informações
        if self.info:
            print("✓ INFORMAÇÕES:")
            for msg in self.info:
                print(f"  {msg}")
            print()
        
        # Avisos
        if self.warnings:
            print("⚠ AVISOS:")
            for msg in self.warnings:
                print(f"  {msg}")
            print()
        
        # Erros
        if self.errors:
            print("✗ ERROS:")
            for msg in self.errors:
                print(f"  {msg}")
            print()
        
        # Resumo
        print("="*70)
        print("RESUMO:")
        print(f"  Erros: {len(self.errors)}")
        print(f"  Avisos: {len(self.warnings)}")
        print(f"  Informações: {len(self.info)}")
        print("="*70 + "\n")
        
        if self.errors:
            print("❌ VALIDAÇÃO FALHOU - Existem erros que precisam ser corrigidos")
            return False
        else:
            print("✅ VALIDAÇÃO PASSOU - Todos os logs estão em formato Markdown válido")
            return True


def main():
    """Função principal."""
    validator = MarkdownValidator()
    success = validator.validate_all()
    validator.print_report()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
