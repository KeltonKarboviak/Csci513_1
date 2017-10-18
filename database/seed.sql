
-- Fill games table
insert into games (asin, title, price) VALUES ('1234567890', 'game3', 15.00);
insert into games (asin, title, price) VALUES ('0987654321', 'game1', 18.25);
insert into games (asin, title, price) VALUES ('B00QWERTYU', 'game2', 12.66);


-- Fill developers table
insert into developers (id, name) VALUES (1, 'Jimmy Bob Carlson');
insert into developers (id, name) VALUES (2, 'Billy Bob Thorton');
insert into developers (id, name) VALUES (3, 'Joeseph Blackberry');
insert into developers (id, name) VALUES (4, 'Curly Joe Stevenson');
insert into developers (id, name) VALUES (5, 'Jim Steve Bobby');


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
insert into customers (username) VALUES ('sally');

-- Fill games_developers table
insert into games_developers(asin, developer_id) VALUES ('1234567890', 1);
insert into games_developers(asin, developer_id) VALUES ('1234567890', 2);
insert into games_developers(asin, developer_id) VALUES ('0987654321', 3);
insert into games_developers(asin, developer_id) VALUES ('B00QWERTYU', 3);
insert into games_developers(asin, developer_id) VALUES ('B00QWERTYU', 4);
insert into games_developers(asin, developer_id) VALUES ('B00QWERTYU', 5);

commit;
