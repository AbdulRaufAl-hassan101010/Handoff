-- Creating handoff_db database
-- Privileges for new user (handoff_db)
CREATE DATABASE IF NOT EXISTS handoff_db;
CREATE USER IF NOT EXISTS 'handoff'@'localhost';
SET PASSWORD FOR 'handoff'@'localhost' = 'password';
USE handoff_db;
GRANT ALL PRIVILEGES ON handoff_db.* TO 'handoff'@'localhost';
GRANT SELECT ON performance_schema.* TO 'handoff'@'localhost';
FLUSH PRIVILEGES;
