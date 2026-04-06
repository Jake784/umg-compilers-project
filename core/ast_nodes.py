class ASTNode:
    """Base class for all Abstract Syntax Tree nodes."""
    pass

# ==========================================
# PROGRAM STRUCTURE NODES
# ==========================================

class ProgramNode(ASTNode):
    def __init__(self, class_decl):
        self.class_decl = class_decl

class ClassDeclNode(ASTNode):
    def __init__(self, name, main_method):
        self.name = name
        self.main_method = main_method

class MainMethodNode(ASTNode):
    def __init__(self, body):
        self.body = body

class BlockNode(ASTNode):
    def __init__(self, statements):
        self.statements = statements  # List of statement nodes

# ==========================================
# STATEMENT NODES
# ==========================================

class VarDeclNode(ASTNode):
    def __init__(self, var_type, identifier, expression):
        self.var_type = var_type
        self.identifier = identifier
        self.expression = expression

class AssignNode(ASTNode):
    def __init__(self, identifier, expression):
        self.identifier = identifier
        self.expression = expression

class IfNode(ASTNode):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

class WhileNode(ASTNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

# ==========================================
# EXPRESSION NODES (MATH & LOGIC)
# ==========================================

class BinOpNode(ASTNode):
    """Handles binary operations like +, -, *, /, <, >, ==, etc."""
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class NumberNode(ASTNode):
    def __init__(self, value):
        self.value = value

class StringNode(ASTNode):
    def __init__(self, value):
        self.value = value

class IdentifierNode(ASTNode):
    def __init__(self, name):
        self.name = name