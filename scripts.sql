# SQL commands and procedures 

USE urlstorage;

-- DROP if exists or something? 
CREATE TABLE urls (
	urlID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	shortURL VARCHAR(6) UNIQUE,
	longURL VARCHAR(2083) UNIQUE
)

-- Returns corresponding longURL of given inputURL
DELIMITER //
CREATE PROCEDURE GetLongURL(inputURL VARCHAR(6))
	BEGIN
	SELECT (longURL) FROM urls WHERE shortURL=inputURL;
	END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE GetMaxID()
	BEGIN
	SELECT `AUTO_INCREMENT`
		FROM  INFORMATION_SCHEMA.TABLES
		WHERE TABLE_SCHEMA = 'urlstorage'
		AND   TABLE_NAME   = 'urls';
	END //
DELIMITER ;

-- TODO: Write Base-10 to Base-62 Converter

DELIMITER //
CREATE PROCEDURE AddNewURL(inputURL VARCHAR(2083))
	BEGIN

	-- Check if URL already in DB. Might be able to avoid this using INSERT IGNORE
	SELECT * FROM urls WHERE longURL=inputURL;

	-- This might not work if two requests are sent at the same time
	-- nextID = GetMaxID()
	-- nextShortURL = Base10ToBase62(nextID)
	-- INSERT INTO urls (shortURL, urlID, longURL) 
	-- VALUES (nextShortURL, nextID, inputURL)
	
	-- Might be a way to automatically call a procedure to fill shortURL 
	-- column after row is added, calculated based on urlID, which is auto-incremented

	END //
DELIMITER ;