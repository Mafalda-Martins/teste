import random
import streamlit as st

st.set_page_config(
    page_title="Crónicas de Eldoria",
    page_icon="⚔️",
    layout="wide"
)

# -----------------------------
# ESTILO
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #090d18 0%, #18213a 55%, #291b3c 100%);
        color: white;
    }

    .game-title {
        text-align: center;
        font-size: 55px;
        font-weight: 900;
        color: #f4c95d;
        text-shadow: 0 0 18px rgba(244, 201, 93, 0.5);
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #d5d9e5;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .card {
        background: rgba(18, 25, 45, 0.92);
        border: 1px solid rgba(244, 201, 93, 0.35);
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.30);
    }

    .hero-name {
        color: #f4c95d;
        font-size: 28px;
        font-weight: 800;
    }

    .enemy-name {
        color: #ff6b6b;
        font-size: 28px;
        font-weight: 800;
    }

    .log-box {
        background: rgba(5, 8, 15, 0.80);
        border-left: 5px solid #f4c95d;
        border-radius: 10px;
        padding: 16px;
        min-height: 180px;
        max-height: 300px;
        overflow-y: auto;
    }

    div.stButton > button {
        width: 100%;
        border-radius: 12px;
        min-height: 48px;
        font-weight: 700;
        border: 1px solid rgba(244, 201, 93, 0.5);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# DADOS BASE
# -----------------------------
CLASSES = {
    "Guerreira": {
        "emoji": "⚔️",
        "vida": 130,
        "ataque": 18,
        "defesa": 7,
        "especial": "Golpe Devastador"
    },
    "Maga": {
        "emoji": "🔮",
        "vida": 95,
        "ataque": 25,
        "defesa": 3,
        "especial": "Explosão Arcana"
    },
    "Arqueira": {
        "emoji": "🏹",
        "vida": 110,
        "ataque": 21,
        "defesa": 5,
        "especial": "Chuva de Flechas"
    }
}

MONSTROS = [
    {
        "nome": "Goblin Saqueador",
        "emoji": "👺",
        "vida": 55,
        "ataque": 12,
        "ouro": 20,
        "xp": 25
    },
    {
        "nome": "Lobo Sombrio",
        "emoji": "🐺",
        "vida": 70,
        "ataque": 15,
        "ouro": 26,
        "xp": 32
    },
    {
        "nome": "Esqueleto Guerreiro",
        "emoji": "💀",
        "vida": 85,
        "ataque": 17,
        "ouro": 34,
        "xp": 40
    },
    {
        "nome": "Ogro das Montanhas",
        "emoji": "👹",
        "vida": 115,
        "ataque": 21,
        "ouro": 48,
        "xp": 55
    },
    {
        "nome": "Feiticeiro Corrompido",
        "emoji": "🧙",
        "vida": 130,
        "ataque": 24,
        "ouro": 65,
        "xp": 70
    }
]

BOSS = {
    "nome": "Dragão de Eldoria",
    "emoji": "🐉",
    "vida": 260,
    "ataque": 30,
    "ouro": 250,
    "xp": 200,
    "boss": True
}

# -----------------------------
# FUNÇÕES
# -----------------------------
def iniciar_estado():
    valores = {
        "jogo_iniciado": False,
        "nome": "",
        "classe": "",
        "nivel": 1,
        "xp": 0,
        "xp_necessario": 100,
        "vida": 100,
        "vida_maxima": 100,
        "ataque": 15,
        "defesa": 5,
        "ouro": 35,
        "pocoes": 3,
        "inimigo": None,
        "turno": 1,
        "vitorias": 0,
        "defendendo": False,
        "especial_disponivel": True,
        "fim": False,
        "vitoria_final": False,
        "registo": []
    }

    for chave, valor in valores.items():
        if chave not in st.session_state:
            st.session_state[chave] = valor


def adicionar_log(mensagem):
    st.session_state.registo.insert(0, mensagem)
    st.session_state.registo = st.session_state.registo[:12]


def criar_heroi(nome, classe):
    dados = CLASSES[classe]

    st.session_state.nome = nome
    st.session_state.classe = classe
    st.session_state.nivel = 1
    st.session_state.xp = 0
    st.session_state.xp_necessario = 100
    st.session_state.vida_maxima = dados["vida"]
    st.session_state.vida = dados["vida"]
    st.session_state.ataque = dados["ataque"]
    st.session_state.defesa = dados["defesa"]
    st.session_state.ouro = 35
    st.session_state.pocoes = 3
    st.session_state.turno = 1
    st.session_state.vitorias = 0
    st.session_state.defendendo = False
    st.session_state.especial_disponivel = True
    st.session_state.inimigo = None
    st.session_state.fim = False
    st.session_state.vitoria_final = False
    st.session_state.registo = [
        f"🌟 {nome}, a {classe}, iniciou a aventura em Eldoria."
    ]
    st.session_state.jogo_iniciado = True


def criar_inimigo():
    if st.session_state.vitorias >= 5:
        inimigo = BOSS.copy()
    else:
        indice_maximo = min(
            len(MONSTROS) - 1,
            st.session_state.vitorias
        )
        inimigo = random.choice(MONSTROS[:indice_maximo + 1]).copy()

        escala = 1 + (st.session_state.nivel - 1) * 0.12
        inimigo["vida"] = int(inimigo["vida"] * escala)
        inimigo["ataque"] = int(inimigo["ataque"] * escala)

    inimigo["vida_maxima"] = inimigo["vida"]
    st.session_state.inimigo = inimigo
    st.session_state.especial_disponivel = True
    adicionar_log(
        f"{inimigo['emoji']} {inimigo['nome']} apareceu!"
    )


def ataque_inimigo():
    if not st.session_state.inimigo:
        return

    inimigo = st.session_state.inimigo
    dano_base = random.randint(
        max(1, inimigo["ataque"] - 4),
        inimigo["ataque"] + 4
    )

    defesa = st.session_state.defesa

    if st.session_state.defendendo:
        defesa += 12
        st.session_state.defendendo = False

    dano = max(1, dano_base - defesa)

    if random.random() < 0.10:
        dano *= 2
        adicionar_log(
            f"💢 Ataque crítico inimigo: recebeste {dano} de dano."
        )
    else:
        adicionar_log(
            f"{inimigo['emoji']} O inimigo causou {dano} de dano."
        )

    st.session_state.vida = max(
        0,
        st.session_state.vida - dano
    )

    if st.session_state.vida <= 0:
        st.session_state.fim = True
        adicionar_log("☠️ Caíste em combate. Eldoria permanece em perigo.")


def verificar_nivel():
    while st.session_state.xp >= st.session_state.xp_necessario:
        st.session_state.xp -= st.session_state.xp_necessario
        st.session_state.nivel += 1
        st.session_state.xp_necessario = int(
            st.session_state.xp_necessario * 1.35
        )
        st.session_state.vida_maxima += 18
        st.session_state.vida = st.session_state.vida_maxima
        st.session_state.ataque += 4
        st.session_state.defesa += 2
        adicionar_log(
            f"⬆️ Subiste para o nível {st.session_state.nivel}! "
            "A vida foi restaurada."
        )


def derrotar_inimigo():
    inimigo = st.session_state.inimigo

    st.session_state.ouro += inimigo["ouro"]
    st.session_state.xp += inimigo["xp"]

    adicionar_log(
        f"🏆 Derrotaste {inimigo['nome']} e recebeste "
        f"{inimigo['ouro']} moedas e {inimigo['xp']} XP."
    )

    if inimigo.get("boss"):
        st.session_state.vitoria_final = True
        st.session_state.fim = True
        adicionar_log("👑 O Dragão caiu. Eldoria foi salva!")
    else:
        st.session_state.vitorias += 1

    st.session_state.inimigo = None
    verificar_nivel()


def atacar():
    inimigo = st.session_state.inimigo

    dano = random.randint(
        max(1, st.session_state.ataque - 5),
        st.session_state.ataque + 7
    )

    if random.random() < 0.18:
        dano *= 2
        adicionar_log(f"✨ Ataque crítico! Causaste {dano} de dano.")
    else:
        adicionar_log(f"⚔️ Causaste {dano} de dano.")

    inimigo["vida"] = max(0, inimigo["vida"] - dano)
    st.session_state.turno += 1

    if inimigo["vida"] <= 0:
        derrotar_inimigo()
    else:
        ataque_inimigo()


def ataque_especial():
    if not st.session_state.especial_disponivel:
        return

    inimigo = st.session_state.inimigo
    classe = CLASSES[st.session_state.classe]

    dano = random.randint(
        int(st.session_state.ataque * 1.7),
        int(st.session_state.ataque * 2.4)
    )

    inimigo["vida"] = max(0, inimigo["vida"] - dano)
    st.session_state.especial_disponivel = False
    st.session_state.turno += 1

    adicionar_log(
        f"🔥 {classe['especial']} causou {dano} de dano!"
    )

    if inimigo["vida"] <= 0:
        derrotar_inimigo()
    else:
        ataque_inimigo()


def defender():
    st.session_state.defendendo = True
    st.session_state.turno += 1
    adicionar_log("🛡️ Preparaste uma defesa reforçada.")
    ataque_inimigo()


def usar_pocao():
    if st.session_state.pocoes <= 0:
        adicionar_log("❌ Não tens poções.")
        return

    if st.session_state.vida >= st.session_state.vida_maxima:
        adicionar_log("ℹ️ A tua vida já está no máximo.")
        return

    cura = min(
        45,
        st.session_state.vida_maxima - st.session_state.vida
    )

    st.session_state.vida += cura
    st.session_state.pocoes -= 1
    st.session_state.turno += 1

    adicionar_log(f"🧪 Recuperaste {cura} pontos de vida.")

    if st.session_state.inimigo:
        ataque_inimigo()


def descansar():
    custo = 18

    if st.session_state.ouro < custo:
        adicionar_log("❌ Não tens ouro suficiente para descansar.")
        return

    st.session_state.ouro -= custo
    st.session_state.vida = st.session_state.vida_maxima
    adicionar_log("🏕️ Descansaste na estalagem e recuperaste toda a vida.")


def comprar_pocao():
    custo = 15

    if st.session_state.ouro < custo:
        adicionar_log("❌ Não tens ouro suficiente.")
        return

    st.session_state.ouro -= custo
    st.session_state.pocoes += 1
    adicionar_log("🧪 Compraste uma poção por 15 moedas.")


def melhorar_arma():
    custo = 55 + (st.session_state.ataque * 2)

    if st.session_state.ouro < custo:
        adicionar_log(
            f"❌ Precisas de {custo} moedas para melhorar a arma."
        )
        return

    st.session_state.ouro -= custo
    st.session_state.ataque += 4
    adicionar_log(
        f"🔨 A arma foi melhorada. Ataque atual: "
        f"{st.session_state.ataque}."
    )


def reiniciar():
    for chave in list(st.session_state.keys()):
        del st.session_state[chave]
    st.rerun()


# -----------------------------
# INÍCIO DO JOGO
# -----------------------------
iniciar_estado()

st.markdown(
    '<div class="game-title">⚔️ Crónicas de Eldoria</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="subtitle">'
    'Cria uma heroína, derrota os monstros e enfrenta o Dragão.'
    '</div>',
    unsafe_allow_html=True
)

if not st.session_state.jogo_iniciado:
    st.markdown("## 🧙 Criar personagem")

    coluna1, coluna2 = st.columns([1, 1])

    with coluna1:
        nome = st.text_input(
            "Nome da personagem",
            placeholder="Escreve um nome..."
        )

        classe = st.selectbox(
            "Escolhe uma classe",
            list(CLASSES.keys())
        )

    with coluna2:
        dados = CLASSES[classe]

        st.markdown(
            f"""
            <div class="card">
                <div class="hero-name">
                    {dados["emoji"]} {classe}
                </div>
                <p>❤️ Vida: {dados["vida"]}</p>
                <p>⚔️ Ataque: {dados["ataque"]}</p>
                <p>🛡️ Defesa: {dados["defesa"]}</p>
                <p>🔥 Especial: {dados["especial"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.button("🌟 Começar aventura", type="primary"):
        if nome.strip():
            criar_heroi(nome.strip(), classe)
            st.rerun()
        else:
            st.warning("Escreve primeiro o nome da personagem.")

else:
    if st.session_state.fim:
        if st.session_state.vitoria_final:
            st.success(
                f"👑 Vitória! {st.session_state.nome} derrotou o "
                "Dragão de Eldoria!"
            )
            st.balloons()
        else:
            st.error(
                f"☠️ {st.session_state.nome} foi derrotada no campo "
                "de batalha."
            )

        st.metric("Nível alcançado", st.session_state.nivel)
        st.metric("Inimigos derrotados", st.session_state.vitorias)

        if st.button("🔄 Jogar novamente", type="primary"):
            reiniciar()

        st.stop()

    heroi, batalha = st.columns([1, 2])

    with heroi:
        classe_info = CLASSES[st.session_state.classe]

        percentagem_vida = (
            st.session_state.vida /
            st.session_state.vida_maxima
        )

        st.markdown(
            f"""
            <div class="card">
                <div class="hero-name">
                    {classe_info["emoji"]} {st.session_state.nome}
                </div>
                <p>{st.session_state.classe} ·
                Nível {st.session_state.nivel}</p>
                <p>❤️ {st.session_state.vida} /
                {st.session_state.vida_maxima}</p>
                <p>⚔️ Ataque: {st.session_state.ataque}</p>
                <p>🛡️ Defesa: {st.session_state.defesa}</p>
                <p>💰 Ouro: {st.session_state.ouro}</p>
                <p>🧪 Poções: {st.session_state.pocoes}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.progress(
            percentagem_vida,
            text="Vida"
        )

        st.progress(
            min(
                1.0,
                st.session_state.xp /
                st.session_state.xp_necessario
            ),
            text=(
                f"XP: {st.session_state.xp} / "
                f"{st.session_state.xp_necessario}"
            )
        )

        st.markdown("### 🏪 Loja e estalagem")

        if st.button("🧪 Comprar poção · 15 moedas"):
            comprar_pocao()
            st.rerun()

        custo_arma = 55 + (st.session_state.ataque * 2)

        if st.button(f"🔨 Melhorar arma · {custo_arma} moedas"):
            melhorar_arma()
            st.rerun()

        if st.button("🏕️ Descansar · 18 moedas"):
            descansar()
            st.rerun()

        if st.button("🚪 Reiniciar jogo"):
            reiniciar()

    with batalha:
        if st.session_state.inimigo is None:
            if st.session_state.vitorias >= 5:
                st.warning(
                    "🐉 O Dragão de Eldoria espera-te no castelo!"
                )
                texto_botao = "🏰 Entrar no castelo"
            else:
                faltam = 5 - st.session_state.vitorias
                st.info(
                    f"🗺️ Explora Eldoria. Faltam {faltam} vitórias "
                    "para desbloquear o boss."
                )
                texto_botao = "🌲 Procurar inimigo"

            if st.button(texto_botao, type="primary"):
                criar_inimigo()
                st.rerun()

        else:
            inimigo = st.session_state.inimigo

            st.markdown(
                f"""
                <div class="card">
                    <div class="enemy-name">
                        {inimigo["emoji"]} {inimigo["nome"]}
                    </div>
                    <p>❤️ Vida: {inimigo["vida"]} /
                    {inimigo["vida_maxima"]}</p>
                    <p>⚔️ Ataque estimado: {inimigo["ataque"]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(
                inimigo["vida"] / inimigo["vida_maxima"],
                text="Vida do inimigo"
            )

            linha1, linha2 = st.columns(2)

            with linha1:
                if st.button("⚔️ Atacar", type="primary"):
                    atacar()
                    st.rerun()

                if st.button(
                    f"🔥 {classe_info['especial']}",
                    disabled=not st.session_state.especial_disponivel
                ):
                    ataque_especial()
                    st.rerun()

            with linha2:
                if st.button("🛡️ Defender"):
                    defender()
                    st.rerun()

                if st.button(
                    f"🧪 Usar poção ({st.session_state.pocoes})",
                    disabled=st.session_state.pocoes == 0
                ):
                    usar_pocao()
                    st.rerun()

        st.markdown("### 📜 Registo da aventura")

        registo_html = "<br>".join(
            st.session_state.registo
        )

        st.markdown(
            f'<div class="log-box">{registo_html}</div>',
            unsafe_allow_html=True
        )
