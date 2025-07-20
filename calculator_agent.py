import pandas as pd

def calculate(question: str, df: pd.DataFrame) -> str:
    q = question.lower()
    try:
        if "total revenue" in q:
            value = df[df['category'] == 'REVENUE']['balance'].sum()
            return f"💰 Total revenue: {value:,.2f}"
        
        elif "total expense" in q:
            value = df[df['category'] == 'EXPENSE']['balance'].sum()
            return f"💸 Total expense: {value:,.2f}"
        
        elif "net income" in q or ("profit" in q and "net" in q):
            rev = df[df['category'] == 'REVENUE']['balance'].sum()
            exp = df[df['category'] == 'EXPENSE']['balance'].sum()
            net = rev - exp
            return f"📊 Net income: {net:,.2f}"
        
        elif "top" in q and "revenue" in q:
            top_rev = df[df['category'] == 'REVENUE'].groupby('date')['balance'].sum().nlargest(3)
            return f"🏆 Top 3 revenue periods:\n{top_rev.to_string()}"
        
        else:
            return "🤔 I detected a calculation question but don't have a rule to handle it yet."

    except Exception as e:
        return f"❌ Calculation Error: {str(e)}"