#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Benchmark Script for log_prompt.py Performance Testing

Mede o tempo de execução do script de logging de prompts para validar
que ele não bloqueia significativamente a execução do Kiro.

Requisito: Tempo de execução < 100ms (ideal < 50ms)
"""

import subprocess
import time
import statistics
import json
from pathlib import Path
from datetime import datetime
import sys

# Configuração
ITERATIONS = 30  # Mínimo 30 iterações conforme requisito
SCRIPT_PATH = Path(__file__).parent / "log_prompt.py"
REPORT_DIR = Path(__file__).parent.parent / "reports"
REPORT_FILE = REPORT_DIR / "performance_report.md"
JSON_REPORT_FILE = REPORT_DIR / "performance_report.json"

# Requisitos de performance
REQUIREMENT_MS = 100  # Requisito: < 100ms
IDEAL_MS = 50  # Ideal: < 50ms


def run_benchmark():
    """Executa o benchmark do script de logging."""
    
    print(f"🚀 Iniciando benchmark do script log_prompt.py")
    print(f"📊 Iterações: {ITERATIONS}")
    print(f"⏱️  Requisito: < {REQUIREMENT_MS}ms")
    print(f"✨ Ideal: < {IDEAL_MS}ms")
    print("-" * 60)
    
    execution_times = []
    
    for i in range(1, ITERATIONS + 1):
        try:
            # Medir tempo de execução
            start_time = time.perf_counter()
            
            # Executar script com timeout de 5 segundos
            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), "--test"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            end_time = time.perf_counter()
            elapsed_ms = (end_time - start_time) * 1000
            execution_times.append(elapsed_ms)
            
            # Status visual
            status = "✅" if elapsed_ms < REQUIREMENT_MS else "⚠️"
            print(f"[{i:2d}/{ITERATIONS}] {status} {elapsed_ms:7.2f}ms", end="")
            
            if result.returncode != 0:
                print(f" ❌ ERRO: {result.stderr[:50]}")
            else:
                print()
            
        except subprocess.TimeoutExpired:
            print(f"[{i:2d}/{ITERATIONS}] ❌ TIMEOUT (>5s)")
            execution_times.append(5000)  # Registrar como 5000ms
        except Exception as e:
            print(f"[{i:2d}/{ITERATIONS}] ❌ ERRO: {str(e)[:50]}")
            execution_times.append(None)
    
    return execution_times


def calculate_statistics(times):
    """Calcula estatísticas dos tempos de execução."""
    
    # Filtrar valores válidos
    valid_times = [t for t in times if t is not None]
    
    if not valid_times:
        return None
    
    stats = {
        "total_iterations": len(times),
        "successful_iterations": len(valid_times),
        "failed_iterations": len(times) - len(valid_times),
        "min_ms": min(valid_times),
        "max_ms": max(valid_times),
        "mean_ms": statistics.mean(valid_times),
        "median_ms": statistics.median(valid_times),
        "stdev_ms": statistics.stdev(valid_times) if len(valid_times) > 1 else 0,
        "p95_ms": sorted(valid_times)[int(len(valid_times) * 0.95)] if len(valid_times) > 1 else valid_times[0],
        "p99_ms": sorted(valid_times)[int(len(valid_times) * 0.99)] if len(valid_times) > 1 else valid_times[0],
    }
    
    return stats


def generate_markdown_report(stats):
    """Gera relatório em formato Markdown."""
    
    if not stats:
        return "# Relatório de Performance - log_prompt.py\n\n❌ Nenhum dado disponível\n"
    
    # Determinar status
    mean_ok = stats["mean_ms"] < 100
    ideal = stats["mean_ms"] < 50
    
    status_emoji = "✅" if mean_ok else "⚠️"
    ideal_emoji = "✨" if ideal else "📊"
    
    report = f"""# Relatório de Performance - log_prompt.py

**Data/Hora:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Brasília - UTC-3)

## 📊 Resumo Executivo

{status_emoji} **Status:** {'PASSOU' if mean_ok else 'FALHOU'} no requisito (<100ms)
{ideal_emoji} **Ideal:** {'ATINGIDO' if ideal else 'NÃO ATINGIDO'} (<50ms)

## ⏱️ Estatísticas de Tempo de Execução

| Métrica | Valor | Status |
|---------|-------|--------|
| **Iterações Totais** | {stats['total_iterations']} | - |
| **Iterações Bem-sucedidas** | {stats['successful_iterations']} | ✅ |
| **Iterações Falhadas** | {stats['failed_iterations']} | {'✅' if stats['failed_iterations'] == 0 else '⚠️'} |
| **Tempo Mínimo** | {stats['min_ms']:.2f}ms | ✅ |
| **Tempo Máximo** | {stats['max_ms']:.2f}ms | {'✅' if stats['max_ms'] < 100 else '⚠️'} |
| **Tempo Médio** | {stats['mean_ms']:.2f}ms | {'✅' if stats['mean_ms'] < 100 else '⚠️'} |
| **Tempo Mediano** | {stats['median_ms']:.2f}ms | {'✅' if stats['median_ms'] < 100 else '⚠️'} |
| **Desvio Padrão** | {stats['stdev_ms']:.2f}ms | - |
| **P95** | {stats['p95_ms']:.2f}ms | {'✅' if stats['p95_ms'] < 100 else '⚠️'} |
| **P99** | {stats['p99_ms']:.2f}ms | {'✅' if stats['p99_ms'] < 100 else '⚠️'} |

## 📈 Análise

### Requisito de Performance
- **Requisito:** Tempo de execução < 100ms
- **Resultado:** {stats['mean_ms']:.2f}ms (média)
- **Status:** {'✅ PASSOU' if stats['mean_ms'] < 100 else '⚠️ FALHOU'}

