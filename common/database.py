import sqlite3
import pandas as pd


def get_db_connection():
    # SQLite 데이터베이스 연결 함수
    conn = sqlite3.connect('sample.db')
    conn.row_factory = sqlite3.Row
    return conn


def query_sqlite(query):
    # SQLite 쿼리 실행 함수
    conn = get_db_connection()
    result = conn.execute(query).fetchall()
    conn.close()
    return pd.DataFrame(result)
