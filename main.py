import sys
import os

from core.scanner import Scanner

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 main.py <source_file.txt>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"Error: The file '{file_path}' was not found.")
        sys.exit(1)

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            source_code = file.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    print(f"Starting lexical analysis for: {file_path}...\n")
    
    scanner = Scanner(source_code)
    scanner.analyze()
    scanner.generate_reports()