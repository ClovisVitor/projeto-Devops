import psycopg2
import os 
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# Carrega Váriaveis do ambiente.
load_dotenv()

# Configuração Flask
app = Flask(__name__)
CORS(app)

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
    
    
    # ROTA GET → listar todas as tasks
@app.get("/tasks")
def get_tasks():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, title, done
            FROM tasks
            ORDER BY id;
        """)

        rows = cur.fetchall()

        tasks = []
        for row in rows:
            tasks.append({
                "id": row[0],
                "title": row[1],
                "done": row[2]
            })

        cur.close()
        conn.close()

        return jsonify(tasks), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# ROTA PUT → atualizar o campo "done" da task
@app.put("/tasks/<int:task_id>")
def update_task(task_id):
    data = request.json
    done = data.get("done")

    # Validação
    if done is None:
        return jsonify({"error": "'done' é obrigatório e deve ser true ou false"}), 400

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE tasks
            SET done = %s
            WHERE id = %s
            RETURNING id, title, done;
        """, (done, task_id))

        updated = cur.fetchone()
        conn.commit()

        cur.close()
        conn.close()

        # Se não existir task com esse ID
        if not updated:
            return jsonify({"error": "Task não encontrada"}), 404

        return jsonify({
            "message": "Task atualizada com sucesso!",
            "task": {
                "id": updated[0],
                "title": updated[1],
                "done": updated[2]
            }
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# ROTA DELETE → remover uma task
@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    try:
        conn = get_connection()
        cur = conn.cursor()

        # Deleta e retorna o ID deletado (se existir)
        cur.execute("""
            DELETE FROM tasks
            WHERE id = %s
            RETURNING id;
        """, (task_id,))

        deleted = cur.fetchone()
        conn.commit()

        cur.close()
        conn.close()

        if not deleted:
            return jsonify({"error": "Task não encontrada"}), 404

        return jsonify({
            "message": "Task deletada com sucesso!",
            "task_id": deleted[0]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT FALSE
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Tabela 'tasks' verificada/criada com sucesso!")


# -------------------------------
# Servidor Flask
# -------------------------------
if __name__ == "__main__":
    init_db()   # garante que a tabela existe
    app.run(host="0.0.0.0", port=5000, debug=True)