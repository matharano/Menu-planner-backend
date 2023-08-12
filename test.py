import os
print(os.environ.get('POSTGRES_IP'))
from src import test

if __name__ == '__main__':
    test.Database()