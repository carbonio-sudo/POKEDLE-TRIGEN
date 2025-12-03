import json
import os

CAMINHO_DB = "models/data/usuarios.json"

def carregar_usuarios():
    if os.path.exists(CAMINHO_DB):
        with open(CAMINHO_DB, "r") as f:
            return json.load(f)
    return []

def salvar_usuarios(lista):
    with open(CAMINHO_DB, "w") as f:
        json.dump(lista, f, indent=4)
