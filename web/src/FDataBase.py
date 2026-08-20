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
    load_dotenv()
    DB_NAME = os.environ.get("DB_NAME", "pgdb")
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_USER = os.environ.get("POSTGRES_USER")
    DB_PASS = os.environ.get("POSTGRES_PASSWORD")
    with psycopg.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT) as conn:
        with conn.cursor() as cur:
            cur.execute("""
create table if not exists streets (
    id uuid primary key default uuidv7(),
    lat numeric not null,
    lon numeric not null,
    name text not null,
    description text,
    special_fact text
);

create table if not exists images (
    id uuid primary key default uuidv7(),
    streetid uuid not null references streets(id),
    path text not null
);
            """)
            conn.commit()

class FDataBase:
    def __init__(self):
        self.__db = psycopg.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, row_factory=psycopg.rows.dict_row)
        self.__cur = self.__db.cursor()

    def __del__(self):
        self.__cur.close()
        self.__db.close()

    def findStreet(self, name: str) -> list:
        sql = """select lat, lon, name, description, special_fact from streets where name like %s"""
        try:
            self.__cur.execute(sql, (f"%{name}%",))
            res = self.__cur.fetchall()
            print(res)
            if res: return res
        except Exception as e:
            print("findStreet failed: " + str(e))
        return []
