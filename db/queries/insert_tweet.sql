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
<<<<<<< HEAD
    ({}, {}, {}, '{}', {}, {}, '{}', '{}')
=======
    ((SELECT IFNULL(MAX(id),0)+1 FROM tweets),
    {},
    {},
    '{}',
    {},
    {},
    '{}',
    '{}')
>>>>>>> main
