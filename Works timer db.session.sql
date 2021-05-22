-- SELECT table_name FROM information_schema.tables
-- WHERE table_schema NOT IN ('information_schema','pg_catalog');

-- select * from users_tag_history;

-- SELECT COUNT(*)
-- FROM users_tag_history
-- WHERE user_id=123;

-- DELETE FROM users_tag_history
-- WHERE user_id=123 AND call_time=(
--     SELECT call_time 
--     FROM users_tag_history
--     ORDER BY call_time DESC
--     LIMIT 1
-- )

-- delete from users_tags

-- CREATE TABLE tg_api_table 
-- (bot_name TEXT PRIMARY KEY NOT NULL,
-- api_key TEXT NOT NULL);


-- INSERT INTO tg_api_table VALUES 
-- ('clear_reports_sender_bot', '1454531950:AAGdb0c7fowkg7NkhS83gkPIGvbQhYHWVYY');

select * from tg_api_table;