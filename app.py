import streamlit as st
import pandas as pd
import time
import graphviz # New import for Graphviz visualization
from core.scanner import Scanner
from core.parser import Parser  # New import for the Parser class
from streamlit_ace import st_ace

st.set_page_config(page_title="Compiler: Lexical & Syntax Analyzer", layout="wide")

def load_css(file_name):
    """Opens a CSS file and injects it into the application."""
    try:
        with open(file_name, 'r') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"File {file_name} was not found.")

load_css("assets/style.css")

# ==========================================
# GRAPHVIZ AST GENERATOR
# ==========================================
def generate_ast_graph(node, graph=None, node_id="root"):
    """Recursively parses the AST and builds a visual Graphviz tree."""
    if graph is None:
        graph = graphviz.Digraph()
        # Estilo visual de los nodos (puedes cambiar los colores)
        graph.attr('node', shape='box', style='rounded,filled', fillcolor='#1E293B', fontcolor='white', color='#38BDF8')
        graph.attr('edge', color='#94A3B8')

    if node is None:
        return graph

    # If the node is a list of statements, create a subgraph for it
    # Si es una lista de instrucciones (ej. dentro de un Block)
    if isinstance(node, list):
        # CORRECCIÓN: Usamos exactamente el node_id que el padre está buscando
        graph.node(node_id, label="Statements", shape='folder', fillcolor='#475569')
        for i, stmt in enumerate(node):
            child_id = f"{node_id}_stmt_{i}"
            generate_ast_graph(stmt, graph, child_id)
            graph.edge(node_id, child_id)
        return graph

    # If the node is a primitive value (plain text)
    if not hasattr(node, '__dict__'):
        graph.node(node_id, label=str(node), shape='ellipse', fillcolor='#10B981')
        return graph

    # Process AST Nodes
    node_label = node.__class__.__name__.replace('Node', '')
    
    # special handling for certain node types to include operator or value in the label
    if node_label == 'BinOp':
        node_label = f"BinOp\n({node.operator})"
    elif node_label in ['Number', 'String', 'Identifier', 'VarDecl']:
        val = getattr(node, 'value', getattr(node, 'name', getattr(node, 'identifier', '')))
        node_label = f"{node_label}\n'{val}'"

    graph.node(node_id, label=node_label)

    # Connect child nodes
    for i, (key, value) in enumerate(vars(node).items()):
        if key == 'operator' and node.__class__.__name__ == 'BinOpNode':
            continue # already included in label
        if value is None or (isinstance(value, list) and len(value) == 0):
            continue # skip empty fields
            
        child_id = f"{node_id}_{key}_{i}"
        generate_ast_graph(value, graph, child_id)
        graph.edge(node_id, child_id, label=key, fontsize='10', fontcolor='#94A3B8')

    return graph

# ==========================================
# STATE MANAGEMENT
# ==========================================
if "code_input" not in st.session_state:
    st.session_state.code_input = ""
if "last_uploaded_file" not in st.session_state:
    st.session_state.last_uploaded_file = None
if "editor_key" not in st.session_state:
    st.session_state.editor_key = 0
if "uploader_key" not in st.session_state:   
    st.session_state.uploader_key = 0        

# ==========================================
# SIDE BAR AND UPLOADER
# ==========================================
with st.sidebar:
    st.header("Settings & Upload")
    st.markdown("You can type the code directly, or upload a file.")
    
    uploaded_file = st.file_uploader(
        "Upload source code", 
        type=["txt", "java"], 
        key=f"uploader_{st.session_state.uploader_key}"
    )
    
    st.divider()
    st.info("**Phase 1:** Lexical Analysis (Tokens & Symbols)\n\n**Phase 2:** Syntax Analysis (AST & Grammar)")

# ==========================================
# FILE LOGIC AND CLEANUP
# ==========================================
if uploaded_file is None:
    st.session_state.last_uploaded_file = None

if uploaded_file is not None:
    if st.session_state.last_uploaded_file != uploaded_file.name:
        st.session_state.code_input = uploaded_file.getvalue().decode("utf-8")
        st.session_state.last_uploaded_file = uploaded_file.name
        st.session_state.editor_key += 1

