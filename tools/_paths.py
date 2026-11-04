"""Caminhos da fábrica, iguais para qualquer agente (Hermes, Claude Code, ...)."""
import os

TOOLS = os.path.dirname(os.path.abspath(__file__))
FABRICA = os.environ.get("FABRICA_HOME", os.path.dirname(TOOLS))
PESQUISA = os.path.join(FABRICA, "pesquisa")
TENDENCIAS = os.path.join(PESQUISA, "tendencias")
SEGREDOS_YT = os.environ.get("SEGREDOS_YT", os.path.expanduser("~/.segredos/youtube"))
TOKENS = os.path.join(SEGREDOS_YT, "tokens")
CLIENT = os.path.join(SEGREDOS_YT, "client.json")
VENV_BIN = os.path.join(TOOLS, ".venv", "bin")
