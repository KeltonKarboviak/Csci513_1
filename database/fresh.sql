
-- Drop stuff first -----------------------------------------------------------

DROP TABLE games_developers;
DROP TABLE games;
DROP TABLE games2;
DROP TABLE developers;
DROP TABLE customers;

-- Types
DROP TYPE purchased_games_table;
DROP TYPE purchased_game_t;

DROP TYPE developers_table;
DROP TYPE dev_t;


-- Now create stuff -----------------------------------------------------------

-- Types

CREATE OR REPLACE TYPE purchased_game_t AS OBJECT (
    asin CHAR(10),
    quantity INTEGER,
    total DECIMAL(6, 2)
)
/

CREATE OR REPLACE TYPE purchased_games_table AS TABLE OF purchased_game_t
/

CREATE OR REPLACE TYPE dev_t AS OBJECT (
    id INTEGER,
    name VARCHAR(64)
)
/

CREATE OR REPLACE TYPE developers_table AS TABLE OF dev_t
/

-- Tables
CREATE TABLE games (
    asin CHAR(10) PRIMARY KEY,
    title VARCHAR(64),
    price DECIMAL(6, 2)
)
/

CREATE TABLE games2 (
    asin CHAR(10) PRIMARY KEY,
    title VARCHAR(64),
    price DECIMAL(6, 2),
    developers developers_table
) NESTED TABLE developers STORE AS nested_developers RETURN AS LOCATOR
/

CREATE TABLE developers (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR(64) UNIQUE
)
/

CREATE TABLE games_developers (
    asin CHAR(10),
    developer_id INTEGER,
    PRIMARY KEY(asin, developer_id),
    FOREIGN KEY (asin) REFERENCES games(asin),
    FOREIGN KEY (developer_id) REFERENCES developers(id)
)
/

CREATE TABLE customers (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    username VARCHAR(64) UNIQUE,
    -- nested table of customer_purchases
    account purchased_games_table
) NESTED TABLE account STORE AS nested_account RETURN AS LOCATOR
/

commit;