### Ideal de Performance
- **Ideal:** Tempo de execução < 50ms
- **Resultado:** {stats['mean_ms']:.2f}ms (média)
- **Status:** {'✨ ATINGIDO' if stats['mean_ms'] < 50 else '📊 NÃO ATINGIDO'}

### Impacto no Kiro
- **Overhead por prompt:** {stats['mean_ms']:.2f}ms
- **Impacto perceptível:** {'❌ Não' if stats['mean_ms'] < 100 else '⚠️ Sim'}
- **Bloqueio significativo:** {'❌ Não' if stats['mean_ms'] < 200 else '⚠️ Sim'}

## 🎯 Conclusão

"""
    
    if stats['mean_ms'] < 50:
        report += f"""✨ **EXCELENTE**: O script executa em {stats['mean_ms']:.2f}ms em média, bem abaixo do requisito de 100ms.
O impacto no Kiro é negligenciável e não causa bloqueio perceptível.

**Recomendação:** ✅ Aprovado para produção. Nenhuma otimização necessária.
"""
    elif stats['mean_ms'] < 100:
        report += f"""✅ **BOM**: O script executa em {stats['mean_ms']:.2f}ms em média, dentro do requisito de 100ms.
O impacto no Kiro é mínimo e não causa bloqueio significativo.

**Recomendação:** ✅ Aprovado para produção. Considerar otimizações futuras se necessário.
"""
    else:
        report += f"""⚠️ **ATENÇÃO**: O script executa em {stats['mean_ms']:.2f}ms em média, acima do requisito de 100ms.
O impacto no Kiro pode ser perceptível em alguns casos.

**Recomendação:** 🔧 Otimizar script antes de usar em produção.
"""
    
    report += f"""

## 📝 Detalhes Técnicos

- **Script testado:** `.kiro/scripts/log_prompt.py`
- **Ambiente:** Windows 11, Python 3.11+
- **Método:** Execução direta com `subprocess.run()`
- **Timeout:** 5 segundos por iteração
- **Data do teste:** {datetime.now().strftime('%d de %B de %Y às %H:%M:%S')} (Brasília - UTC-3)

## 📚 Referências

- Requisito: Tempo de execução < 100ms
- Ideal: Tempo de execução < 50ms
- Documentação: `.kiro/steering/prompt-logging.md`
- Spec: `.kiro/specs/prompt-logging/`

---

**Versão:** 1.0.0  
**Status:** ✅ Relatório Gerado  
**Timestamp:** {datetime.now().isoformat()}
"""
    
    return report


def generate_json_report(stats, times):
    """Gera relatório em formato JSON."""
    
    if not stats:
        return {"error": "Nenhum dado disponível"}
    
    return {
        "timestamp": datetime.now().isoformat(),
        "environment": {
            "script": str(SCRIPT_PATH),
            "iterations": ITERATIONS,
            "requirement_ms": REQUIREMENT_MS,
            "ideal_ms": IDEAL_MS,
        },
        "statistics": stats,
        "all_times_ms": [t for t in times if t is not None],
        "status": {
            "passed_requirement": stats["mean_ms"] < REQUIREMENT_MS,
            "achieved_ideal": stats["mean_ms"] < IDEAL_MS,
        }
    }


def main():
    """Função principal."""
    
    # Criar diretório de relatórios se não existir
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Executar benchmark
    print()
    execution_times = run_benchmark()
    print()
    
    # Calcular estatísticas
    stats = calculate_statistics(execution_times)
    
    if not stats:
        print("❌ Erro: Nenhum dado de performance foi coletado")
        return 1
    
    # Gerar relatórios
    print("📝 Gerando relatórios...")
    
    # Relatório Markdown
    markdown_report = generate_markdown_report(stats)
    REPORT_FILE.write_text(markdown_report, encoding='utf-8')
    print(f"✅ Relatório Markdown: {REPORT_FILE}")
    
    # Relatório JSON
    json_report = generate_json_report(stats, execution_times)
    JSON_REPORT_FILE.write_text(json.dumps(json_report, indent=2), encoding='utf-8')
    print(f"✅ Relatório JSON: {JSON_REPORT_FILE}")
    
    # Exibir resumo
    print()
    print("=" * 60)
    print("📊 RESUMO DE PERFORMANCE")
    print("=" * 60)
    print(f"Tempo Médio:     {stats['mean_ms']:.2f}ms")
    print(f"Tempo Mediano:   {stats['median_ms']:.2f}ms")
    print(f"Tempo Mínimo:    {stats['min_ms']:.2f}ms")
    print(f"Tempo Máximo:    {stats['max_ms']:.2f}ms")
    print(f"Desvio Padrão:   {stats['stdev_ms']:.2f}ms")
    print(f"P95:             {stats['p95_ms']:.2f}ms")
    print(f"P99:             {stats['p99_ms']:.2f}ms")
    print("=" * 60)
    
    # Status final
    if stats['mean_ms'] < REQUIREMENT_MS:
        print(f"✅ PASSOU: Tempo médio ({stats['mean_ms']:.2f}ms) < Requisito ({REQUIREMENT_MS}ms)")
        if stats['mean_ms'] < IDEAL_MS:
            print(f"✨ IDEAL: Tempo médio ({stats['mean_ms']:.2f}ms) < Ideal ({IDEAL_MS}ms)")
        return 0
    else:
        print(f"⚠️ FALHOU: Tempo médio ({stats['mean_ms']:.2f}ms) >= Requisito ({REQUIREMENT_MS}ms)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
