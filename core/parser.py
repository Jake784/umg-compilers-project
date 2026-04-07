from core.ast_nodes import *

class SyntaxErrorLog:
    def __init__(self, code, line, col, message):
        self.code = code
        self.line = line
        self.col = col
        self.message = message

    def __str__(self):
        return f"[{self.code}] Line {self.line}, Col {self.col}: {self.message}"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None
        self.syntax_errors = []
        self.error_count = 1

    def advance(self):
        """Moves to the next token in the stream."""
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None

    def match(self, expected_type, expected_value=None):
        """Checks if the current token matches the expected type/value. If so, advances."""
        if self.current_token is None:
            self.report_error(f"Expected {expected_type} but reached End Of File.")
            return False

        type_matches = self.current_token.type == expected_type
        value_matches = True if expected_value is None else self.current_token.value == expected_value

        if type_matches and value_matches:
            self.advance()
            return True
        else:
            expected_str = expected_value if expected_value else expected_type
            found_str = self.current_token.value
            self.report_error(f"Expected '{expected_str}' but found '{found_str}'")
            self.panic_mode_recovery()
            return False

    def report_error(self, message):
        """Logs a syntax error without stopping the parser."""
        line = self.current_token.line if self.current_token else "EOF"
        col = self.current_token.column if self.current_token else "EOF"
        error_code = f"SYN-{self.error_count:03d}"
        self.syntax_errors.append(SyntaxErrorLog(error_code, line, col, message))
        self.error_count += 1

    def panic_mode_recovery(self):
        """Panic mode: skips tokens until a synchronization point (like ';' or '}') is found."""
        while self.current_token is not None:
            if self.current_token.value in [';', '}']:
                self.advance() # Skip the sync token itself
                break
            self.advance()

    # ==========================================
    # PROGRAM STRUCTURE PARSING
    # ==========================================
    def parse(self):
        """Entry point for the parser."""
        if not self.current_token:
            return None
        return self.parse_class_decl()

    def parse_class_decl(self):
        """ <ClassDeclaration> ::= "public" "class" IDENTIFIER "{" <MainMethod> "}" """
        self.match('KEYWORD', 'public')
        self.match('KEYWORD', 'class')
        
        class_name = "Unknown"
        if self.current_token and self.current_token.type == 'IDENTIFIER':
            class_name = self.current_token.value
            self.advance()
        else:
            self.report_error("Expected class name (Identifier)")
            self.panic_mode_recovery()

        self.match('PUNCTUATION', '{')
        main_method_node = self.parse_main_method()
        self.match('PUNCTUATION', '}')
        
        return ClassDeclNode(class_name, main_method_node)

    def parse_main_method(self):
        """ <MainMethod> ::= "public" "static" "void" "main" "(" "String" "[" "]" IDENTIFIER ")" <Block> """
        self.match('KEYWORD', 'public')
        self.match('KEYWORD', 'static')
        self.match('KEYWORD', 'void')
        
        # Bulletproof check for 'main' (ignores if Phase 1 called it Keyword or Identifier)
        if self.current_token and self.current_token.value == 'main':
            self.advance()
        else:
            self.report_error(f"Expected 'main' but found '{self.current_token.value if self.current_token else 'EOF'}'")
            
        self.match('PUNCTUATION', '(')
        
        # Bulletproof check for 'String'
        if self.current_token and self.current_token.value == 'String':
            self.advance()
        else:
            self.report_error(f"Expected 'String' but found '{self.current_token.value if self.current_token else 'EOF'}'")
            
        self.match('PUNCTUATION', '[')
        self.match('PUNCTUATION', ']')
        
        # Args identifier (like 'args')
        if self.current_token and self.current_token.type == 'IDENTIFIER':
            self.advance() 
        else:
            self.report_error("Expected 'args' identifier")
            
        self.match('PUNCTUATION', ')')
        body = self.parse_block()
        return MainMethodNode(body)

    def parse_block(self):
        """ <Block> ::= "{" <Statement>* "}" """
        statements = []
        if self.match('PUNCTUATION', '{'):
            while self.current_token and not (self.current_token.type == 'PUNCTUATION' and self.current_token.value == '}'):
                stmt = self.parse_statement()
                if stmt:
                    statements.append(stmt)
                else:
                    # If statement parsing fails completely, avoid infinite loops
                    self.advance() 
            self.match('PUNCTUATION', '}')
        return BlockNode(statements)

    # ==========================================
    # STATEMENT PARSING
    # ==========================================
    def parse_statement(self):
        """ Routes to the correct statement parser based on the current token. """
        if not self.current_token:
            return None

        val = self.current_token.value
        if val in ['int', 'float', 'String', 'boolean']:
            return self.parse_var_decl()
        elif val == 'if':
            return self.parse_if_statement()
        elif val == 'while':
            return self.parse_while_statement()
        elif self.current_token.type == 'IDENTIFIER':
            return self.parse_assignment()
        elif val == '{':
            return self.parse_block()
        else:
            self.report_error(f"Unexpected token '{val}' in statement")
            self.panic_mode_recovery()
            return None

    def parse_var_decl(self):
        """ <VariableDecl> ::= <Type> IDENTIFIER "=" <Expression> ";" """
        var_type = self.current_token.value
        self.advance() # Consume type
        
        identifier = "Unknown"
        if self.current_token and self.current_token.type == 'IDENTIFIER':
            identifier = self.current_token.value
            self.advance()
        else:
            self.report_error("Expected identifier in variable declaration")
            
        self.match('OPERATOR', '=')
        expr = self.parse_expression()
        self.match('PUNCTUATION', ';')
        return VarDeclNode(var_type, identifier, expr)

    def parse_assignment(self):
        """ <Assignment> ::= IDENTIFIER "=" <Expression> ";" """
        identifier = self.current_token.value
        self.advance() # Consume identifier
        self.match('OPERATOR', '=')
        expr = self.parse_expression()
        self.match('PUNCTUATION', ';')
        return AssignNode(identifier, expr)

    def parse_if_statement(self):
        """ <IfStatement> ::= "if" "(" <Expression> ")" <Block> ( "else" <Block> )? """
        self.match('KEYWORD', 'if')
        self.match('PUNCTUATION', '(')
        condition = self.parse_expression()
        self.match('PUNCTUATION', ')')
        true_block = self.parse_block()
        
        false_block = None
        if self.current_token and self.current_token.value == 'else':
            self.advance() # Consume else
            false_block = self.parse_block()
            
        return IfNode(condition, true_block, false_block)

    def parse_while_statement(self):
        """ <WhileStatement> ::= "while" "(" <Expression> ")" <Block> """
        self.match('KEYWORD', 'while')
        self.match('PUNCTUATION', '(')
        condition = self.parse_expression()
        self.match('PUNCTUATION', ')')
        body = self.parse_block()
        return WhileNode(condition, body)

    # ==========================================
    # EXPRESSION PARSING (Precedence & AST logic)
    # ==========================================
    def parse_expression(self):
        return self.parse_logical_expr()

    def parse_logical_expr(self):
        left = self.parse_additive_expr()
        while self.current_token and self.current_token.value in ['<', '>', '<=', '>=', '==', '!=']:
            op = self.current_token.value
            self.advance()
            right = self.parse_additive_expr()
            left = BinOpNode(left, op, right)
        return left

    def parse_additive_expr(self):
        left = self.parse_multiplicative_expr()
        while self.current_token and self.current_token.value in ['+', '-']:
            op = self.current_token.value
            self.advance()
            right = self.parse_multiplicative_expr()
            left = BinOpNode(left, op, right)
        return left

    def parse_multiplicative_expr(self):
        left = self.parse_primary_expr()
        while self.current_token and self.current_token.value in ['*', '/']:
            op = self.current_token.value
            self.advance()
            right = self.parse_primary_expr()
            left = BinOpNode(left, op, right)
        return left

    def parse_primary_expr(self):
        if not self.current_token:
            self.report_error("Unexpected end of expression")
            return None

        token = self.current_token
        if token.type == 'NUMBER':
            self.advance()
            return NumberNode(token.value)
        elif token.type == 'STRING_LIT':
            self.advance()
            return StringNode(token.value)
        elif token.type == 'IDENTIFIER':
            self.advance()
            return IdentifierNode(token.value)
        elif token.value == '(':
            self.advance()
            expr = self.parse_expression()
            self.match('PUNCTUATION', ')')
            return expr
        else:
            self.report_error(f"Invalid primary expression: '{token.value}'")
            self.advance()
            return None