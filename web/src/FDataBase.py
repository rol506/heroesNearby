import psycopg
import psycopg.rows
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.environ.get("DB_NAME", "pgdb")
DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")

def create_db():
    with psycopg.connect(f"dbname={DB_NAME} user={DB_USER}") as conn:
        with conn.cursor() as cur:
            conn.commit()

class FDataBase:
    def __init__(self):
        self.__db = psycopg.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, row_factory=psycopg.rows.dict_row)
        self.__cur = self.__db.cursor()

    def __del__(self):
        self.__cur.close()
        self.__db.close()
