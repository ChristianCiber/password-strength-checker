from flask import Flask, render_template, request, jsonify
from analyzer import analizar_password


app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON inválido"}), 400

    password = data.get("password", "")

    if not password:
        return jsonify({"error": "La contraseña no puede estar vacía"}), 400

    if len(password) > 128:
        return jsonify({"error": "Contraseña demasiado larga"}), 400

    resultado = analizar_password(password)

    return jsonify(resultado)


if __name__ == "__main__":
    app.run(debug=False)