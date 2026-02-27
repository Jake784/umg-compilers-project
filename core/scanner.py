import re
import os

from core.token_model import Token

class Scanner:
    def __init__(self, source_code):
        self.source_code = source_code
        self.tokens = []
        self.symbol_table = {}
        self.lexical_errors = []
        
        self.token_specification = [
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
        self.tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self.token_specification)

    def analyze(self):
        line_num = 1
        line_start = 0

        for match_obj in re.finditer(self.tok_regex, self.source_code):
            token_type = match_obj.lastgroup
            value = match_obj.group()
            column = match_obj.start() - line_start + 1

            if token_type == 'NEWLINE':
                line_start = match_obj.end()
                line_num += 1
                continue

            elif token_type == 'SKIP' or token_type == 'COMMENT':
                if token_type == 'COMMENT':
                    newlines_in_comment = value.count('\n')
                    if newlines_in_comment > 0:
                        line_num += newlines_in_comment
                        line_start = match_obj.start() + value.rfind('\n') + 1
                continue

            elif token_type == 'MISMATCH':
                error_msg = f"Lexical Error: Invalid character '{value}' at line {line_num}, column {column}"
                print(f"{error_msg}")
                self.lexical_errors.append(error_msg)
                continue

            new_token = Token(token_type, value, line_num, column)
            self.tokens.append(new_token)

            if token_type == 'IDENTIFIER' and value not in self.symbol_table:
                self.symbol_table[value] = {
                    'type': 'Undefined',
                    'line': line_num,
                    'column': column
                }

    def generate_reports(self, report_dir='report-generation'):
        os.makedirs(report_dir, exist_ok=True)
        
        tokens_path = os.path.join(report_dir, 'tokens_report.txt')
        with open(tokens_path, 'w', encoding='utf-8') as f:
            f.write(f"{'TYPE':<15} | {'VALUE':<20} | {'LINE':<5} | {'COLUMN'}\n")
            f.write("-" * 60 + "\n")
            for t in self.tokens:
                f.write(f"{t.type:<15} | {t.value:<20} | {t.line:<5} | {t.column}\n")
                
        sym_table_path = os.path.join(report_dir, 'symbol_table_report.txt')
        with open(sym_table_path, 'w', encoding='utf-8') as f:
            f.write(f"{'IDENTIFIER':<20} | {'FIRST APPEARANCE (LINE)'}\n")
            f.write("-" * 50 + "\n")
            for identifier, info in self.symbol_table.items():
                f.write(f"{identifier:<20} | {info['first_appearance_line']}\n")

        errors_path = os.path.join(report_dir, 'errors_report.txt')
        if self.lexical_errors:
            with open(errors_path, 'w', encoding='utf-8') as f:
                f.write("--- LEXICAL ERRORS DETECTED ---\n")
                for error in self.lexical_errors:
                    f.write(error + "\n")
            print(f"Lexical errors found. Check '{errors_path}' for details.")
        else:
            if os.path.exists(errors_path):
                os.remove(errors_path)
            print("No lexical errors found.")

        print(f"\nAnalysis complete! Check the generated .txt report files in your '{report_dir}/' folder.")