def clear_text():
    st.session_state.code_input = ""
    st.session_state.last_uploaded_file = None
    st.session_state.editor_key += 1
    st.session_state.uploader_key += 1  

# ==========================================
# MAIN INTERFACE
# ==========================================
st.title("Compiler Frontend")
st.markdown("### Scanner & Parser (Java Subset)")
st.markdown("**Source Code Entry:**")

source_code = st_ace(
    value=st.session_state.code_input,
    language="java",
    theme="tomorrow_night",
    key=f"ace_editor_{st.session_state.editor_key}",  
    font_size=13,
    tab_size=4,
    height=400,
    show_gutter=True,
    auto_update=False
)

if source_code != st.session_state.code_input and source_code is not None:
    st.session_state.code_input = source_code

col_btn1, col_btn2 = st.columns([3, 2])

with col_btn1:
    run_pressed = st.button("Run Lexical & Syntax Analysis", type="primary", use_container_width=True)
with col_btn2:
    st.button("Clear Code", on_click=clear_text, use_container_width=True)

# ==========================================
# ANALYSIS AND RESULTS
# ==========================================
if run_pressed:
    if source_code.strip():
        with st.spinner('Compiling code (Scanning & Parsing)...'):
            time.sleep(0.5)
            
            # Phase 1: Scanner
            scanner = Scanner(source_code)
            scanner.analyze()
            
            # Phase 2: Parser
            parser = Parser(scanner.tokens)
            ast = parser.parse()
            
        st.markdown("### Compilation Overview")
        
        # Update metrics to include Syntax Errors
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(label="Total Tokens", value=len(scanner.tokens))
        with col2:
            st.metric(label="Unique Symbols", value=len(scanner.symbol_table))
        with col3:
            lex_err = len(scanner.lexical_errors)
            st.metric(label="Lexical Errors", value=lex_err, delta="Fix needed" if lex_err > 0 else "Clean", delta_color="inverse")
        with col4:
            syn_err = len(parser.syntax_errors)
            st.metric(label="Syntax Errors", value=syn_err, delta="Fix needed" if syn_err > 0 else "Clean", delta_color="inverse")

        st.divider()

        # Added AST and Syntax Error Tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "AST (Hierarchy)", 
            "Syntax Errors", 
            "Token Stream", 
            "Symbol Table", 
            "Lexical Errors"
        ])

        with tab1:
            st.markdown("#### Abstract Syntax Tree (Visual Graph)")
            if ast:
                ast_graph = generate_ast_graph(ast)
                st.graphviz_chart(ast_graph, use_container_width=True)
            else:
                st.info("AST could not be generated due to fatal structural errors.")

        with tab2:
            st.markdown("#### Syntax Error Console")
            if parser.syntax_errors:
                for error in parser.syntax_errors:
                    st.error(str(error))
            else:
                st.success("Syntax analysis passed! The code structure matches the grammar.")

        with tab3:
            tokens_data = [{"Lexeme": t.value, "Token Category": t.type, "Line": t.line, "Col": t.column} for t in scanner.tokens]
            if tokens_data:
                st.dataframe(pd.DataFrame(tokens_data), use_container_width=True, height=400)
            else:
                st.info("No valid tokens found.")

        with tab4:
            symbols_data = [{"Identifier": k, "Type": v['type'], "Line": v['line'], "Col": v['column']} for k, v in scanner.symbol_table.items()]
            if symbols_data:
                st.dataframe(pd.DataFrame(symbols_data), use_container_width=True)
            else:
                st.info("The symbol table is empty.")

        with tab5:
            if scanner.lexical_errors:
                for error in scanner.lexical_errors:
                    st.warning(error)
            else:
                st.success("No lexical errors found.")
                
        # Export feature remains for phase 1 compliance
        st.divider()
        report_content = f"{'LEXEME':<20} | {'TOKEN'}\n" + "-" * 40 + "\n"
        for t in scanner.tokens:
            report_content += f"{t.value:<20} | {t.type}\n"
            
        st.download_button(
            label="Download Token Report (.txt)",
            data=report_content,
            file_name="token_report.txt",
            mime="text/plain",
            type="primary"
        )
                
    else:
        st.warning("Please enter some code or upload a file before analyzing.")