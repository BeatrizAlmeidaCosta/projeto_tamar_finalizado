from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Caminho absoluto para o diretório do arquivo
basedir = os.path.abspath(os.path.dirname(__file__))

# Criar a pasta 'instance' se não existir
instance_path = os.path.join(basedir, 'instance')
if not os.path.exists(instance_path):
    os.makedirs(instance_path)

# Inicializa Flask
app = Flask(__name__)
CORS(app)

# Configura banco SQLite
db_path = os.path.join(instance_path, 'prontuario_tamar.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de dados
class Prontuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dados = db.Column(db.JSON, nullable=False)
    pdf = db.Column(db.Text)  # Base64 do PDF
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Criar tabelas automaticamente
with app.app_context():
    db.create_all()

# Rota para receber dados
@app.route('/api/prontuarios', methods=['POST'])
def salvar_prontuario():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    novo = Prontuario(dados=data, pdf=data.get('pdf'))
    db.session.add(novo)
    db.session.commit()
    return jsonify({'message': 'Prontuário salvo com sucesso!'}), 201

# Rota para listar dados
@app.route('/api/prontuarios', methods=['GET'])
def listar_prontuarios():
    prontuarios = Prontuario.query.all()
    result = []
    for p in prontuarios:
        item = p.dados
        item['pdf'] = p.pdf
        item['id'] = p.id
        item['created_at'] = p.created_at.isoformat()
        result.append(item)
    return jsonify(result), 200

# Roda localmente
if __name__ == '__main__':
    app.run(debug=True)


