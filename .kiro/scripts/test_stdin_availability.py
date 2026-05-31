#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de teste para validar disponibilidade de stdin no contexto do hook Kiro.

Este script testa se stdin está disponível quando o hook promptSubmit é disparado.
Ele valida múltiplas estratégias de captura de conteúdo do prompt.

Uso:
    python3 .kiro/scripts/test_stdin_availability.py

Resultado:
    Gera relatório em .kiro/reports/stdin_availability_report.md
"""

import os
import sys
import subprocess
import json
from datetime import datetime


def test_environment_variables():
    """
    Testa se variáveis de ambiente estão disponíveis.
    
    Returns:
        dict: Resultado do teste com status e detalhes.
    """
    result = {
        'test': 'Environment Variables',
        'status': 'UNKNOWN',
        'details': {},
        'timestamp': datetime.now().isoformat()
    }
    
    # Verifica USER_PROMPT
    user_prompt = os.environ.get('USER_PROMPT')
    result['details']['USER_PROMPT'] = {
        'available': user_prompt is not None,
        'value': user_prompt[:50] + '...' if user_prompt and len(user_prompt) > 50 else user_prompt
    }
    
    # Verifica KIRO_PROMPT
    kiro_prompt = os.environ.get('KIRO_PROMPT')
    result['details']['KIRO_PROMPT'] = {
        'available': kiro_prompt is not None,
        'value': kiro_prompt[:50] + '...' if kiro_prompt and len(kiro_prompt) > 50 else kiro_prompt
    }
    
    # Status geral
    if user_prompt or kiro_prompt:
        result['status'] = 'PASS'
    else:
        result['status'] = 'FAIL'
    
    return result


def test_stdin_availability():
    """
    Testa se stdin está disponível.
    
    Returns:
        dict: Resultado do teste com status e detalhes.
    """
    result = {
        'test': 'stdin Availability',
        'status': 'UNKNOWN',
        'details': {},
        'timestamp': datetime.now().isoformat()
    }
    
    # Verifica se stdin é TTY
    is_tty = sys.stdin.isatty()
    result['details']['is_tty'] = is_tty
    
    # Verifica se stdin é readable
    try:
        is_readable = sys.stdin.readable()
        result['details']['is_readable'] = is_readable
    except Exception as e:
        result['details']['is_readable'] = f'Error: {str(e)}'
    
    # Verifica se stdin tem dados disponíveis
    try:
        # Tenta ler sem bloquear (não funciona em todos os sistemas)
        import select
        if hasattr(select, 'select'):
            ready, _, _ = select.select([sys.stdin], [], [], 0)
            has_data = bool(ready)
            result['details']['has_data_available'] = has_data
        else:
            result['details']['has_data_available'] = 'N/A (select não disponível)'
    except Exception as e:
        result['details']['has_data_available'] = f'Error: {str(e)}'
    
    # Status geral
    if is_tty:
        result['status'] = 'FAIL'
        result['details']['reason'] = 'stdin é TTY (terminal interativo) - não há dados disponíveis'
    elif result['details'].get('is_readable'):
        result['status'] = 'PASS'
        result['details']['reason'] = 'stdin é readable e não é TTY'
    else:
        result['status'] = 'UNKNOWN'
        result['details']['reason'] = 'Não foi possível determinar status de stdin'
    
    return result


def test_command_line_arguments():
    """
    Testa se argumentos de linha de comando estão disponíveis.
    
    Returns:
        dict: Resultado do teste com status e detalhes.
    """
    result = {
        'test': 'Command Line Arguments',
        'status': 'UNKNOWN',
        'details': {},
        'timestamp': datetime.now().isoformat()
    }
    
    # Verifica sys.argv
    result['details']['sys.argv'] = sys.argv
    result['details']['argc'] = len(sys.argv)
    
    # Status geral
    if len(sys.argv) > 1:
        result['status'] = 'PASS'
        result['details']['reason'] = f'{len(sys.argv) - 1} argumentos disponíveis'
    else:
        result['status'] = 'FAIL'
        result['details']['reason'] = 'Nenhum argumento de linha de comando disponível'
    
    return result


def test_hook_context():
    """
    Testa o contexto do hook (variáveis de ambiente específicas do Kiro).
    
    Returns:
        dict: Resultado do teste com status e detalhes.
    """
    result = {
        'test': 'Hook Context (Kiro)',
        'status': 'UNKNOWN',
        'details': {},
        'timestamp': datetime.now().isoformat()
    }
    
    # Variáveis de ambiente que podem estar disponíveis no contexto do hook
    kiro_env_vars = [
        'KIRO_HOOK_TYPE',
        'KIRO_EVENT_TYPE',
        'KIRO_PROMPT',
        'KIRO_USER_PROMPT',
        'KIRO_CONTEXT',
        'KIRO_WORKSPACE',
        'KIRO_IDE_VERSION'
    ]
    
    available_vars = {}
    for var in kiro_env_vars:
        value = os.environ.get(var)
        if value:
            available_vars[var] = value[:50] + '...' if len(value) > 50 else value
    
    result['details']['available_kiro_vars'] = available_vars
    result['details']['total_available'] = len(available_vars)
    
    # Status geral
    if available_vars:
        result['status'] = 'PASS'
        result['details']['reason'] = f'{len(available_vars)} variáveis Kiro disponíveis'
    else:
        result['status'] = 'FAIL'
        result['details']['reason'] = 'Nenhuma variável Kiro específica disponível'
    
    return result


def test_file_descriptors():
    """
    Testa os file descriptors disponíveis.
    
    Returns:
        dict: Resultado do teste com status e detalhes.
    """
    result = {
        'test': 'File Descriptors',
        'status': 'UNKNOWN',
        'details': {},
        'timestamp': datetime.now().isoformat()
    }
    
    # Verifica file descriptors padrão
    fds = {
        'stdin (0)': os.fstat(0) if os.fstat(0) else None,
        'stdout (1)': os.fstat(1) if os.fstat(1) else None,
        'stderr (2)': os.fstat(2) if os.fstat(2) else None,
    }
    
    result['details']['file_descriptors'] = {}
    for name, fd in fds.items():
        try:
            result['details']['file_descriptors'][name] = 'Available'
        except Exception as e:
            result['details']['file_descriptors'][name] = f'Error: {str(e)}'
    
    result['status'] = 'PASS'
    return result


def generate_report(tests_results):
    """
    Gera relatório em Markdown com resultados dos testes.
    
    Args:
        tests_results (list): Lista de resultados dos testes.
    
    Returns:
        str: Relatório formatado em Markdown.
    """
    report = """# Relatório de Disponibilidade de stdin - Kiro Hook

