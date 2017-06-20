CREATE TABLE users (id integer primary key autoincrement, username TEXT, email TEXT, password TEXT, image_url TEXT);

CREATE TABLE question (id integer primary key autoincrement, question TEXT, first_choice TEXT, second_choice TEXT, choice1 INTEGER, choice2 INTEGER, user_id INTEGER);

CREATE TABLE rate (id integer primary key autoincrement, image_url TEXT, user_id INTEGER);

CREATE TABLE pemilih_rate (id integer primary key autoincrement, rate_id INTEGER, choice CHAR, user_id INTEGER);

INSERT INTO users (username, email, password) VALUES ("q","q","q");
INSERT INTO question (question,first_choice,second_choice,choice1,choice2,user_id) values('Jika', 'YES', 'NO',0,0,1);
INSERT INTO question (question,first_choice,second_choice,choice1,choice2,user_id) values('Pilih mami atau papi?', 'Mami', 'Papi',0,0,1);

INSERT INTO rate (image_url, user_id) values('http://cdn.akamai.steamstatic.com/steam/apps/292030/header.jpg?t=1479919850', 1);
INSERT INTO rate (image_url, user_id) values('https://uniknown.files.wordpress.com/2011/12/121211_0733_perkembanga1.jpg?w=110&h=146', 1);

