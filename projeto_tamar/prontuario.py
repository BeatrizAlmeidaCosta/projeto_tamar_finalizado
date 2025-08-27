from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Configuração do banco SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prontuario_tamar.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


# ------------------- MODELO -------------------
class Prontuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120))
    especie = db.Column(db.String(120))
    sexo = db.Column(db.String(50))
    data_entrada = db.Column(db.String(20))
    origem = db.Column(db.String(120))
    nascimento = db.Column(db.String(20))
    microchip = db.Column(db.String(120))
    anilhas = db.Column(db.String(120))
    observacoes = db.Column(db.Text)

    dt_entrada = db.Column(db.String(20))
    hr_entrada = db.Column(db.String(20))
    tt_tamar = db.Column(db.String(120))
    recinto = db.Column(db.String(120))
    procedencia = db.Column(db.String(120))
    forma = db.Column(db.String(120))
    esp_entrada = db.Column(db.String(120))
    ccc = db.Column(db.Float)
    lcc = db.Column(db.Float)
    ct = db.Column(db.Float)
    peso = db.Column(db.Float)
    marcas_encontradas = db.Column(db.String(120))
    marcas_colocadas = db.Column(db.String(120))
    historico = db.Column(db.Text)
    anamnese = db.Column(db.Text)

    ref_pupilar = db.Column(db.String(50))
    ref_palpebral = db.Column(db.String(50))
    ref_corneal = db.Column(db.String(50))
    ref_doloroso = db.Column(db.String(50))
    hidratacao = db.Column(db.String(50))
    mucosas = db.Column(db.String(50))
    hematocrito = db.Column(db.String(50))
    ppt = db.Column(db.String(50))
    glicemia = db.Column(db.String(50))
    fc = db.Column(db.String(50))
    fr = db.Column(db.String(50))
    suspeita = db.Column(db.Text)
    proced_medicos = db.Column(db.Text)

    dt_saida = db.Column(db.String(20))
    hr_saida = db.Column(db.String(20))
    forma_saida = db.Column(db.String(120))
    tt_saida = db.Column(db.String(120))
    ccc_saida = db.Column(db.Float)
    lcc_saida = db.Column(db.Float)
    ct_saida = db.Column(db.Float)
    peso_saida = db.Column(db.Float)
    marc_encon_saida = db.Column(db.String(120))
    marc_coloc_saida = db.Column(db.String(120))
    praia = db.Column(db.String(120))

    pdf = db.Column(db.Text)
    procedimentos = db.Column(db.Text)
    parametros_agua = db.Column(db.Text)

    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# ------------------- ROTAS HTML -------------------
@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(".", filename)


# ------------------- ROTAS API -------------------
@app.route("/api/prontuarios", methods=["POST"])
def salvar():
    dados = request.json

    # Converte strings vazias em None (evita erro em floats)
    for k, v in list(dados.items()):
        if isinstance(v, str) and v.strip() == "":
            dados[k] = None

    # Corrige nome do campo de parâmetros da água
    if "parametrosAgua" in dados:
        dados["parametros_agua"] = dados.pop("parametrosAgua")

    novo = Prontuario(**dados)
    db.session.add(novo)
    db.session.commit()
    return jsonify({"msg": "Salvo com sucesso!"}), 201


@app.route("/api/prontuarios", methods=["GET"])
def listar():
    todos = Prontuario.query.all()
    result = []
    for p in todos:
        item = {c.name: getattr(p, c.name) for c in p.__table__.columns}
        # Conversão para JSON
        if "parametros_agua" in item:
            item["parametrosAgua"] = item.pop("parametros_agua")
        result.append(item)
    return jsonify(result)


@app.route("/api/prontuarios/<int:id>", methods=["DELETE"])
def deletar(id):
    p = Prontuario.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"msg": "Prontuário deletado com sucesso!"})


# ------------------- MAIN -------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="127.0.0.1", port=5000, debug=True)
