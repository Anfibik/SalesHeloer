CREATE TABLE IF NOT EXISTS lead (
id integer PRIMARY KEY AUTOINCREMENT,
company text NOT NULL,
name text NOT NULL,
job_title text NOT NULL,
phone text NOT NULL,
mail text NOT NULL,
project text NOT NULL,
price float NOT NULL,
profit float NOT NULL,
status text NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
email text NOT NULL,
psw text NOT NULL
);
