CREATE TABLE IF NOT EXISTS tweets (
    id integer PRIMARY KEY,
    user_id integer,
    created_at integer,
    screen_name text,
    is_retweet tinyint,
    is_quoted tinyint,
    tweet_text text,
    quoted_text text
)