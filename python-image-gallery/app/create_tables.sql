DROP TABLE IF EXISTS users;
CREATE TABLE users (username varchar(100) NOT NULL PRIMARY KEY, password varchar(100), full_name varchar(200));
INSERT INTO users values ('jim1', '123', 'jim bob');
INSERT INTO users values ('jim', 'jim', 'jim jim');
INSERT INTO users values ('steve', '456', 'steve harvey');
INSERT INTO users values ('dongji', 'cpsc4973', 'dongji');
INSERT INTO users values ('angelo', '123', 'angelo adkins');
