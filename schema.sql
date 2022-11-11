DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS users_post;
DROP TABLE IF EXISTS user_followers;
DROP TABLE IF EXISTS users_following;

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    name TEXT,
    username TEXT,
    password_hash TEXT,
    follower_count INTEGER,
    following_count INTEGER
    );

CREATE TABLE users_post(
    image_id TEXT,
    name TEXT,
    img_url TEXT,
    description TEXT,
    like_counter INTEGER,
    comments_name TEXT,
    comments_username TEXT,
    comments TEXT
    );

CREATE TABLE users_followers (
    user_followers_id SERIAL PRIMARY KEY,
    name_followers_name TEXT,
    followers_username TEXT
    );


CREATE TABLE users_following (
    users_following_id SERIAL PRIMARY KEY,
    name_following_name TEXT,
    following_username TEXT
    );



    


