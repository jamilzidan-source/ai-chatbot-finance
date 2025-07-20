import os
print("Current dir:", os.getcwd())
print("Files:", os.listdir())

from bq_query import get_bigquery_data
from ui_components import chatbot_ui

def main():
    import streamlit as st
    st.set_page_config(page_title="Finance AI Chatbot", layout="wide")

    try:
        df = get_bigquery_data()
        chatbot_ui(df)
    except Exception as e:
        st.error(f"❌ Failed to load data or launch chatbot: {e}")

if __name__ == "__main__":
    main()
