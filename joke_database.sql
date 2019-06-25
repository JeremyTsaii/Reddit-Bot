CREATE TABLE joke_submissions(
	numID int NOT NULL AUTO_INCREMENT,
    userID varchar(255), 
    joke_text LONGTEXT,
    dateOfEntry varchar(255),
    PRIMARY KEY (numID)
    );

CREATE USER 'user'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON jokes.submissions TO 'user'@'localhost';
ALTER USER 'user'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';

SELECT * FROM joke_submissions;

