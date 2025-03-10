#!/usr/bin/env python3
"""
Script to fix common linting issues in the codebase.
Run with: python fix_linting.py
"""
import re
from pathlib import Path

# Regex patterns
TYPING_LIST = re.compile(r'from typing import (?:[^,]*,\s*)?List(?:[^,]*,\s*)?')
TYPING_DICT = re.compile(r'from typing import (?:[^,]*,\s*)?Dict(?:[^,]*,\s*)?')
TYPING_OPTIONAL = re.compile(r'from typing import (?:[^,]*,\s*)?Optional(?:[^,]*,\s*)?')
LIST_ANNOTATION = re.compile(r'List\[(.*?)\]')
DICT_ANNOTATION = re.compile(r'Dict\[(.*?), (.*?)\]')
OPTIONAL_ANNOTATION = re.compile(r'Optional\[(.*?)\]')
UNION_ANNOTATION = re.compile(r'Union\[(.*?), (.*?)\]')
DEPENDS_IN_PARAMS = re.compile(r'(\w+):\s*(\w+)\s*=\s*Depends\(([^)]*)\)')

def fix_file(file_path):
    """Fix linting issues in a single file."""
    with open(file_path) as f:
        content = f.read()
    
    # Fix typing imports
    if 'from typing import' in content:
        # Replace List with list
        content = TYPING_LIST.sub(lambda m: m.group().replace('List', 'list'), content)
        # Replace Dict with dict
        content = TYPING_DICT.sub(lambda m: m.group().replace('Dict', 'dict'), content)
        # Replace Optional with | None notation
        content = TYPING_OPTIONAL.sub(lambda m: m.group().replace('Optional', ''), content)
    
    # Fix type annotations
    content = LIST_ANNOTATION.sub(r'list[\1]', content)
    content = DICT_ANNOTATION.sub(r'dict[\1, \2]', content)
    content = OPTIONAL_ANNOTATION.sub(r'\1 | None', content)
    content = UNION_ANNOTATION.sub(r'\1 | \2', content)
    
    # Fix FastAPI Depends issue (this is more complex and might need manual review)
    # content = DEPENDS_IN_PARAMS.sub(r'\1: Annotated[\2, Depends(\3)]', content)
    
    # Fix comparison to True
    content = content.replace(' is True', ' is True')
    
    with open(file_path, 'w') as f:
        f.write(content)

def main():
    """Find and fix Python files."""
    python_files = list(Path('.').glob('**/*.py'))
    for py_file in python_files:
        print(f"Fixing {py_file}")
        fix_file(py_file)

if __name__ == "__main__":
    main() 