## Resumo Executivo

Este relatório valida se stdin está disponível no contexto do hook `promptSubmit` do Kiro.
A disponibilidade de stdin é crítica para determinar se o conteúdo do prompt pode ser capturado
automaticamente via stdin ou se precisamos de outras estratégias (variáveis de ambiente, argumentos).

---

## Resultados dos Testes

"""
    
    # Resumo dos testes
    passed = sum(1 for t in tests_results if t['status'] == 'PASS')
    failed = sum(1 for t in tests_results if t['status'] == 'FAIL')
    unknown = sum(1 for t in tests_results if t['status'] == 'UNKNOWN')
    
    report += f"""### Status Geral
- ✅ Passou: {passed}
- ❌ Falhou: {failed}
- ❓ Desconhecido: {unknown}
- **Total**: {len(tests_results)}

---

"""
    
    # Detalhes de cada teste
    for test in tests_results:
        status_icon = '✅' if test['status'] == 'PASS' else '❌' if test['status'] == 'FAIL' else '❓'
        report += f"""### {status_icon} {test['test']}

**Status**: {test['status']}

**Detalhes**:
```json
{json.dumps(test['details'], indent=2, ensure_ascii=False)}
```

**Timestamp**: {test['timestamp']}

---

"""
    
    return report


def main():
    """
    Função principal que executa todos os testes.
    """
    print("🔍 Iniciando testes de disponibilidade de stdin no contexto do hook Kiro...")
    print()
    
    # Executa todos os testes
    tests_results = [
        test_environment_variables(),
        test_stdin_availability(),
        test_command_line_arguments(),
        test_hook_context(),
        test_file_descriptors(),
    ]
    
    # Gera relatório
    report = generate_report(tests_results)
    
    # Cria diretório de relatórios se não existir
    os.makedirs('.kiro/reports', exist_ok=True)
    
    # Salva relatório
    report_file = '.kiro/reports/stdin_availability_report.md'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Relatório salvo em: {report_file}")
    print()
    print("📊 Resumo dos Testes:")
    print()
    
    for test in tests_results:
        status_icon = '✅' if test['status'] == 'PASS' else '❌' if test['status'] == 'FAIL' else '❓'
        print(f"{status_icon} {test['test']}: {test['status']}")
        if 'reason' in test['details']:
            print(f"   └─ {test['details']['reason']}")
    
    print()
    print("📝 Análise Completa:")
    print(report)


if __name__ == '__main__':
    main()
