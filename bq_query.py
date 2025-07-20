from google.cloud import bigquery
import os
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def get_bigquery_data():
    # Load credentials and configs
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service_account.json"
    project_id = os.getenv("GCP_PROJECT_ID")
    table_name = os.getenv("BQ_TABLE")

    if not project_id or not table_name:
        raise ValueError("Missing GCP_PROJECT_ID or BQ_TABLE in .env file")

    client = bigquery.Client(project=project_id)

    query = f"""
        SELECT
            *
        FROM
            `{table_name}`
        WHERE
            date BETWEEN DATE('2025-01-01') AND CURRENT_DATE()
        ORDER BY date
    """

    df = client.query(query).to_dataframe()
    return df

if __name__ == "__main__":
    df = get_bigquery_data()
    print("✅ Sample result:")
    print(df.head())
    print(len(df))