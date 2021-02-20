CREATE TABLE IF NOT EXIST tweets (
    id integer PRIMARY KEY,
    user_id integer,
    created_at integer,
    screen_name text,
    is_retweet boolean,
    is_quoted boolean,
    tweet_text text,
    quoted_text text
)