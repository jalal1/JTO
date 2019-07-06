BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> eafa0f64abd3

CREATE TABLE users (
    id SERIAL NOT NULL, 
    name VARCHAR(128) NOT NULL, 
    email VARCHAR(128) NOT NULL, 
    password VARCHAR(128), 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    modified_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id), 
    UNIQUE (email)
);

INSERT INTO alembic_version (version_num) VALUES ('eafa0f64abd3');

-- Running upgrade eafa0f64abd3 -> a9472850ddac

CREATE TABLE posts (
    id SERIAL NOT NULL, 
    text VARCHAR NOT NULL, 
    image_id INTEGER, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    modified_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id)
);

UPDATE alembic_version SET version_num='a9472850ddac' WHERE alembic_version.version_num = 'eafa0f64abd3';

COMMIT;

