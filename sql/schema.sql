CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

CREATE TABLE developers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE apps (
    id SERIAL PRIMARY KEY,
    app_id VARCHAR(255) UNIQUE NOT NULL,
    app_name VARCHAR(255) NOT NULL,
    category_id INT REFERENCES categories(id) ON DELETE SET NULL,
    developer_id INT REFERENCES developers(id) ON DELETE SET NULL,
    rating FLOAT,
    rating_count BIGINT,
    installs BIGINT,
    min_installs BIGINT,
    max_installs BIGINT,
    free BOOLEAN,
    price FLOAT,
    currency VARCHAR(50),
    size FLOAT,
    min_android VARCHAR(50),
    released DATE,
    last_updated DATE,
    content_rating VARCHAR(50),
    ad_supported BOOLEAN,
    in_app_purchases BOOLEAN,
    editors_choice BOOLEAN,
    scraped_time TIMESTAMP
);
