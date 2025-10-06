
-- https://tableplus.com/blog/2018/04/postgresql-how-to-create-read-only-user.html
-- https://tableplus.com/blog/2018/04/postgresql-how-to-grant-access-to-users.html

CREATE database taxi_db;
-- NOTE NEVER hardcode passwords in repo files in production, this is for local use only
CREATE USER usr WITH ENCRYPTED PASSWORD 'S0S1rongPsw';
GRANT CONNECT ON DATABASE taxi_db TO usr;

\connect taxi_db
GRANT USAGE ON SCHEMA public TO usr;
GRANT CREATE ON SCHEMA public TO usr;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO usr;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO usr;
