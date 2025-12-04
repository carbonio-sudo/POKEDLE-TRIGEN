from flask import render_template, request, session, redirect, url_for
from models.user import carregar_usuarios, salvar_usuarios
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

        # Atualizar apelido
        usuario["apelido"] = request.form.get("apelido", "")

        # Garantir que a pasta existe
        os.makedirs("static/img", exist_ok=True)

        # Upload da foto
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
