from flask import render_template, request, session, redirect, url_for
import requests
import random
from models.user import carregar_usuarios
from models.pontos import get_pontos, set_pontos

LISTA_POKEMONS = []
pokemon_alvo = None

def carregar_nomes():
    global LISTA_POKEMONS
    url = "https://pokeapi.co/api/v2/pokemon?limit=386"
    r = requests.get(url)
    if r.status_code == 200:
        LISTA_POKEMONS = [p["name"] for p in r.json()["results"]]

carregar_nomes()

# ==========================
#      EVOLUÇÃO / FASE
# ==========================

def encontrar_fase(cadeia, alvo, fase=1):
    if cadeia["species"]["name"] == alvo:
        return fase
    
    for evolucao in cadeia["evolves_to"]:
        resultado = encontrar_fase(evolucao, alvo, fase + 1)
        if resultado:
            return resultado
    
    return None

def calcular_fase(especie):
    url_chain = especie["evolution_chain"]["url"]
    cadeia = requests.get(url_chain).json()["chain"]
    nome_especie = especie["name"]
    fase = encontrar_fase(cadeia, nome_especie)
    return fase or 1


# ==========================
#      DADOS POKÉMON
# ==========================

def obter_dados(nome):
    nome = str(nome).lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{nome}"
    r = requests.get(url)

    if r.status_code != 200:
        return None

    d = r.json()
    especie = requests.get(d["species"]["url"]).json()

    tipos = [t["type"]["name"] for t in d["types"]]
    tipo1 = tipos[0]
    tipo2 = tipos[1] if len(tipos) > 1 else "nenhum"

    return {
        "nome": d["name"],
        "sprite": d["sprites"]["front_default"],
        "tipos": tipos,
        "tipo1": tipo1,
        "tipo2": tipo2,
        "altura": d["height"],
        "peso": d["weight"],
        "habitat": especie["habitat"]["name"] if especie["habitat"] else "desconhecido",
        "cor": especie["color"]["name"],
        "fase": calcular_fase(especie)
    }


# ==========================
#      SORTEAR POKÉMON
# ==========================

def sortear():
    global pokemon_alvo
    poke = None
    while poke is None:
        poke = obter_dados(random.randint(1, 386))
    pokemon_alvo = poke
    return True

sortear()


# ==========================
#          RESET
# ==========================

def reset():
    session["tentativas"] = []
    session["mensagem"] = "🔄 Tentativas resetadas!"
    session["venceu"] = False
    sortear()
    return redirect(url_for("index"))


# ==========================
#     PÁGINA PRINCIPAL
# ==========================

def index():
    global pokemon_alvo

    if not session.get("logado"):
        return redirect(url_for("login"))

    # carrega tentativas
    session.setdefault("tentativas", [])
    session.setdefault("venceu", False)

    # carrega pontos do arquivo pontos.json
    session.setdefault("pontos", get_pontos(session["usuario"]))

    # caso já tenha vencido
    if session["venceu"]:
        tent = session["tentativas"][::-1]
        set_pontos(session["usuario"], session["pontos"])
        return render_template(
            "index.html",
            message="🎉 Você já venceu!",
            attempts=tent,
            alvo=pokemon_alvo["nome"],
            pontos=session["pontos"],
            pokemon_list=[]
        )

    # tentativa enviada
    if request.method == "POST":
        chute = request.form.get("guess", "").lower()

        if not chute:
            session["mensagem"] = "Digite um Pokémon!"
            return redirect(url_for("index"))

        dados = obter_dados(chute)
        if dados is None:
            session["mensagem"] = "Pokémon inválido!"
            return redirect(url_for("index"))

        # já tentado
        for t in session["tentativas"]:
            if t["nome"] == dados["nome"]:
                session["mensagem"] = "❌ Você já tentou esse!"
                return redirect(url_for("index"))

        # registra tentativa
        tentativa = montar_feedback(dados)
        session["tentativas"].append(tentativa)

        # perde pontos
        if session["pontos"] > 0:
            session["pontos"] -= 5

        # acertou
        if dados["nome"] == pokemon_alvo["nome"]:
            session["venceu"] = True
            session["pontos"] += 50
            session["mensagem"] = "🎉 Você acertou!"
            set_pontos(session["usuario"], session["pontos"])

        session.modified = True
        return redirect(url_for("index"))

    # exibe tela normal
    mensagem = session.pop("mensagem", "")
    tent = session["tentativas"][::-1]
    nomes_usados = {t["nome"] for t in session["tentativas"]}
    lista = [n for n in LISTA_POKEMONS if n not in nomes_usados]

    return render_template(
        "index.html",
        message=mensagem,
        attempts=tent,
        pokemon_list=lista,
        alvo=pokemon_alvo["nome"],
        pontos=session["pontos"]
    )


# ==========================
#      FEEDBACK
# ==========================

def montar_feedback(p):
    alvo = pokemon_alvo
    return {
        "nome": p["nome"],
        "sprite": p["sprite"],
        "tipo1": p["tipo1"],
        "tipo2": p["tipo2"],
        "habitat": p["habitat"],
        "cor": p["cor"],
        "fase": p["fase"],
        "altura": p["altura"],
        "peso": p["peso"],

        "tipo1_cor": "correto" if p["tipo1"] in alvo["tipos"] else "errado",
        "tipo2_cor": "correto" if p["tipo2"] == alvo["tipo2"] else "errado",
        "habitat_cor": "correto" if p["habitat"] == alvo["habitat"] else "errado",
        "cor_cor": "correto" if p["cor"] == alvo["cor"] else "errado",
        "fase_cor": "correto" if p["fase"] == alvo["fase"] else "errado",

        "altura_cor": (
            "correto" if p["altura"] == alvo["altura"] else
            "maior" if p["altura"] < alvo["altura"] else
            "menor"
        ),

        "peso_cor": (
            "correto" if p["peso"] == alvo["peso"] else
            "maior" if p["peso"] < alvo["peso"] else
            "menor"
        )
    }
