# 🚗 Sistema Especialista - Luzes do Painel

> Um sistema inteligente capaz de identificar e diagnosticar o significado das luzes de alerta no painel de veículos, desenvolvido para a disciplina de Inteligência Artificial.

![Badge Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)
![Badge Tkinter](https://img.shields.io/badge/Interface-Tkinter-blue?logo=python&logoColor=white)
![Badge Experta](https://img.shields.io/badge/Library-Experta-green)
![Badge Academic](https://img.shields.io/badge/Type-Academic%20Project-blue)

## 🏫 Sobre o Projeto

Este projeto foi desenvolvido como o 3º Trabalho da disciplina de **Inteligência Artificial** da **Universidade Estadual do Oeste do Paraná (Unioeste)**.

O objetivo é simular o raciocínio de um mecânico especialista. Através de uma base de conhecimento e um motor de inferência, o sistema faz perguntas ao usuário sobre quais símbolos estão acesos no painel e retorna o provável problema e a recomendação de ação.

## 🛠️ Tecnologias Utilizadas

* **[Python](https://www.python.org/)**: Linguagem base do projeto.
* **[Experta](https://pypi.org/project/experta/)**: Biblioteca para construção de sistemas especialistas baseada em regras (inspirada no CLIPS).
* **Tkinter**: Biblioteca padrão do Python utilizada para a construção da Interface Gráfica (GUI).

## 📂 Estrutura do Projeto

```bash
Sistema-Especialista/
├── src/                  # Código fonte (Interface e Regras)
├── Espeficações...pdf    # Documentação e regras do trabalho
├── requirements.txt      # Lista de dependências (Experta)
└── README.md             # Documentação do projeto
```

## 🚀 Como Executar

Para utilizar o sistema, você precisará do Python instalado.

### Passo a passo

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/yVinicin/Sistema-Especialista.git
    cd Sistema-Especialista
    ```

2.  **Crie um ambiente virtual (Opcional, mas recomendado):**
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # Linux/Mac:
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    Navegue até a pasta do código fonte e execute o arquivo principal (verifique se o nome é `main.py`, `app.py` ou `interface.py` dentro da pasta `src`).
    ```bash
    python src/main.py
    ```

## 🧠 Como Funciona?

1.  **Base de Conhecimento:** O sistema possui regras cadastradas (ex: "Se a luz é vermelha e parece um termômetro -> Superaquecimento").
2.  **Motor de Inferência:** Utiliza a biblioteca `Experta` para processar as entradas do usuário contra essas regras.
3.  **Interface Gráfica:** Uma janela Tkinter permite que o usuário selecione os sintomas visualmente e receba o diagnóstico.
