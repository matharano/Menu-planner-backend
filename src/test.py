from . import database

def Database():
    db = database.Database()
    db.send("INSERT INTO menu_planner.user( name ) VALUES ('Mateus'),('Maria')")
    db.send("SELECT * FROM menu_planner.user")
    database.logger.info(db.get())
    db.disconnect()

if __name__ == '__main__':
    Database()