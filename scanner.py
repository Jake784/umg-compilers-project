import re
import sys
import os

def tokenize(source_code):
    # 1. Definición de la gramática regular / Regular Grammar Definition
    token_specification = [
        ('KEYWORD',      r'\b(public|class|static|void|int|String|if|else|while|return)\b'),
        ('COMMENT',      r'//.*|/\*[\s\S]*?\*/'),         
        ('IDENTIFIER',   r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('NUMBER',       r'\d+(\.\d*)?'),
        ('STRING_LIT',   r'"[^"]*"'),
        ('OPERATOR',     r'[+\-*/=<>!]+'),
        ('PUNCTUATION',  r'[{}();,\[\]\.]'),              
        ('NEWLINE',      r'\n'),
        ('SKIP',         r'[ \t]+'),
        ('MISMATCH',     r'.'),
    ]

    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

    line_num = 1
    line_start = 0
    symbol_table = {}
    found_tokens = []
    lexical_errors = [] 

    # 2. Procesamiento / Processing
    for match_obj in re.finditer(tok_regex, source_code):
        token_type = match_obj.lastgroup
        value = match_obj.group()
        
        column = match_obj.start() - line_start + 1

        if token_type == 'NEWLINE':
            line_start = match_obj.end()
            line_num += 1
            continue
        elif token_type == 'SKIP' or token_type == 'COMMENT':
            continue
        elif token_type == 'MISMATCH':
            # 3. Manejo de Errores Léxicos / Lexical Error Handling
            error_msg = f"Lexical Error: Invalid character '{value}' at line {line_num}, column {column}"
            print(f"{error_msg}")
            lexical_errors.append(error_msg)
            continue

        found_tokens.append((token_type, value, line_num, column))

        # 4. Tabla de Símbolos / Symbol Table
        if token_type == 'IDENTIFIER' and value not in symbol_table:
            symbol_table[value] = {
                'first_appearance_line': line_num
            }

    return found_tokens, symbol_table, lexical_errors

# ==========================================
# Ejecución del Programa / Program Execution
# ==========================================
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 scanner.py <source_file.txt>")
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
    
    tokens, sym_table, errors = tokenize(source_code)

    # ==========================================
    # Generación de Reportes / Report Generation
    # ==========================================
    
    # Definir y crear la carpeta de reportes
    report_dir = 'report-generation'
    os.makedirs(report_dir, exist_ok=True)
    
    # 1. Reporte de Tokens
    tokens_path = os.path.join(report_dir, 'tokens_report.txt')
    with open(tokens_path, 'w', encoding='utf-8') as f:
        f.write(f"{'TYPE':<15} | {'VALUE':<20} | {'LINE':<5} | {'COLUMN'}\n")
        f.write("-" * 60 + "\n")
        for t in tokens:
            f.write(f"{t[0]:<15} | {t[1]:<20} | {t[2]:<5} | {t[3]}\n")
            
    # 2. Reporte de Tabla de Símbolos
    sym_table_path = os.path.join(report_dir, 'symbol_table_report.txt')
    with open(sym_table_path, 'w', encoding='utf-8') as f:
        f.write(f"{'IDENTIFIER':<20} | {'FIRST APPEARANCE (LINE)'}\n")
        f.write("-" * 50 + "\n")
        for identifier, info in sym_table.items():
            f.write(f"{identifier:<20} | {info['first_appearance_line']}\n")

    # 3. Reporte de Errores (Solo se crea si hay errores)
    errors_path = os.path.join(report_dir, 'errors_report.txt')
    if errors:
        with open(errors_path, 'w', encoding='utf-8') as f:
            f.write("--- LEXICAL ERRORS DETECTED ---\n")
            for error in errors:
                f.write(error + "\n")
        print(f"Lexical errors found. Check '{errors_path}' for details.")
    else:
        # Borrar el reporte de errores anterior si el código ya no tiene errores
        if os.path.exists(errors_path):
            os.remove(errors_path)
        print("No lexical errors found.")

    print(f"\nAnalysis complete! Check the generated .txt report files in your '{report_dir}/' folder.")