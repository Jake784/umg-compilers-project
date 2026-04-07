# Java Compiler Frontend: Lexical & Syntax Analyzer

This repository contains Phase 1 and Phase 2 of a compiler design project — a complete frontend (Scanner and Parser) for a subset of Java, bridging Formal Languages, Automata Theory, and Context-Free Grammars with functional software architecture.

## Objectives

### Phase 1: Lexical Analysis (Scanner)

- **Scanner implementation:** Recognizes the regular grammar of the language using regular expressions.
- **Token management:** Classifies input streams into categories (keywords, identifiers, operators, literals, and punctuation).
- **Lexical error handling:** Detects invalid characters and accurately reports their exact line and column.

### Phase 2: Syntax Analysis (Parser)

- **Recursive descent parser:** Validates the token stream against a custom Context-Free Grammar (BNF).
- **AST generation:** Constructs an object-oriented Abstract Syntax Tree reflecting the hierarchical structure of the code (loops, conditionals, math precedence).
- **Interactive visualization:** Renders the AST as an interactive, zoomable SVG graph using Graphviz.
- **Panic mode error recovery:** Gracefully handles syntax errors, isolating the issue and continuing analysis without crashing the compiler.

## Project Structure

The codebase follows a modular architecture, separating core business logic from the presentation layer.

```text
project-test/
├── core/                   # Core logic and models
│   ├── __init__.py
│   ├── scanner.py          # Lexical analysis engine (Regex & Tokenization)
│   ├── parser.py           # Syntax analysis engine (Recursive Descent)
│   └── token_model.py      # Token data structure
├── grammar.bnf             # Formal Backus-Naur Form grammar rules
├── assets/                 # External stylesheets
│   └── style.css           # UI layout configurations (Dark Theme & SVG viewer)
├── samples/                # Test files
│   └── code.txt            # Sample Java source code
├── app.py                  # Main entry point (Streamlit Web Dashboard)
├── main.py                 # Alternative entry point (CLI version)
└── report-generation/      # Auto-generated .txt reports (ignored in version control)
```

## Prerequisites: Graphviz Installation

Because this project generates visual AST diagrams, Graphviz must be installed on your operating system, not just in Python.

### Windows

1. Download the installer from the official Graphviz website.
2. Run the installer. During installation, select: _"Add Graphviz to the system PATH for all users"_ (or current user).
3. Alternatively, on Windows 10/11 open PowerShell and run:

```bash
winget install graphviz
```

### macOS

Open your terminal and use Homebrew:

```bash
brew install graphviz
```

### Linux (Debian/Ubuntu)

Open your terminal and run:

```bash
sudo apt-get install graphviz
```

## How to Run (Web Interface)

This project features a modern web GUI built with Streamlit.

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd project-test
```

### 2. Activate the virtual environment

- Mac/Linux: `source .venv/bin/activate`
- Windows: `.venv\Scripts\activate`

### 3. Install Python dependencies

```bash
pip install streamlit pandas graphviz
```

### 4. Launch the application

```bash
python -m streamlit run app.py
```

## Built With

- **Python 3** — core engine
- **Streamlit & Pandas** — web dashboard and data visualization
- **Graphviz & SVG-Pan-Zoom** — AST rendering and interactive navigation
- **RegEx** — deterministic finite automaton (DFA) simulation