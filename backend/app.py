import psycopg2
import os 
from dotenv import load_dotenv
from flask import Flask, request, jsonify

# Carrega Váriaveis do ambiente.
load_dotenv()

# Configuração Flask
app = Flask(__name__)


try:
    # Criar conexão
    conn = psycopg2.connect(
        database = os.getenv("DB_NAME"),
        user= os.getenv("DB_USER"),
        password= os.getenv("DB_PASSWORD"),
        host= os.getenv("DB_HOST"),
        port= os.getenv("DB_PORT")
    )

    print("Conexão bem-sucedida!")

except Exception as e:
    print("Erro ao conectar:", e)

# FUNÇÃO PARA CONEXÃO (necessária para as rotas) 
def get_connection():
    return psycopg2.connect(
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

#Rota Post

@app.post("/tasks")
def add_task():
    data = request.json
    title = data.get("title")
    done = data.get("done", False)  # caso não seja enviado, assume False

    if not title:
        return jsonify({"error": "title é obrigatório"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO tasks (title, done)
            VALUES (%s, %s)
            RETURNING id;
        """, (title, done))

        task_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "message": "Task adicionada com sucesso!",
            "task_id": task_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# -------------------------------
# Servidor Flask
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)