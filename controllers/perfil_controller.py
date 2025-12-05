from flask import render_template, request, session, redirect, url_for
from models.user import carregar_usuarios, salvar_usuarios
from models.pontos import carregar_todos_pontos, salvar_todos_pontos
import os

def perfil():
    if "usuario" not in session:
        return redirect(url_for("login"))

    usuarios = carregar_usuarios()
    usuario_logado = session["usuario"]

    for user in usuarios:
        if user["usuario"] == usuario_logado:
            usuario = user
            break
    else:
        return "Usuário não encontrado", 404

    if request.method == "POST":
        usuario["apelido"] = request.form.get("apelido", "")

        os.makedirs("static/img", exist_ok=True)

        foto = request.files.get("foto")
        if foto and foto.filename != "":
            caminho_foto = f"static/img/{usuario_logado}.jpg"
            foto.save(caminho_foto)
            usuario["foto"] = caminho_foto

        salvar_usuarios(usuarios)
        return redirect(url_for("perfil"))

    return render_template(
        "editar.html",
        usuario=usuario,
        foto=usuario.get("foto", "static/img/default.png")
    )


def excluir_conta():
    if "usuario" not in session:
        return redirect(url_for("login"))

    usuario_logado = session["usuario"]

    usuarios = carregar_usuarios()
    usuarios = [u for u in usuarios if u["usuario"] != usuario_logado]
    salvar_usuarios(usuarios)

    pontos = carregar_todos_pontos()
    if usuario_logado in pontos:
        del pontos[usuario_logado]
    salvar_todos_pontos(pontos)

    caminho = f"static/img/{usuario_logado}.jpg"
    if os.path.exists(caminho):
        os.remove(caminho)

    session.clear()
    return redirect(url_for("login"))
