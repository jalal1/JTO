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

COMMIT;

