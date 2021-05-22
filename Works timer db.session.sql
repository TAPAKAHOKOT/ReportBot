SELECT table_name FROM information_schema.tables
WHERE table_schema NOT IN ('information_schema','pg_catalog');

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