
-- Fill games2 table
insert into games2 (asin, title, price, developers) VALUES (
    '1234567890', 'game3', 15.00, developers_table(
        dev_t(1, 'Jimmy Bob Carlson'),
        dev_t(2, 'Billy Bob Thorton')
    )
);
insert into games2 (asin, title, price, developers) VALUES (
    '0987654321', 'game1', 18.25, developers_table(
        dev_t(3, 'Joseph Blackberry')
    )
);
insert into games2 (asin, title, price, developers) VALUES (
    'B00QWERTYU', 'game2', 12.66, developers_table(
        dev_t(3, 'Joseph Blackberry'),
        dev_t(4, 'Curly Joe Stevenson'),
        dev_t(5, 'Jim Steve Bobby')
    )
);


-- Fill developers table
insert into developers (name) VALUES ('Jimmy Bob Carlson');
insert into developers (name) VALUES ('Billy Bob Thorton');
insert into developers (name) VALUES ('Joeseph Blackberry');
insert into developers (name) VALUES ('Curly Joe Stevenson');
insert into developers (name) VALUES ('Jim Steve Bobby');


-- Fill customers table
insert into customers (username, account) VALUES ('mary',
    purchased_games_table(
        purchased_game_t('1234567890', 2, 30.00),
        purchased_game_t('0987654321', 1, 18.25)
    )
);
insert into customers (username, account) VALUES ('carly',
    purchased_games_table(
        purchased_game_t('1234567890', 1, 15.00)
    )
);
insert into customers (username, account) VALUES ('susie',
    purchased_games_table(
        purchased_game_t('1234567890', 2, 30.00),
        purchased_game_t('0987654321', 1, 18.25),
        purchased_game_t('B00QWERTYU', 3, 37.98)
    )
);
insert into customers (username, account) VALUES ('sally',
    purchased_games_table()
);

commit;
