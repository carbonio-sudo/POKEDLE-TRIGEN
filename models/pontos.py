import json
import os

CAMINHO_DB = "models/data/pontos.json"

def get_pontos(usuario):
    if os.path.exists(CAMINHO_DB):
        with open(CAMINHO_DB, "r") as f:
            dados = json.load(f)
            return dados.get(usuario, 0)
    return 0

def set_pontos(usuario, pontos):
    dados = {}
    if os.path.exists(CAMINHO_DB):
        with open(CAMINHO_DB, "r") as f:
            dados = json.load(f)
    dados[usuario] = pontos
    with open(CAMINHO_DB, "w") as f:
        json.dump(dados, f, indent=4)

def add_pontos(usuario, pontos):
    atuais = get_pontos(usuario)
    set_pontos(usuario, atuais + pontos)

def get_all_pontos():
    if os.path.exists(CAMINHO_DB):
        with open(CAMINHO_DB, "r") as f:
            dados = json.load(f)
            return sorted(dados.items(), key=lambda x: x[1], reverse=True)
    return []
