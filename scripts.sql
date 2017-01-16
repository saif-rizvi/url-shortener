# Author: Saif Rizvi
# SQL commands and procedures used to set up and interact with urlstorage database

CREATE DATABASE IF NOT EXISTS urlstorage;
USE urlstorage

-- Table for storing urls
-- urlID is base10 id, shortURL is base62 version of urlID
CREATE TABLE IF NOT EXISTS urls (
	urlID INT AUTO_INCREMENT PRIMARY KEY,
	shortURL VARCHAR(6) UNIQUE,
	longURL VARCHAR(2083) NOT NULL UNIQUE
);

-- Returns record with a matching longURL
DELIMITER //
DROP PROCEDURE IF EXISTS GetRecordFromLongURL //
CREATE PROCEDURE GetRecordFromLongURL(inputURL VARCHAR(2083))
	SELECT shortURL, longURL FROM urls WHERE longURL=inputURL;
	//

-- Returns record with a matching shortURL
DROP PROCEDURE IF EXISTS GetRecordFromShortURL //  
CREATE PROCEDURE GetRecordFromShortURL(inputURL VARCHAR(6))
	SELECT shortURL, longURL FROM urls WHERE shortURL=inputURL;
	//

-- Converts base-10 number into base-62 string using repeated division method
DROP FUNCTION IF EXISTS base10ToBase62 // 
CREATE FUNCTION base10ToBase62(num INT(11)) RETURNS VARCHAR(6) DETERMINISTIC 
BEGIN
	DECLARE output VARCHAR(6) DEFAULT "";
	DECLARE base62 CHAR(62) DEFAULT "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
	DECLARE remainder INT DEFAULT 0;
	
	IF num = 0 THEN SET output = "0";
	END IF;
	
	WHILE num > 0 DO
    SET remainder = num MOD 62;
    SET num = num DIV 62;
    SET output = CONCAT(SUBSTR(base62, remainder+1, 1), output);
    END WHILE;
	RETURN (output);
END // 

-- Creates new row for given inputURL then sets its shortURL to a base62 repr. of its urlID
-- Only call this if you already know the inputURL isn't already in DB, or handle the error
DROP PROCEDURE IF EXISTS AddNewURL;
CREATE PROCEDURE AddNewURL(inputURL VARCHAR(2083))
	BEGIN
	START TRANSACTION;
	INSERT INTO urls (longURL) VALUES (inputURL);
	UPDATE urls
		SET shortURL = base10ToBase62(urlID)
		WHERE longURL = inputURL;
	COMMIT;
	END //
DELIMITER ;