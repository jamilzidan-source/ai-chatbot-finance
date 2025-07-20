# ui_components.py
import streamlit as st
from llm_tools import ask_openai   # ask_openai(question: str, df: pd.DataFrame)

def chatbot_ui(df):
    # ---------- CSS untuk tombol peluncur (floating button)
    st.markdown(
        """
        <style>
        .chat-launch {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 9999;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ---------- State untuk men-toggle panel chat
    if "show_chat" not in st.session_state:
        st.session_state.show_chat = False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []   # [(role, text), ...]

    # ---------- Tombol floating
    if st.button("💬 Launch Chatbot", key="launcher", help="Ask a question about financial performance"):
        st.session_state.show_chat = not st.session_state.show_chat

    # ---------- Panel Chat
    if st.session_state.show_chat:
        st.subheader("🧠 AI Chatbot – Financial Performance Assistant")

        # Tampilkan riwayat percakapan (jika ada)
        for role, text in st.session_state.chat_history:
            if role == "user":
                st.markdown(f"**👤 You:** {text}")
            else:
                st.markdown(f"**🤖 Bot:** {text}")

        # Input pertanyaan
        user_question = st.text_input("Ask a question:", key="user_input")
        if user_question:
            # --- simpan pertanyaan user
            st.session_state.chat_history.append(("user", user_question))

            # --- panggil agent → df langsung
            response = ask_openai(user_question, df)

            # --- tampilkan & simpan jawaban
            st.session_state.chat_history.append(("bot", response))
            st.markdown("**💡 Answer:**")
            st.info(response)

            # Kosongkan kotak input setelah submit
            st.rerun()