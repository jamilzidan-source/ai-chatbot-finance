import openai
import os
import pandas as pd
from dotenv import load_dotenv
import psycopg2-binary
from datetime import datetime
from calculator_agent import calculate

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# PostgreSQL logging
SUPABASE_DB = os.getenv("SUPABASE_DB")
SUPABASE_USER = os.getenv("SUPABASE_USER")
SUPABASE_PASS = os.getenv("SUPABASE_PASS")
SUPABASE_HOST = os.getenv("SUPABASE_HOST")
SUPABASE_PORT = os.getenv("SUPABASE_PORT")

def log_to_supabase(question, data_text, response):
    try:
        conn = psycopg2-binary.connect(
            dbname=SUPABASE_DB,
            user=SUPABASE_USER,
            password=SUPABASE_PASS,
            host=SUPABASE_HOST,
            port=SUPABASE_PORT
        )
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chatbot_logs (
                id SERIAL PRIMARY KEY,
                question TEXT,
                data_input TEXT,
                response TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """)

        cursor.execute("""
            INSERT INTO chatbot_logs (question, data_input, response, created_at)
            VALUES (%s, %s, %s, %s)
        """, (question, data_text[:1000], response[:1000], datetime.now()))

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Failed to log conversation: {e}")

def ask_openai(question: str, df: pd.DataFrame) -> str:
    q = question.lower()

    # Step 1: Try calculation if keyword detected
    if any(kw in q for kw in ["total", "sum", "net", "top", "growth", "trend", "average"]):
        result = calculate(q, df)
        log_to_supabase(question, df.to_string(index=False), result)
        return result

    # Step 2: If not calculation → ask LLM
    try:
        prompt = f"""
You are a professional financial analyst. Below is a table of financial data:

{df.to_string(index=False)}

Now answer this question based on the data above:

{question}
"""
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1024
        )
        result = response['choices'][0]['message']['content']
        log_to_supabase(question, df.to_string(index=False), result)
        return result
    except Exception as e:
        return f"❌ Error: {str(e)}"
