import streamlit as st
import pandas as pd
import time
from core.scanner import Scanner
from streamlit_ace import st_ace

st.set_page_config(page_title="Advanced Lexical Analyzer", layout="wide")

def load_css(file_name):
    """Opens a CSS file and injects it into the application."""
    try:
        with open(file_name, 'r') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"File {file_name} was not found.")

load_css("assets/style.css")

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
    st.info("**Pro Tip:** This scanner detects Keywords, Identifiers, Numbers, Operators, and basic Punctuation in Java.")

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
st.title("Lexical Analyzer")
st.markdown("### Java Subset Scanner")
st.markdown("**Source Code Entry:**")

source_code = st_ace(
    value=st.session_state.code_input,
    language="java",
    theme="tomorrow_night",
    key=f"ace_editor_{st.session_state.editor_key}",  
    font_size=13,
    tab_size=4,
    height=340,
    show_gutter=True,
    auto_update=False
)

if source_code != st.session_state.code_input and source_code is not None:
    st.session_state.code_input = source_code

col_btn1, col_btn2 = st.columns([3, 2])

with col_btn1:
    run_pressed = st.button("Run Lexical Analysis", type="primary", use_container_width=True)
with col_btn2:
    st.button("Clear Code", on_click=clear_text, use_container_width=True)

# ==========================================
# ANALYSIS AND RESULTS
# ==========================================
if run_pressed:
    if source_code.strip():
        with st.spinner('Analyzing syntax and generating tokens...'):
            time.sleep(0.5)
            
            scanner = Scanner(source_code)
            scanner.analyze()
            
        st.markdown("### Analysis Overview")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label="Total Tokens", value=len(scanner.tokens))
        with col2:
            st.metric(label="Unique Symbols", value=len(scanner.symbol_table))
        with col3:
            error_count = len(scanner.lexical_errors)
            st.metric(label="Lexical Errors", value=error_count, delta="-Needs Fix" if error_count > 0 else "Perfect", delta_color="inverse")

        st.divider()

        report_content = f"{'LEXEME (VALUE)':<20} | {'TOKEN (CATEGORY)'}\n"
        report_content += "-" * 45 + "\n"
        for t in scanner.tokens:
            report_content += f"{t.value:<20} | {t.type}\n"

        col_export1, col_export2 = st.columns([1, 2])
        with col_export1:
            st.download_button(
                label="Export Token Report (.txt)",
                data=report_content,
                file_name="token_report.txt",
                mime="text/plain",
                type="primary"
            )

        st.divider()

        tab1, tab2, tab3 = st.tabs(["Token Stream", "Symbol Table", "Error Report"])

        with tab1:
            tokens_data = [{"Lexeme (Value)": t.value, "Token (Category)": t.type, "Line": t.line, "Column": t.column} for t in scanner.tokens]
            if tokens_data:
                st.dataframe(pd.DataFrame(tokens_data), use_container_width=True, height=400)
            else:
                st.info("No valid tokens found.")

        with tab2:
            symbols_data = [{"Identifier Name": k, "Type": v['type'], "Line": v['line'], "Column": v['column']} for k, v in scanner.symbol_table.items()]
            if symbols_data:
                st.dataframe(pd.DataFrame(symbols_data), use_container_width=True)
            else:
                st.info("The symbol table is empty.")

        with tab3:
            if scanner.lexical_errors:
                for error in scanner.lexical_errors:
                    st.error(error)
            else:
                st.success("Analysis passed successfully. No lexical errors found.")
                st.balloons()
                
    else:
        st.warning("Please enter some code or upload a file before analyzing.")