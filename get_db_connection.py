import psycopg2
def get_db_connection():
    conn = psycopg2.connect(host='YOUR_HOST',
                            database='YOUR_DATABASE',
                            user='YOUR_USER',
                            password='YOUR_PASSWORD')
    return conn