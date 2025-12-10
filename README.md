# 🚗 Sistema Especialista - Luzes do Painel

> Um sistema inteligente capaz de identificar e diagnosticar o significado das luzes de alerta no painel de veículos, desenvolvido para a disciplina de Inteligência Artificial.

![Badge Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python&logoColor=white)
![Badge Streamlit](https://img.shields.io/badge/Frontend-Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Badge Experta](https://img.shields.io/badge/Library-Experta-green)
![Badge Academic](https://img.shields.io/badge/Type-Academic%20Project-blue)

## 🏫 Sobre o Projeto

Este projeto foi desenvolvido como o 3º Trabalho da disciplina de **Inteligência Artificial** da **Universidade Estadual do Oeste do Paraná (Unioeste)**.

O objetivo é simular o raciocínio de um mecânico especialista. Através de uma base de conhecimento e um motor de inferência, o sistema faz perguntas ao usuário sobre quais símbolos estão acesos no painel e retorna o provável problema e a recomendação de ação.

## 🛠️ Tecnologias Utilizadas

* **[Python](https://www.python.org/)**: Linguagem base do projeto.
* **[Experta](https://pypi.org/project/experta/)**: Biblioteca para construção de sistemas especialistas baseada em regras (inspirada no CLIPS).
* **[Streamlit](https://streamlit.io/)**: Framework para criação da interface web interativa.

## 📂 Estrutura do Projeto

```bash
Sistema-Especialista/
├── src/                  # Código fonte do sistema
├── Espeficações...pdf    # Documentação e regras do trabalho
├── requirements.txt      # Lista de dependências
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
    O comando abaixo iniciará a interface no seu navegador.
    ```bash
    streamlit run src/app.py
    ```
    *(Nota: Verifique dentro da pasta `src` qual é o arquivo principal, geralmente é `app.py`, `main.py` ou `interface.py`).*

## 🧠 Como Funciona?

1.  **Base de Conhecimento:** O sistema possui regras cadastradas (ex: "Se a luz é vermelha e parece um termômetro -> Superaquecimento").
2.  **Motor de Inferência:** Utiliza a biblioteca `Experta` para processar as entradas do usuário contra essas regras.
3.  **Diagnóstico:** O sistema exibe o significado da luz (Alerta, Perigo, Informativo) e o que o motorista deve fazer.
