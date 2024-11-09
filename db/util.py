import os
import psycopg2
from typing import Dict, Literal
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


def get_db_engine():
    url = URL.create(
        drivername="postgresql+psycopg2",
        host="localhost",
        database="prempred_db",
        username=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD')
    )

    return create_engine(url)

def get_db_connection(use_sqlalchemy=True):
    if use_sqlalchemy:
        engine = get_db_engine()
        return engine.connect()

    conn = psycopg2.connect(host='localhost',
                            database='prempred_db',
                            user=os.getenv('DB_USERNAME'),
                            password=os.getenv('DB_PASSWORD'))


    return conn

def db_insert(table, values):
    if not isinstance(table, str) or len(table) < 1:
        return

    if not isinstance(values, dict) or len(values.keys()) < 1:
        return

    conn = get_db_connection()
    cur = conn.cursor()

    columns = ", ".join(list(values.keys()))
    inserts = ", ".join(['%s'] * len(values.keys()))
    query = cur.mogrify(f'INSERT INTO {table} ({columns}) VALUES ({inserts})', tuple(values.values()))

    cur.execute(query)

    conn.commit()
    cur.close()
    conn.close()


def db_get(table, columns, where: Dict = None, where_raw: str = None):
    if where is None:
        where = {}

    conn = get_db_connection()
    cur = conn.cursor()

    db_columns = ','.join(columns)
    query = f'SELECT {db_columns} FROM {table}'

    if where_raw is not None:
        query += f' WHERE {where_raw}'
    elif where is not {}:
        where_clause = ' AND '.join(map(lambda column: str(column) + ' = ' + f'\'{where[column]}\'', where.keys()))
        query += f' WHERE {where_clause}'

    query += ' LIMIT 1;'

    cur.execute(query)
    result = cur.fetchone()

    cur.close()
    conn.close()

    return result


def db_all(table, columns, where: Dict = None, where_raw: str = None, order: Literal['asc', 'desc']='asc', order_by='id'):
    if where is None:
        where = {}

    conn = get_db_connection()
    cur = conn.cursor()

    db_columns = ','.join(columns)
    query = f'SELECT {db_columns} FROM {table}'

    if where_raw is not None:
        query += f' WHERE {where_raw}'
    elif where is not {}:
        where_clause = ' OR '.join(map(lambda column: str(column) + ' = ' + f'\'{where[column]}\'', where.keys()))
        query += f' WHERE {where_clause}'

    query += f' ORDER BY {order_by} {order.upper()}'

    cur.execute(query)
    result = cur.fetchall()

    cur.close()
    conn.close()

    return result