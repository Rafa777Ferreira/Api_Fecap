from flask import Flask, render_template, request, jsonify
import database_config
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from sqlalchemy.exc import SQLAlchemyError

plt.switch_backend('Agg')

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco_combustivel.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

database_config.init_db(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test_grafico')
def test_grafico():
    try:
        ano = request.args.get('ano', type=int, default=2019)
        estado = request.args.get('estado', default='SP')
        produto = request.args.get('produto', default='Gasolina')

        query = database_config.Combustivel.query.filter_by(ano=ano, estado=estado, produto=produto).statement
        df = pd.read_sql(query, database_config.db.engine)

        df['media_mensal_valor_venda'] = pd.to_numeric(df['media_mensal_valor_venda'], errors='coerce')
        df = df.dropna(subset=['media_mensal_valor_venda'])

        if df.empty:
            return jsonify({"error": "Nenhum dado encontrado para os filtros selecionados"}), 404

        media_mensal = df.groupby('mes')['media_mensal_valor_venda'].mean()

        plt.figure(figsize=(10, 5))
        media_mensal.plot(kind='bar', color='skyblue')
        plt.title(f'Média Mensal do Preço de {produto} em {ano} - {estado}')
        plt.xlabel('Mês')
        plt.ylabel('Preço Médio')

        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close('all')
        img_base64 = base64.b64encode(img.getvalue()).decode()

        return jsonify({"grafico": img_base64})

    except SQLAlchemyError as e:
        return jsonify({"error": "Erro ao acessar o banco de dados", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Erro ao gerar o gráfico", "details": str(e)}), 500

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
