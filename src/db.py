import psycopg
import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(env_path)

db_name = os.getenv("POSTGRES_DB")
user_name = os.getenv("POSTGRES_USER")
pass_name = os.getenv("POSTGRES_PASSWORD")
host = "127.0.0.1"
port = 5433

def get_connection():
    return psycopg.connect(dbname=db_name,
                           user=user_name,
                           password=pass_name,
                           host=host, port=port
    )