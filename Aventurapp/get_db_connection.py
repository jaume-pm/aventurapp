import psycopg2
import os

Host = os.getenv('POSTGRES_HOST')

def get_db_connection():
    conn = psycopg2.connect(host = Host,
                            port = '5432',
                            user='postgres',
                            password='Aventurapp')
    return conn