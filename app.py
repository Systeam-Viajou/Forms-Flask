from flask import Flask, render_template, request, url_for
from dotenv import load_dotenv
import pandas as pd
from psycopg2 import pool
import psycopg2
import joblib
import os

app = Flask(__name__)

# Carregar variáveis de ambiente
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def response(type):
    return f"""
                            <html>
                            <head>
                                <style>
                                    body, html {{
                                        height: 100%;
                                        margin: 0;
                                    }}
                                    .full-bg {{
                                        background-image: url('{type}');
                                        height: 100%;
                                        background-position: center;
                                        background-size: cover;
                                        background-repeat: no-repeat;
                                    }}
                                </style>
                            </head>
                            <body>
                                <div class="full-bg"></div>
                            </body>
                            </html>
                            """


def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname='dbviajou2',
            user=os.getenv('POSTGRE_USER'),
            password=os.getenv('POSTGRE_PASSWORD'),
            host=os.getenv('POSTGRE_HOST'),
            port=os.getenv('POSTGRE_PORT')
        )
        if conn:
            print("Conexão com DB2 estabelecida.")
            return conn
    except Exception as e:
        print(f"Erro ao conectar ao DB2: {e}")
        return None


@app.route("/", methods=["GET"])
def home():
    uuid = url_for("static", filename="uuid.jpg")
    return response(uuid)


@app.route("/<name>", methods=["GET", "POST"])
def pesquisa(name):
    connection = get_db_connection()
    if not connection:
        return "Erro de conexão com o banco de dados.", 500

    if request.method == "POST":
        # Processamento do formulário
        df = pd.DataFrame(
            {
                "idade": [request.form.get("idade")],
                "genero": [request.form.get("genero")],
                "municipio_residencia": [request.form.get("municipio_residencia")],
                "visita_pontos_turisticos": [
                    request.form.get("visita_pontos_turisticos")
                ],
                "participa_eventos": [request.form.get("participa_eventos")],
                "frequencia_eventos": [request.form.get("frequencia_eventos")],
                "tipos_eventos_preferidos": [
                    ",".join(request.form.getlist("tipos_eventos_preferidos"))
                ],
                "participa_excursões": [request.form.get("participa_excursões")],
                "frequencia_tours_virtuais": [
                    request.form.get("frequencia_tours_virtuais")
                ],
                "frequencia_apps_turismo": [
                    request.form.get("frequencia_apps_turismo")
                ],
                "usou_apps_turismo": [request.form.get("usou_apps_turismo")],
                "confianca_avaliacoes": [request.form.get("confianca_avaliacoes")],
                "interesse_acessibilidade": [
                    request.form.get("interesse_acessibilidade")
                ],
                "pagaria_por_tour_virtual": [
                    request.form.get("pagaria_por_tour_virtual")
                ],
                "descoberta_eventos_atracoes": [
                    ",".join(request.form.getlist("descoberta_eventos_atracoes"))
                ],
                "motivacao_uso_app_turismo": [
                    request.form.get("motivacao_uso_app_turismo")
                ],
            }
        )

        model_pipeline = joblib.load(
            os.path.join(BASE_DIR, "modelo_com_preprocessador.joblib")
        )
        previsao = int(model_pipeline.predict(df)[0])

        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO resposta_usuario (id_usuario, resposta) VALUES (%s, %s)",
                    (name, previsao),
                )
                connection.commit()
        finally:
            connection.close()

        image_file = "recomenda.jpg" if previsao == 1 else "naorecomenda.jpg"
        result = url_for("static", filename=image_file)

        return response(result)

    # GET request: renderizar o formulário
    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
