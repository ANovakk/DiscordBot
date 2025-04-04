DROP TABLE IF EXISTS voice_logs;
DROP TABLE IF EXISTS casino_games;
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS users;

-- users
CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    username TEXT,
    balance INTEGER DEFAULT 0,
    total_voice_time INTEGER DEFAULT 0,
    last_join_time TIMESTAMP
);

-- transactions
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    amount INTEGER,
    type TEXT,
    timestamp TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- casino_games
CREATE TABLE IF NOT EXISTS casino_games (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    game_type TEXT,
    bet INTEGER,
    result TEXT,
    profit INTEGER,
    timestamp TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- voice_logs
CREATE TABLE IF NOT EXISTS voice_logs (
    id SERIAL PRIMARY KEY,
    user_id TEXT,
    channel_id TEXT,
    join_time TIMESTAMP,
    leave_time TIMESTAMP,
    duration INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);
