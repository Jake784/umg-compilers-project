import re

def tokenize(source_code):
    # 1. Definición de la gramática regular (Expresiones Regulares)
    # El orden es VITAL: Las palabras reservadas deben ir antes que los identificadores.
    # (?P<name>pattern) crea un "grupo con nombre" para saber qué token hizo match.
    token_specification = [
        ('KEYWORD',      r'\b(public|class|static|void|int|String|if|else|while|return)\b'),
        ('IDENTIFIER',   r'[a-zA-Z_][a-zA-Z0-9_]*'),
        ('NUMBER',       r'\d+(\.\d*)?'),                 # Enteros y decimales
        ('OPERATOR',     r'[+\-*/=<>!]+'),
        ('PUNCTUATION',  r'[{}();,]'),
        ('STRING_LIT',   r'"[^"]*"'),                     # Cadenas de texto: "hola"
        ('COMMENT',      r'//.*|/\*[\s\S]*?\*/'),         # Comentarios de una o múltiples líneas
        ('NEWLINE',      r'\n'),                          # Salto de línea (para contar)
        ('SKIP',         r'[ \t]+'),                      # Espacios y tabs (se ignoran)
        ('MISMATCH',     r'.'),                           # Cualquier otro carácter (Error)
    ]

    # Unimos todas las ER con el operador OR (|) lógico
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)

    # Variables de estado
    line_num = 1
    line_start = 0
    symbol_table = {} # Diccionario para el requerimiento #4 (Tabla de Símbolos)
    found_tokens = []

    # 2. Procesamiento (El bucle del Scanner)
    # re.finditer recorre el texto y devuelve objetos "match" cada vez que una ER coincide
    for match_obj in re.finditer(tok_regex, source_code):
        token_type = match_obj.lastgroup  # Nombre del grupo que hizo match (ej. 'KEYWORD')
        value = match_obj.group()         # El texto exacto que hizo match (ej. 'public')
        
        # Cálculo exacto de la columna
        column = match_obj.start() - line_start + 1

        if token_type == 'NEWLINE':
            line_start = match_obj.end() # Reiniciamos el contador de columnas para la nueva línea
            line_num += 1
            continue
        elif token_type == 'SKIP' or token_type == 'COMMENT':
            # Elementos irrelevantes que se eliminan (Requerimiento de la fase)
            continue
        elif token_type == 'MISMATCH':
            # 3. Manejo de Errores Léxicos
            print(f"❌ Lexical Error: Invalid character '{value}' at line {line_num}, column {column}")
            continue

        # Guardar el token válido
        found_tokens.append((token_type, value, line_num, column))

        # 4. Tabla de Símbolos
        # Solo almacenamos los identificadores (nombres de variables, clases, métodos)
        if token_type == 'IDENTIFIER' and value not in symbol_table:
            symbol_table[value] = {
                'first_appearance_line': line_num
                # Aquí en el futuro tu analizador sintáctico/semántico agregará el tipo de dato
            }

    return found_tokens, symbol_table

# ==========================================
# Pruebas del Scanner / Scanner Tests
# ==========================================
if __name__ == '__main__':
    # Simulamos el contenido de un archivo .txt con código Java
    sample_java_code = """
    public class HelloWorld {
        public static void main(String[] args) {
            int number = 10;
            // Esto es un comentario que debe ser ignorado
            int result = number + 20;
            
            $invalidCharacter = 5; 
        }
    }
    """

    print("Starting lexical analysis...\n")
    tokens, sym_table = tokenize(sample_java_code)

    print("\n--- FOUND TOKENS ---")
    print(f"{'TYPE':<15} | {'VALUE':<15} | {'LINE':<5} | {'COLUMN'}")
    print("-" * 50)
    for t in tokens:
        print(f"{t[0]:<15} | {t[1]:<15} | {t[2]:<5} | {t[3]}")

    print("\n--- SYMBOL TABLE (Initial Structure) ---")
    for identifier, info in sym_table.items():
        print(f"ID: {identifier:<15} -> {info}")