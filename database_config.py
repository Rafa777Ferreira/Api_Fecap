from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Combustivel(db.Model):
    __tablename__ = 'tabela_combustivel'
    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer)
    mes = db.Column(db.String)
    estado = db.Column(db.String)
    produto = db.Column(db.String)
    media_mensal_valor_venda = db.Column(db.Float)

def init_db(app):
    db.init_app(app)
