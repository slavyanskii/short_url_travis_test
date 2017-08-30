CREATE TABLE IF NOT EXISTS url_web
(
    id SERIAL PRIMARY KEY NOT NULL,
    full_url VARCHAR (255) NOT NULL,
    short_url VARCHAR (255) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);