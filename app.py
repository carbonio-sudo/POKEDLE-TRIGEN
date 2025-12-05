from flask import Flask
from controllers.auth_controller import login, registro, logout, main
from controllers.pokemon_controller import index, reset
from controllers.perfil_controller import perfil, excluir_conta


app = Flask(__name__)
app.secret_key = "segredo-seguro-qualquer"

app.add_url_rule("/excluir", view_func=excluir_conta, methods=["POST"], endpoint="excluir_conta")
app.add_url_rule("/jogo", view_func=index, methods=["GET", "POST"])
app.add_url_rule("/", view_func=main)
app.add_url_rule("/login", view_func=login, methods=["GET", "POST"])
app.add_url_rule("/registro", view_func=registro, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=logout)
app.add_url_rule("/reset", view_func=reset, methods=["POST"])
app.add_url_rule("/perfil", view_func=perfil, methods=["GET", "POST"])

if __name__ == "__main__":
    app.run(debug=True)
