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

-- Running upgrade a9472850ddac -> 2c0176db11a7

CREATE TABLE relationships (
    id SERIAL NOT NULL, 
    "user1_Id" INTEGER, 
    "user2_Id" INTEGER, 
    created_at TIMESTAMP WITHOUT TIME ZONE, 
    modified_at TIMESTAMP WITHOUT TIME ZONE, 
    PRIMARY KEY (id), 
    FOREIGN KEY("user1_Id") REFERENCES users (id), 
    FOREIGN KEY("user2_Id") REFERENCES users (id)
);

CREATE INDEX ix_relationships_created_at ON relationships (created_at);

ALTER TABLE posts ADD COLUMN user_id INTEGER;

CREATE INDEX ix_posts_created_at ON posts (created_at);

ALTER TABLE posts ADD FOREIGN KEY(user_id) REFERENCES users (id);

CREATE UNIQUE INDEX ix_users_email ON users (email);

CREATE INDEX ix_users_name ON users (name);

ALTER TABLE users DROP CONSTRAINT users_email_key;

UPDATE alembic_version SET version_num='2c0176db11a7' WHERE alembic_version.version_num = 'a9472850ddac';

-- Running upgrade 2c0176db11a7 -> 60751cde36c9

ALTER TABLE relationships ADD COLUMN action_by INTEGER;

ALTER TABLE relationships ADD COLUMN status INTEGER NOT NULL;

ALTER TABLE relationships ADD FOREIGN KEY(action_by) REFERENCES users (id);

UPDATE alembic_version SET version_num='60751cde36c9' WHERE alembic_version.version_num = '2c0176db11a7';

COMMIT;

