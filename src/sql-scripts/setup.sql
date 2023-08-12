CREATE SCHEMA menu_planner;

CREATE TABLE menu_planner.user (
    id SERIAL PRIMARY KEY,
    name varchar(50),
    sirname varchar(50)
);

CREATE TABLE menu_planner.menu_template (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by INTEGER REFERENCES menu_planner.user (id),
    name VARCHAR(50),
    template JSON
);

CREATE TABLE menu_planner.menu (
    id SERIAL PRIMARY KEY,
    created_at TIMESTAMP DEFAULT NOW(),
    created_by INTEGER REFERENCES menu_planner.user (id),
    reference_date DATE,
    category VARCHAR(50)
);

CREATE TABLE menu_planner.dishes (
    id SERIAL PRIMARY KEY,
    category VARCHAR(50),
    name VARCHAR(200),
    cost INTEGER,
    observation VARCHAR(200),
    UNIQUE (category, name)
);

CREATE TABLE menu_planner.menu_composition (
    id SERIAL PRIMARY KEY,
    menu_id INTEGER REFERENCES menu_planner.menu (id),
    dish_id INTEGER REFERENCES menu_planner.dishes (id)
);