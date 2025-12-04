from flask import render_template, request, session, redirect, url_for, flash
from models.user import carregar_usuarios, salvar_usuarios

def registro():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        usuarios = carregar_usuarios()

        for u in usuarios:
            if u["usuario"] == usuario:
                flash("❌ Nome de usuário já existe!")
                return redirect(url_for("registro"))

        usuarios.append({
            "usuario": usuario,
            "senha": senha,
            "apelido": None,
            "foto": "default.png",
            "pontos": 0
        })

        salvar_usuarios(usuarios)

        flash("✅ Usuário registrado com sucesso!")
        return redirect(url_for("login"))

    return render_template("registro.html")


def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        usuarios = carregar_usuarios()

        for u in usuarios:
            if u["usuario"] == usuario and u["senha"] == senha:
                session["logado"] = True
                session["usuario"] = usuario
                session["apelido"] = u.get("apelido")
                session["foto"] = u.get("foto", "default.png")
                return redirect(url_for("index"))

        flash("❌ Usuário ou senha incorretos.")
        return redirect(url_for("login"))

    return render_template("login.html")


def logout():
    session.clear()
    return redirect(url_for("login"))
