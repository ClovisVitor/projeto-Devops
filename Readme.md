# Projeto de Avaliação - Devops 2025.2

![Status](https://img.shields.io/badge/Status-Desenvolvido-brightgreen)

---

## Descrição 📝

A aplicação se trada de um To Do List onde é possível gerenciar tarefas do dia a dia.

---

## Requisitos

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

## Tecnologias Utilizadas

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

## 📁 Estrutura (de pastas) do projeto
```
📌raíz
 ┣ 📂backend/
 ┃ ┣ 📜app.py
 ┃ ┣ 📜dockerfile
 ┃ ┗ 📜requirements.txt
 ┃ 📂frontend/
 ┃ ┣ 📜index.html
 ┃ ┗ 📜dockerfile
 ┣ 📜docker-compose.yml
 ┗ 📜Readme.md
```
---

---
