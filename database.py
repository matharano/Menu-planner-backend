import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

USER = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')
IP = os.environ.get('POSTGRES_IP')
PORT = os.environ.get('POSTGRES_PORT')
DATABASE_NAME = 'menu_planner'

def setup() -> None:
    """Create database and tables"""
    create_db()
    connection = psycopg2.connect(user=USER, password=PASSWORD, host=IP, port=PORT, database=DATABASE_NAME)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()

    with open('setup.sql', 'r') as sqlfile:
        commands = sqlfile.read()
        for command in commands.split(';'):
            if len(command.replace('\n', '').replace(' ', '')) == 0: continue
            cursor.execute(command + ';')

    cursor.close()
    connection.close()

def create_db() -> None:
    connection = psycopg2.connect(user=USER, password=PASSWORD, host=IP, port=PORT)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()

    # Check if any database with the given name already exists. If not, creates the database
    cursor.execute(F"SELECT 1 FROM pg_database WHERE datname = '{DATABASE_NAME}'")
    db_exists = cursor.fetchone() is not None
    if not db_exists: cursor.execute(f"CREATE DATABASE {DATABASE_NAME}")

    cursor.close()
    connection.close()

def drop_db():
    connection = psycopg2.connect(user=USER, password=PASSWORD, host=IP, port=PORT)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute(F"DROP DATABASE {DATABASE_NAME}")
    cursor.close()
    connection.close()

def test():
    connection = psycopg2.connect(user=USER, password=PASSWORD, host=IP, port=PORT, database=DATABASE_NAME)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO menu_planner.user( name )
    VALUES
        ('Mateus'),
        ('Maria')
    ;""")
    cursor.execute("SELECT * FROM menu_planner.user;")
    print(cursor.fetchall())

    cursor.close()
    connection.close()

if __name__ == '__main__':
    drop_db()
    setup()
    test()