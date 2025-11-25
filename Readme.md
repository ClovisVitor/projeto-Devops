# Projeto de Avaliação - Devops 2025.2

![Status](https://img.shields.io/badge/Status-Desenvolvido-brightgreen)

---

## Descrição 📝

A aplicação se trada de um To Do List onde é possível gerenciar tarefas do dia a dia.

---

## Índice 📚
- [Requisitos](#requisitos-)
- [Tecnologias Utilizadas](#tecnologias-utilizadas-)
- [Estrutura do Projeto](#estrutura-do-projeto-)
- [Como Executar a Aplicação](#como-executar-a-aplicação-)
- [Testando a API com o Postman](#testando-a-api-com-postman-)
- [Links da Aplicação](#links-da-aplicação-)
- [Equipe](#equipe-)
---

## Requisitos ⚙️

- **Aplicação**
    - Elementos Get e Post, usando transferências de arquivos JSON.
    - Elementos de back-end e front-end.
- Armazenar e alterar dados em uma **Base de dados**.
- O Banco de Dados, Frontend e Banckend devem utilizar o **Docker**.
- **Git**
    - Utilizar no mínimo 3 Branchs.
    - Branchs devem atualizar um repositório no Github.
- A máquina deve estar em um ambiente da **AWS**.
- Atualizações nas branches **Staging** e **Master** devem atualizar os códigos da aplicação no servidor AWS.
- **Monitoramento**
    - Zabbix. 
    - Grafana.
- **Postman** para testes e documentação da API.
---
## Tecnologias Utilizadas 🛠️

| Tecnologia               | Descrição                                    |
|--------------------------|----------------------------------------------|
| Python                   | Linguagem de programação usada               |
| Html + JavaScript        | Frontend do Projeto                          |
| PostgreSQL               | Banco de Dados                               |
| Docker                   | Conteinerização                              |
| AWS EC2                  | Máquina de Produção em Nuvem                 |
| Zabbix e Grafana         | Monitoramento                                |
| Postman                  | Teste e Documentação da API                  |

---
## Estrutura do Projeto 📁
```
📌raíz
 ┣ 📂backend/
 ┃ ┣ 📜app.py
 ┃ ┣ 📜dockerfile
 ┃ ┗ 📄requirements.txt
 ┃ 📂frontend/
 ┃ ┣ 📜index.html
 ┃ ┗ 📜dockerfile
 ┣ 📜docker-compose.yml
 ┗ 📄Readme.md
```
---
## Como Executar a Aplicação 🚀

### 1. Importar o Projeto, Criar Banco e Configurar `.env`

1. Clone o repositório:

   ```bash
   git clone https://github.com/ClovisVitor/projeto-Devops
   ```
2. Acesse a pasta do projeto:

   ```bash
   cd projeto-Devops
   ```
3. Crie o banco de dados PostgreSQL ou banco da sua preferência:

   ```sql
   CREATE DATABASE nomedobanco;

   CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
    );

   ```
4. Crie o arquivo `.env` na pasta `backend/` com:

   ```env
    DB_NAME=nomedobanco
    DB_USER=usuario
    DB_PASSWORD=senha
    DB_HOST=db
    DB_PORT=5432
   ```
5. Crie o arquivo `.env` na pasta raíz `projeto-Devops/` com:

   ```env
    POSTGRES_USER=usuario
    POSTGRES_PASSWORD=senha
    POSTGRES_DB=nomedobanco

    DB_HOST=db
    DB_PORT=5432
    DB_USER=usuario
    DB_PASSWORD=senha
    DB_NAME=nomedobanco
   ```
### 2. Rodando a Aplicação com Docker

1. Na raiz do projeto, execute:

   ```bash
   docker compose up -d
   ```
2. A aplicação irá subir com backend, frontend e banco de dados.

### 3. Subindo em uma Instância EC2

1. Crie uma EC2 Ubuntu 22.04.
2. Instale Docker e Docker Compose:

   ```bash
   sudo apt update
   sudo apt install docker.io -y
   ```
3. Clone o projeto dentro da EC2 e rode `docker compose up -d`.

### 4. Branches e GitHub Actions

* **main** → Produção
* **staging** → Homologação
* **develop** → Desenvolvimento
* Workflow `.github/workflows/deploy.yml` faz deploy automático na EC2 ao receber push nas branchs `staging` ou `main`.

**No Github Actions siga esse caminho para criação das variavéis.**

1. No topo do repositório vá em Settings > Secrets and Variables > Actions > New repository secret.
2. Criar três variáveis.

| Name              | Value                   |
|-------------------|-------------------------|
| AWS_EC2_HOST      | IP público do EC2       |
| AWS_EC2_SSH_KEY   | Frontend do Projeto     |
| AWS_EC2_SSH_KEY   | Aqui você deve colar a chave privada PEM inteira.                               |

### 5. Monitoramento (Zabbix e Grafana)

1. Crie um novo EC2 utilizando o ubuntu Server 24.04, e com uma tipo de instancia mais robusta.

2. Acesse a EC2 via SSH e crie uma nova pasta `monitoramento/`.

3. Criar o arquivo `docker-compose.yml` dentro dela.
    ```bash
    nano docker-compose.yml
    ```
4. Cole esta configuração:
    ```bash
        version: '3.9'
        services:
        postgres:
        image: postgres:14
        environment:
        POSTGRES_USER: zabbix
        POSTGRES_PASSWORD: zabbix
        POSTGRES_DB: zabbix
        volumes:
        - pgdata:/var/lib/postgresql/data

    zabbix-server:
        image: zabbix/zabbix-server-pgsql:latest
        environment:
        DB_SERVER_HOST: postgres
        DB_SERVER_PORT: 5432
        POSTGRES_USER: zabbix
        POSTGRES_PASSWORD: zabbix
        POSTGRES_DB: zabbix
        ports:
        - "10051:10051"
        depends_on:
        - postgres

    zabbix-web:
        image: zabbix/zabbix-web-nginx-pgsql:latest
        environment:
        DB_SERVER_HOST: postgres
        DB_SERVER_PORT: 5432
        POSTGRES_USER: zabbix
        POSTGRES_PASSWORD: zabbix
        POSTGRES_DB: zabbix
        ZBX_SERVER_HOST: zabbix-server
        ports:
        - "8080:8080"
        depends_on:
        - zabbix-server

    grafana:
        image: grafana/grafana
        ports:
        - "3000:3000"

    volumes:
    pgdata:
    ```
**Como salvar no Nano:**

- Pressione Ctrl + O para salvar
- Pressione Enter para confirmar
- Pressione Ctrl + X para sair
5. Instalar o docker na EC2:
    ```bash
   sudo apt update
   sudo apt install docker.io -y
   sudo apt install docker-compose -y
   ```
   Adicione o usuário ubuntu ao grupo docker:
   ```bash
   sudo usermod -aG docker ubuntu
   ```
    Atualize a sessão: 
    ```bash
   newgrp docker
   ```
### 6. Subir o monitoramento:

   ```bash
   docker compose up -d
   ```
   Veirificar se os containers subiram:
   ```bash
   docker ps
   ```
    **Você deve ver algo como:**
    - zabbix-web
    -  zabbix-server
    - postgres
    - grafana
### 7. Liberar portas na EC2
    
    Na AWS → EC2 → Security Groups → sua instância

    Adicione **Regras de Saída**:
    | Porta | Serviço    | Protocolo | Origem    |
    | ----- | ---------- | --------- | --------- |
    | 8080  | Zabbix     | TCP       | 0.0.0.0/0 |
    | 3000  | Grafana    | TCP       | 0.0.0.0/0 |
    | 10051 | Zabbix Srv | TCP       | 0.0.0.0/0 |
    
### 8. Criar o Host de Monitoramento
    
    Acesse o Zabbix: http://IP:8080
    
    No Zabbix:

    1. Acesse o menu lateral:

        **Data Collection → Hosts**

    2. Clique em **Create Host**

    3. Preencha:
        - **Hostname:** todo-aplicacao
        - **Interfaces:** Agent (IP da EC2)
    4. Em templates, adicione:
        
        - **Linux by Zabbix agent**
        - **ICMP Ping**

    5. Salve e instale isso no EC2 de monitoramento:
        ```bash
        sudo apt update
        sudo apt install zabbix-agent -y
        sudo systemctl enable --now zabbix-agent
        ```
        Edite o arquivo de configuração:
        ```bash
        sudo nano /etc/zabbix/zabbix_agentd.conf
        ```
        Procure a linha: Server e edite para:
        ```bash
         Server=IP DO ZABBIX SERVER
        ```
        Salve com Ctrl + O, Enter, Ctrl + X.
        
        Reinicie:
        ```bash
        sudo systemctl restart zabbix-agent
        ```
### 9. Configuração do Grafana: 

    Acesse o Grafana: http://IP:3000

    1. Siga o caminho:
         
         Administration → Plugin and data  → Plugins  → Busque por Zabbix  → Install
    2. Após instalação do Zabbix ir para configuração seguindo o caminho: 
        
        Connections → Data sources  → Add new data source  → Zabbix 
    3. Preencha com os dados do Docker: 
       
        - URL: 
        - Access: Server (default)
        - Username: Admin
        - Password: zabbix (ou a sua senha)
    4. Importar o Dashboard
        1. Vá em Dashboard e clique em **New > Import**
        2. No campo onde diz "Import via grafana.com", digite apenas o número: 5363.
            - Este é o ID do dashboard "Zabbix - Linux Server".
        3. Vai aparecer uma tela de configuração. A única coisa que você precisa mudar é lá embaixo:
            - Onde diz **Zabbix** (ou Data Source), clique na lista e selecione o **Zabbix** que acabamos de configurar.
        4. Clique em **Import**.
    5. Como usar o Dashboard

        Assim que carregar, pode ser que ele mostre "No data" ou dados de outro servidor. Para ver a sua EC2:

        1. Olhe no topo do Dashboard, existem filtros (variáveis).

        2. Host Group: Geralmente pode deixar em "All" ou selecionar o grupo onde colocou sua EC2.

        3. Clique e selecione o seu Host (todo-aplicacao).
---
## Links da Aplicação 🌐

**Link:** [To Do List](http://13.222.108.176:8080/)

**Link:** [Zabbix](http://3.218.244.196:8080/)

**Link:** [Grafana](http://3.218.244.196:3000/)

**Link:** [Documentação Postman](https://documenter.getpostman.com/view/50174126/2sB3dHWCzw)

---
## Equipe 👥
#### [👤 Clovis Vitor: 01564866](https://github.com/ClovisVitor)
#### [👤 Maria Christina: 01565538](https://github.com/mariachrixtina)