import psycopg2
import os 
from dotenv import load_dotenv

load_dotenv()

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

    cursor = conn.cursor()

    # Consulta básica
    cursor.execute("SELECT * FROM tasks;")

    dados = cursor.fetchall()

    print("Dados retornados:")
    for linha in dados:
        print(linha)

    cursor.close()
    conn.close()

except Exception as e:
    print("Erro ao conectar:", e)
