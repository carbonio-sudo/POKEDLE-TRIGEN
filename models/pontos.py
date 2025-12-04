import json
import os

CAMINHO_DB_PONTOS = "models/data/pontos.json"

def carregar_pontos():
    if os.path.exists(CAMINHO_DB_PONTOS):
        with open(CAMINHO_DB_PONTOS, "r") as f:
            return json.load(f)
    return {}

def salvar_pontos(pontos):
    with open(CAMINHO_DB_PONTOS, "w") as f:
        json.dump(pontos, f, indent=4)

def get_pontos(usuario):
    pontos = carregar_pontos()
    return pontos.get(usuario, 0)

def set_pontos(usuario, valor):
    pontos = carregar_pontos()
    pontos[usuario] = valor
    salvar_pontos(pontos)
