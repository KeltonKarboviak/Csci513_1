
-- Fill games table
insert into games (asin, title, price) VALUES (asin_t('1234567890'), 'game1', 15.00);
insert into games (asin, title, price) VALUES (asin_t('0987654321'), 'game2', 18.25);
insert into games (asin, title, price) VALUES (asin_t('B00QWERTYU'), 'game3', 12.66);


-- Fill developers table
insert into developers (name) VALUES ('jim');
insert into developers (name) VALUES ('bob');
insert into developers (name) VALUES ('joe');


-- Fill customers table
insert into customers (username, account) VALUES ('mary',
    purchased_games_table(
        purchased_game_t(asin_t('1234567890'), 2, 30.00),
        purchased_game_t(asin_t('0987654321'), 1, 18.25)
    )
);
insert into customers (username, account) VALUES ('carly',
    purchased_games_table(
        purchased_game_t(asin_t('1234567890'), 1, 15.00)
    )
);
insert into customers (username, account) VALUES ('susie',
    purchased_games_table(
        purchased_game_t(asin_t('1234567890'), 2, 30.00),
        purchased_game_t(asin_t('0987654321'), 1, 18.25),
        purchased_game_t(asin_t('B00QWERTYU'), 3, 37.98)
    )
);
insert into customers (username) VALUES ('sally');

