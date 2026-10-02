import streamlit as st
import random

st.set_page_config(page_title="Mini RPG", page_icon="⚔️")

# Estado inicial
if "hp" not in st.session_state:
    st.session_state.hp = 100
    st.session_state.gold = 0
    st.session_state.level = 1
    st.session_state.enemy_hp = 50

st.title("⚔️ Mini RPG")

# Herói
st.subheader("🧝 Heroína")

st.progress(st.session_state.hp / 100)
st.write(f"❤️ Vida: {st.session_state.hp}")
st.write(f"⭐ Nível: {st.session_state.level}")
st.write(f"💰 Ouro: {st.session_state.gold}")

st.divider()

# Monstro muda consoante o nível
monsters = [
    ("🐺 Lobo", 50),
    ("👺 Goblin", 70),
    ("💀 Esqueleto", 90),
    ("👹 Ogro", 120),
]

monster_name, _ = monsters[min(st.session_state.level - 1, len(monsters)-1)]

st.subheader(monster_name)

st.progress(max(st.session_state.enemy_hp, 0) / 120)
st.write(f"❤️ Vida do inimigo: {max(st.session_state.enemy_hp, 0)}")

col1, col2 = st.columns(2)

with col1:
    if st.button("⚔️ Atacar"):
        damage = random.randint(10, 25)
        st.session_state.enemy_hp -= damage
        st.success(f"Causaste {damage} de dano!")

        if st.session_state.enemy_hp <= 0:
            st.balloons()
            st.success("🏆 Inimigo derrotado!")

            st.session_state.gold += random.randint(20, 50)
            st.session_state.level += 1

            novo_hp = 50 + st.session_state.level * 20
            st.session_state.enemy_hp = novo_hp

with col2:
    if st.button("🧪 Curar"):
        heal = random.randint(10, 20)
        st.session_state.hp = min(100, st.session_state.hp + heal)
        st.info(f"Recuperaste {heal} HP!")

st.divider()

if st.button("🔄 Novo Jogo"):
    st.session_state.hp = 100
    st.session_state.gold = 0
    st.session_state.level = 1
    st.session_state.enemy_hp = 50
    st.rerun()

# Pequena história
if st.session_state.level >= 5:
    st.warning("🐉 O Dragão aproxima-se...")
