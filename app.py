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

# Configurar pool de conexões para o banco de dados
db_pool = psycopg2.pool.SimpleConnectionPool(
    1, 20, os.getenv("POSTGRE2_URL")  # Min e max de conexões
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_db_connection():
    try:
        conn = db_pool.getconn()
        if conn:
            print("Conexão com DB2 estabelecida.")
            return conn
    except Exception as e:
        print(f"Erro ao conectar ao DB2: {e}")
        return None


@app.route("/<uid>", methods=["GET", "POST"])
def pesquisa(uid):
    connection = get_db_connection()
    if not connection:
        return "Erro de conexão com o banco de dados.", 500

    # Verificar se o UID existe no banco de dados
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT uid FROM usuario WHERE uid = %s", (uid,))
            result = cursor.fetchone()
            if result is None:
                erro = url_for("static", filename="erro.jpg")
                return f"""
                            <html>
                            <head>
                                <style>
                                    body, html {{
                                        height: 100%;
                                        margin: 0;
                                    }}
                                    .full-bg {{
                                        background-image: url('{erro}');
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

            cursor.execute("SELECT * FROM  resposta_usuario WHERE id_usuario = %s", (uid,))
            result = cursor.fetchone()
            if result is not None:
                return """
                            <html>
                            <head>
                                <style>
                                    body, html {{
                                        height: 100%;
                                        margin: 0;
                                    }}
                                    .full-bg {{
                                        background-color: #D0CAD3;
                                        height: 100%;
                                        background-position: center;
                                        background-size: cover;
                                        background-repeat: no-repeat;
                                    }}
                                </style>
                            </head>
                            <body>
                                <h1>Você já respondeu este formulário!</h1>
                            </body>
                            </html>
                            """.format(image_url=result[1])
    except Exception as e:
        print(f"Erro ao verificar UID: {e}")
        return "Erro ao verificar o usuário.", 500
    finally:
        db_pool.putconn(connection)

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

        print(previsao)
        try:
            connection = get_db_connection()
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO resposta_usuario (id_usuario, resposta) VALUES (%s, %s)",
                    (uid, previsao),
                )
                connection.commit()
        finally:
            db_pool.putconn(connection)  # Devolve a conexão ao pool

        image_file = "recomenda (7).jpg" if previsao == 1 else "naorecomenda (3).jpg"
        result = url_for("static", filename=image_file)

        return f"""
                            <html>
                            <head>
                                <style>
                                    body, html {{
                                        height: 100%;
                                        margin: 0;
                                    }}
                                    .full-bg {{
                                        background-image: url('{result}');
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

    # GET request: renderizar o formulário
    return render_template("form.html")


if __name__ == "__main__":
    app.run(debug=True)
