import streamlit as st
import pandas as pd
import time
from scanner import Scanner

st.set_page_config(page_title="Advanced Lexical Analyzer", layout="wide")

def load_css(file_name):
    """Abre un archivo CSS y lo inyecta en la aplicación."""
    try:
        with open(file_name, 'r') as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"No se encontró el archivo {file_name}")

load_css("style.css")

with st.sidebar:
    st.header("Settings & Upload")
    st.markdown("You can type the code directly, or upload a file.")
    
    uploaded_file = st.file_uploader("Upload source code", type=["txt", "java"])
    
    st.divider()
    st.info("**Pro Tip:** This scanner detects Keywords, Identifiers, Numbers, Operators, and basic Punctuation in Java.")

st.title("Lexical Analyzer")
st.markdown("### Java Subset Scanner")

default_code = ""
if uploaded_file is not None:
    default_code = uploaded_file.getvalue().decode("utf-8")

source_code = st.text_area("Source Code Entry:", value=default_code, height=300)

if st.button("Run Lexical Analysis", type="primary", use_container_width=True):
    
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
        tab1, tab2, tab3 = st.tabs(["Token Stream", "Symbol Table", "Error Report"])

        with tab1:
            tokens_data = [{"Type": t.type, "Value": t.value, "Line": t.line, "Column": t.column} for t in scanner.tokens]
            if tokens_data:
                st.dataframe(pd.DataFrame(tokens_data), use_container_width=True, height=400)
            else:
                st.info("No valid tokens found.")

        with tab2:
            symbols_data = [{"Identifier": k, "First Appearance (Line)": v['first_appearance_line']} for k, v in scanner.symbol_table.items()]
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