-- ===============================
-- BACKUP & RESTORE COMMANDS
-- ===============================

-- ===============================
-- PostgreSQL
-- ===============================

-- Backup database
-- Run in CMD:
-- pg_dump -U postgres library_db > library_backup.sql

-- Restore database
-- psql -U postgres -d library_db -f library_backup.sql


-- ===============================
-- MySQL
-- ===============================

-- Backup database
-- Run in CMD:
-- mysqldump -u root -p library_db > library_backup.sql

-- Restore database
-- mysql -u root -p library_db < library_backup.sql