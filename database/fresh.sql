
-- Drop stuff first -----------------------------------------------------------

DROP TABLE games;
DROP TABLE developers;
DROP TABLE customers;

-- Types
DROP TYPE purchased_games_table;
DROP TYPE purchased_game_t;
DROP TYPE asin_t;


-- Now create stuff -----------------------------------------------------------

-- Types
CREATE OR REPLACE TYPE asin_t AS OBJECT (
    asin CHAR(10)
)
/

CREATE OR REPLACE TYPE purchased_game_t AS OBJECT (
    asin asin_t,
    quantity INTEGER,
    total DECIMAL(6, 2)
)
/

CREATE OR REPLACE TYPE purchased_games_table AS TABLE OF purchased_game_t
/

-- Tables
CREATE TABLE games (
    asin asin_t,
    title VARCHAR(64),
    price DECIMAL(6, 2)
)
/

CREATE TABLE developers (
    id INTEGER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    name VARCHAR(64) UNIQUE
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
