from src import test, database

if __name__ == '__main__':
    db = database.Database()
    db.drop_db()

    db = database.Database()
    db.setup()
    test.populate_db()