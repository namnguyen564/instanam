DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS users_post;


CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    name TEXT,
    username TEXT,
    password_hash TEXT
    );

CREATE TABLE users_post(
    image_id SERIAL PRIMARY KEY,
    name TEXT,
    img_url TEXT,
    description TEXT
    );

    


