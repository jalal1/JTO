BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 1d475c2c1de1

ALTER TABLE users ADD COLUMN birthday TIMESTAMP WITHOUT TIME ZONE;

ALTER TABLE users ADD COLUMN city VARCHAR(20);

ALTER TABLE users ADD COLUMN interest VARCHAR(30);

ALTER TABLE users ADD COLUMN languages VARCHAR(10);

ALTER TABLE users ADD COLUMN weight VARCHAR(5);

CREATE INDEX ix_users_birthday ON users (birthday);

CREATE INDEX ix_users_city ON users (city);

CREATE INDEX ix_users_interest ON users (interest);

CREATE INDEX ix_users_languages ON users (languages);

CREATE INDEX ix_users_weight ON users (weight);

INSERT INTO alembic_version (version_num) VALUES ('1d475c2c1de1');

COMMIT;

