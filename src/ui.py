import streamlit as st
from main import executar_diagnostico, formatar_diagnostico_para_usuario

# Aplicar CSS simples
st.markdown(
    """
    <style>
    .block-container {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
        padding: 20px;
        margin: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Sistema Especialista: Diagnóstico da Luzes de Painel de Carros Flex")
st.markdown("**Clique na luz que estiver acesa no painel do seu carro.**")
st.markdown("---")

# Layout simples para bateria
st.markdown("### Bateria")
bateria = st.checkbox("Acesa", key="bateria")

luzes_acesas = {
    'bateria': bateria
}



# Inicializar estado da sessão
if 'pergunta_atual' not in st.session_state:
    st.session_state.pergunta_atual = 0
if 'respostas' not in st.session_state:
    st.session_state.respostas = {}
if 'diagnostico_final' not in st.session_state:
    st.session_state.diagnostico_final = None

# Função para resetar sessão
def resetar_sessao():
    st.session_state.pergunta_atual = 0
    st.session_state.respostas = {}
    st.session_state.diagnostico_final = None

# Definir perguntas baseadas na luz da bateria
perguntas_por_luz = {
    'bateria': [
        {"pergunta": "As conexões da bateria estão soltas?", "acao_sim": "Conecte as conexões firmemente.", "acao_nao": None, "proxima": 1},
        {"pergunta": "Há corrosão nos terminais da bateria?", "acao_sim": "Limpe os terminais com uma solução de bicarbonato de sódio e água.", "acao_nao": None, "proxima": 2},
        {"pergunta": "A bateria tem mais de 3 anos?", "acao_sim": "Substitua a bateria.", "acao_nao": "Verifique o alternador com um multímetro.", "proxima": None}
    ]
}

# Botão para iniciar diagnóstico interativo
st.markdown("---")
if st.button("Iniciar Diagnóstico Interativo", type="primary"):
    resetar_sessao()
    luzes_selecionadas = [luz for luz, acesa in luzes_acesas.items() if acesa]
    if luzes_selecionadas:
        st.session_state.luzes_selecionadas = luzes_selecionadas
        st.rerun()
    else:
        st.warning("Selecione pelo menos uma luz acesa.")

# Lógica do diagnóstico interativo
if 'luzes_selecionadas' in st.session_state and st.session_state.pergunta_atual < len(st.session_state.luzes_selecionadas):
    luz_atual = st.session_state.luzes_selecionadas[st.session_state.pergunta_atual]
    if luz_atual in perguntas_por_luz:
        perguntas = perguntas_por_luz[luz_atual]
        pergunta_idx = st.session_state.get('pergunta_idx', 0)
        if pergunta_idx < len(perguntas):
            pergunta = perguntas[pergunta_idx]
            st.subheader(f"Diagnóstico para Luz: {luz_atual.upper()}")
            st.write(f"**Pergunta {pergunta_idx + 1}:** {pergunta['pergunta']}")

            col_sim, col_nao = st.columns(2)
            with col_sim:
                if st.button("Sim", key=f"sim_{luz_atual}_{pergunta_idx}"):
                    st.session_state.respostas[f"{luz_atual}_{pergunta_idx}"] = "sim"
                    if pergunta['acao_sim']:
                        st.success(f"Ação recomendada: {pergunta['acao_sim']}")
                    if pergunta['proxima'] is not None:
                        st.session_state.pergunta_idx = pergunta['proxima']
                    else:
                        st.session_state.pergunta_atual += 1
                        st.session_state.pergunta_idx = 0
                    st.rerun()

            with col_nao:
                if st.button("Não", key=f"nao_{luz_atual}_{pergunta_idx}"):
                    st.session_state.respostas[f"{luz_atual}_{pergunta_idx}"] = "nao"
                    if pergunta['acao_nao']:
                        st.info(f"Próxima ação: {pergunta['acao_nao']}")
                    if pergunta['proxima'] is not None:
                        st.session_state.pergunta_idx = pergunta['proxima']
                    else:
                        st.session_state.pergunta_atual += 1
                        st.session_state.pergunta_idx = 0
                    st.rerun()
        else:
            st.session_state.pergunta_atual += 1
            st.session_state.pergunta_idx = 0
            st.rerun()
    else:
        st.session_state.pergunta_atual += 1
        st.rerun()

# Diagnóstico final
if 'luzes_selecionadas' in st.session_state and st.session_state.pergunta_atual >= len(st.session_state.luzes_selecionadas):
    st.success("Diagnóstico interativo concluído!")
    st.write("**Resumo das ações recomendadas:**")
    for resposta, valor in st.session_state.respostas.items():
        luz, idx = resposta.split('_')
        if valor == "sim":
            acao = perguntas_por_luz[luz][int(idx)]['acao_sim']
            st.write(f"- Para {luz}: {acao}")
    st.info("Lembre-se: Este é um sistema de apoio. Sempre consulte um mecânico para confirmação.")
    if st.button("Reiniciar Diagnóstico"):
        resetar_sessao()
        st.rerun()

# Informações
with st.expander("Sobre"):
    st.write("**Equipe:** Felipe, Lucas, Thalita e Vinícius Marcos")
    st.write("**Especialista:** Lenir I. Wiederkehr")
    st.write("**Shell:** Experta")
    st.write("**Interface:** Streamlit")
