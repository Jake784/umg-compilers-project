# Java Lexical Analyzer (Scanner)

This repository contains Phase 1 of a compiler design project, focusing on the construction of a Lexical Analyzer (Scanner) for a subset of the Java programming language. It is designed to bridge core concepts of Formal Languages and Automata Theory with functional software architecture.

## Objectives
* **Scanner Implementation:** Recognizes the regular grammar of the language using Regular Expressions.
* **Token Management:** Classifies input streams into categories (Keywords, Identifiers, Operators, Literals, and Punctuation).
* **Lexical Error Handling:** Detects invalid characters and accurately reports their exact line and column.
* **Symbol Table:** Initializes the data structure to store information about found identifiers.

## Project Structure
The codebase follows a modular architecture, separating the core business logic from the presentation layer:

```text
project-test/
├── core/                   # Core logic and models
│   ├── __init__.py
│   ├── scanner.py          # Lexical analysis engine (Regex & Tokenization)
│   └── token_model.py      # Token data structure
├── assets/                 # External stylesheets
│   └── style.css           # UI layout configurations
├── samples/                # Test files
│   └── code.txt            # Sample Java source code
├── app.py                  # Main entry point (Streamlit Web Dashboard)
├── main.py                 # Alternative entry point (CLI version)
└── report-generation/      # Auto-generated .txt reports (Ignored in version control)

How to Run (Web Interface)
This project features a modern Web GUI built with Streamlit.

1. Activate the virtual environment:

Bash
source .venv/bin/activate
2. Install dependencies:

Bash
pip install streamlit pandas
3. Launch the application:

Bash
python3 -m streamlit run app.py
Built With
Python 3 - Core engine

Streamlit & Pandas - Web Dashboard and Data Visualization

RegEx - Deterministic Finite Automaton (DFA) simulation