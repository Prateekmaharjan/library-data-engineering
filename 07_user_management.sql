-- ===============================
-- USER MANAGEMENT
-- ===============================

-- ===============================
-- PostgreSQL
-- ===============================

-- Create user (role with login)
CREATE ROLE librarian LOGIN PASSWORD 'librarian123';

-- Grant database access
GRANT CONNECT ON DATABASE library_db TO librarian;

-- Grant schema access
GRANT USAGE ON SCHEMA public TO librarian;

-- Grant table permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO librarian;


-- ===============================
-- MySQL
-- ===============================

-- Create user
CREATE USER 'librarian'@'localhost' IDENTIFIED BY 'librarian123';

-- Grant access to database
GRANT ALL PRIVILEGES ON library_db.* TO 'librarian'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;