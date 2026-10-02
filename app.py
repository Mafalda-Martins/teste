import streamlit as st
import random

st.set_page_config(page_title="Jogo", page_icon="🎮")

st.title("🎮 Adivinha o Número")

if "numero" not in st.session_state:
    st.session_state.numero = random.randint(1, 100)
    st.session_state.tentativas = 0

palpite = st.number_input(
    "Escolhe um número",
    min_value=1,
    max_value=100,
    step=1
)

if st.button("Verificar"):
    st.session_state.tentativas += 1

    if palpite < st.session_state.numero:
        st.warning("⬆️ Mais alto")
    elif palpite > st.session_state.numero:
        st.warning("⬇️ Mais baixo")
    else:
        st.success(
            f"🎉 Acertaste em {st.session_state.tentativas} tentativas!"
        )
        st.balloons()

if st.button("Novo Jogo"):
    st.session_state.numero = random.randint(1, 100)
    st.session_state.tentativas = 0
    st.rerun()

st.write(f"Tentativas: {st.session_state.tentativas}")
