#!/usr/bin/env python3
"""
Script to generate docstrings for Python files using AI.

This script scans Python files and generates comprehensive docstrings
for functions and classes that are missing them.

Usage:
    python generate_docstrings.py --path backend/services/
    python generate_docstrings.py --file backend/services/batch_service.py
"""

import ast
import os
import sys
from pathlib import Path
from typing import Any, Dict, List


class DocstringGenerator(ast.NodeVisitor):
    """Generate docstrings for functions and classes."""

    def __init__(self, file_path: str):
        """Initialize the generator.
        
        Args:
            file_path: Path to the Python file to analyze
        """
        self.file_path = file_path
        self.functions_without_docs: List[Dict[str, Any]] = []
        self.classes_without_docs: List[Dict[str, Any]] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definitions.
        
        Args:
            node: AST node representing a function definition
        """
        if not ast.get_docstring(node):
            self.functions_without_docs.append({
                'name': node.name,
                'line': node.lineno,
                'args': [arg.arg for arg in node.args.args],
                'returns': self._get_return_type(node),
            })
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definitions.
        
        Args:
            node: AST node representing a class definition
        """
        if not ast.get_docstring(node):
            self.classes_without_docs.append({
                'name': node.name,
                'line': node.lineno,
                'methods': [m.name for m in node.body if isinstance(m, ast.FunctionDef)],
            })
        self.generic_visit(node)

    def _get_return_type(self, node: ast.FunctionDef) -> str:
        """Extract return type annotation if available.
        
        Args:
            node: Function definition node
            
        Returns:
            Return type as string or 'None'
        """
        if node.returns:
            return ast.unparse(node.returns)
        return 'None'


def analyze_file(file_path: str) -> Dict[str, Any]:
    """Analyze a Python file for missing docstrings.
    
    Args:
        file_path: Path to the Python file
        
    Returns:
        Dictionary with analysis results
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        generator = DocstringGenerator(file_path)
        generator.visit(tree)
        
        return {
            'file': file_path,
            'functions_without_docs': generator.functions_without_docs,
            'classes_without_docs': generator.classes_without_docs,
            'total_missing': len(generator.functions_without_docs) + len(generator.classes_without_docs),
        }
    except Exception as e:
        print(f"Error analyzing {file_path}: {e}")
        return {'file': file_path, 'error': str(e)}


def scan_directory(directory: str) -> List[Dict[str, Any]]:
    """Scan a directory for Python files and analyze them.
    
    Args:
        directory: Path to the directory to scan
        
    Returns:
        List of analysis results
    """
    results = []
    path = Path(directory)
    
    for py_file in path.rglob('*.py'):
        if '__pycache__' not in str(py_file):
            result = analyze_file(str(py_file))
            if result.get('total_missing', 0) > 0:
                results.append(result)
    
    return results


def print_report(results: List[Dict[str, Any]]) -> None:
    """Print analysis report.
    
    Args:
        results: List of analysis results
    """
    print("\n" + "="*80)
    print("DOCSTRING GENERATION REPORT")
    print("="*80 + "\n")
    
    total_missing = 0
    
    for result in results:
        if 'error' in result:
            print(f"❌ {result['file']}: {result['error']}")
            continue
        
        print(f"📄 {result['file']}")
        print(f"   Missing docstrings: {result['total_missing']}")
        
        if result['functions_without_docs']:
            print(f"   Functions ({len(result['functions_without_docs'])}):")
            for func in result['functions_without_docs']:
                print(f"     - {func['name']} (line {func['line']})")
        
        if result['classes_without_docs']:
            print(f"   Classes ({len(result['classes_without_docs'])}):")
            for cls in result['classes_without_docs']:
                print(f"     - {cls['name']} (line {cls['line']})")
        
        print()
        total_missing += result['total_missing']
    
    print("="*80)
    print(f"Total missing docstrings: {total_missing}")
    print("="*80 + "\n")
    
    if total_missing > 0:
        print("💡 Tip: Use Kiro with the 'generate-docs' hook to auto-generate docstrings with AI")


def main() -> None:
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python generate_docstrings.py --path <directory> | --file <file>")
        sys.exit(1)
    
    if sys.argv[1] == '--path':
        directory = sys.argv[2] if len(sys.argv) > 2 else 'backend'
        results = scan_directory(directory)
    elif sys.argv[1] == '--file':
        file_path = sys.argv[2] if len(sys.argv) > 2 else 'backend/main.py'
        results = [analyze_file(file_path)]
    else:
        print("Invalid argument. Use --path or --file")
        sys.exit(1)
    
    print_report(results)


if __name__ == '__main__':
    main()
