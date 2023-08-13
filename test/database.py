from . import database

def Database():
    db = database.Database()
    db.send("INSERT INTO menu_planner.user( name ) VALUES ('Mateus'),('Maria')")
    db.send("SELECT * FROM menu_planner.user")
    database.logger.info(db.get())
    db.disconnect()

def populate_db():
    db = database.Database()
    with open('src/sql-scripts/demo_data.sql', 'r') as sql:
        command = sql.read()
        db.send(command)
