import os

import streamlit as st
from datapizza.clients.openai import OpenAIClient
from dotenv import load_dotenv

from agents.gamemaster_agent import create_gamemaster_agent


load_dotenv()

st.set_page_config(
    page_title="GameMaster AI",
    page_icon="🎲",
)

st.title("🎲 GameMaster AI")
st.caption(
    "Trova un gioco da tavolo o chiedi informazioni sui regolamenti caricati."
)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error(
        "OPENAI_API_KEY non configurata. Aggiungila al file .env "
        "o alle variabili d'ambiente per usare l'assistente."
    )
    st.stop()

if "agent" not in st.session_state:
    client = OpenAIClient(
        api_key=api_key,
        model="gpt-4o-mini",
    )
    st.session_state.agent = create_gamemaster_agent(client)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "Ciao! Posso aiutarti a scegliere un gioco o a consultare "
                "un regolamento. Per esempio: «Siamo in 4 e vogliamo "
                "un cooperativo»."
            ),
        }
    ]

with st.sidebar:
    st.header("Cosa posso fare")
    st.markdown(
        "- **Consigliare un gioco** in base a giocatori e preferenze.\n"
        "- **Rispondere sulle regole** usando i regolamenti caricati."
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Scrivi una domanda..."):
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("GameMaster sta pensando..."):
            response = st.session_state.agent.run(question)

        if response is None:
            st.error("L'assistente non ha restituito una risposta.")
        else:
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append(
                {"role": "assistant", "content": answer}
            )
