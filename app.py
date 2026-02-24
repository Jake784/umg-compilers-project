import streamlit as st
import pandas as pd
from scanner import Scanner

# Configuración de la página web
st.set_page_config(page_title="Lexical Analyzer", layout="wide")

st.title("Lexical Analyzer - Java Scanner")
st.markdown("Phase 1: Lexical Analysis using Regular Expressions.")

# Área de texto para que el usuario escriba o pegue el código
source_code = st.text_area("Enter the source code (Java) here:", height=250)

# Botón principal para ejecutar el análisis
if st.button("Analyze Code", type="primary"):
    if source_code.strip():
        # 1. Instanciamos el Scanner que ya construiste previamente
        scanner = Scanner(source_code)
        
        # 2. Ejecutamos el motor de análisis
        scanner.analyze()

        st.divider() # Línea visual separadora

        # 3. Creamos tres pestañas interactivas para organizar los resultados
        tab1, tab2, tab3 = st.tabs(["Found Tokens", "Symbol Table", "Lexical Errors"])

        # --- Pestaña 1: Tokens ---
        with tab1:
            # Convertimos tu lista de objetos Token en un formato que la tabla visual pueda leer
            tokens_data = [{"Type": t.type, "Value": t.value, "Line": t.line, "Column": t.column} for t in scanner.tokens]
            if tokens_data:
                # Mostramos los datos en una tabla interactiva
                st.dataframe(pd.DataFrame(tokens_data), use_container_width=True)
            else:
                st.info("No valid tokens found.")

        # --- Pestaña 2: Tabla de Símbolos ---
        with tab2:
            # Extraemos los identificadores de tu diccionario
            symbols_data = [{"Identifier": k, "First Appearance (Line)": v['first_appearance_line']} for k, v in scanner.symbol_table.items()]
            if symbols_data:
                st.dataframe(pd.DataFrame(symbols_data), use_container_width=True)
            else:
                st.info("The symbol table is empty.")

        # --- Pestaña 3: Errores Léxicos ---
        with tab3:
            if scanner.lexical_errors:
                # Mostramos cada error detectado en una caja roja de alerta
                for error in scanner.lexical_errors:
                    st.error(error)
            else:
                st.success("Excellent! No lexical errors were detected in the source code.")
    else:
        st.warning("Please enter source code before analyzing.")