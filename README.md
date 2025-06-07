# Projeto ADK GOOGLE
# Instale o python:
https://www.python.org/downloads/

# Instale o VS Code
https://code.visualstudio.com/download

# Instale o UV
pip install uv

# COM UV INICIE O PROJETO
"uv init" ou "uv sync" caso já exista o arquivo "pyproject.toml"

# CRIE UM AMBIENTE VIRTUAL
uv venv

# Ative o .venv
.venv\Scripts\activate

# Instale o google ADK 
uv add google-adk google-generativeai python-dotenv

# CRIE O AGENTE E EXECUTE
adk web
