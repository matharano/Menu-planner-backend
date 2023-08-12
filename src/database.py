import os
import psycopg2
import logging
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

USER = os.environ.get('POSTGRES_USER')
PASSWORD = os.environ.get('POSTGRES_PASSWORD')
IP = os.environ.get('POSTGRES_IP')
PORT = os.environ.get('POSTGRES_PORT')
DATABASE_NAME = 'menu_planner'

logger = logging.getLogger('backend')

class Database:
    def __init__(self, user:str=USER, password:str=PASSWORD, ip:str=IP, port:str=PORT, database_name:str=DATABASE_NAME, create_if_not_exists:bool=True) -> None:
        self.user = user
        self.password = password
        self.ip = ip
        self.port = port
        self.database_name = database_name
        if create_if_not_exists: self.create_db()
        self.connect()

    def create_db(self) -> None:
        """Checks if any database with the given name already exists. If not, creates the database"""
        connection = psycopg2.connect(user=self.user, password=self.password, host=self.ip, port=self.port)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        cursor.execute(F"SELECT 1 FROM pg_database WHERE datname = '{self.database_name}'")
        db_exists = cursor.fetchone() is not None
        if not db_exists: cursor.execute(f"CREATE DATABASE {self.database_name}")

        cursor.close()
        connection.close()
        
    def connect(self) -> None:
        self.connection = psycopg2.connect(user=self.user, password=self.password, host=self.ip, port=self.port, database=self.database_name)
        self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.connection.cursor()
    
    def disconnect(self) -> None:
        self.cursor.close()
        self.connection.close()
    
    def send(self, command:str) -> None:
        if command[-1] != ';': command += ';'
        try:
            self.cursor.execute(command)
        except Exception as e:
            logger.warning(e)
    
    def get(self) -> list[str]:
        return self.cursor.fetchall()
    
    def send_and_hear_back(self, command:str) -> list[str]:
        """Send a command and wait for an answer"""
        self.send(command)
        return self.get()

    def setup(self) -> None:
        """Create database and tables"""
        with open('src/sql-scripts/setup.sql', 'r') as sqlfile:
            commands = sqlfile.read()
            for command in commands.split(';'):
                if len(command.replace('\n', '').replace(' ', '')) == 0: continue
                self.send(command)

    def drop_db(self) -> None:
        self.disconnect()
        connection = psycopg2.connect(user=self.user, password=self.password, host=self.ip, port=self.port)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        cursor.execute(F"DROP DATABASE {DATABASE_NAME} WITH (FORCE);")
        cursor.close()
        connection.close()

if __name__ == '__main__':
    db = Database()
    # db.drop_db()
    db.setup()