FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia requirements e instala dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código
COPY . .

# Expõe a porta usada pelo Flask
EXPOSE 5000

# Comando para iniciar o app
CMD ["python", "app.py"]