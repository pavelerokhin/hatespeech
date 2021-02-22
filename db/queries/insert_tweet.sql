INSERT INTO tweets (
        id,
        user_id,
        created_at,
        screen_name,
        is_retweet,
        is_quoted,
        tweet_text,
        quoted_text
    )
VALUES
    ((SELECT IFNULL(MAX(id),0)+1 FROM tweets),
    {},
    {},
    '{}',
    {},
    {},
    '{}',
    '{}')