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

-- Running upgrade 60751cde36c9 -> 22dbbad1373d

ALTER TABLE relationships ADD CONSTRAINT "unique_user1_Id_user2_Id" UNIQUE ("user1_Id", "user2_Id");

UPDATE alembic_version SET version_num='22dbbad1373d' WHERE alembic_version.version_num = '60751cde36c9';

-- Running upgrade 22dbbad1373d -> 670ea5c6d6b0

ALTER TABLE posts ADD COLUMN likes INTEGER;

UPDATE alembic_version SET version_num='670ea5c6d6b0' WHERE alembic_version.version_num = '22dbbad1373d';

-- Running upgrade 670ea5c6d6b0 -> c64e2c7405ae

ALTER TABLE posts ALTER COLUMN likes SET NOT NULL;

UPDATE alembic_version SET version_num='c64e2c7405ae' WHERE alembic_version.version_num = '670ea5c6d6b0';

-- Running upgrade c64e2c7405ae -> cc760ec42088

ALTER TABLE posts ADD COLUMN image_path VARCHAR(200);

ALTER TABLE posts ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE posts ALTER COLUMN user_id SET NOT NULL;

ALTER TABLE posts DROP COLUMN image_id;

ALTER TABLE users ADD COLUMN image_path VARCHAR(200);

UPDATE alembic_version SET version_num='cc760ec42088' WHERE alembic_version.version_num = 'c64e2c7405ae';

-- Running upgrade cc760ec42088 -> 90c679497f21



ALTER TABLE posts ALTER COLUMN created_at SET NOT NULL;

ALTER TABLE posts ALTER COLUMN user_id SET NOT NULL;



UPDATE alembic_version SET version_num='90c679497f21' WHERE alembic_version.version_num = 'cc760ec42088';

COMMIT;

