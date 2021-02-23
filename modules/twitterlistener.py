import tweepy
import utils
from modules.databaseaccess import insert_tweet


def stream_go(conf, keys, conn):
    """
    main function launching twitter filtered streaming
    input from config file, file with Twitter credentials
    output goes to the output/[csv_file]
    """
    # authorisation
    auth = tweepy.OAuthHandler(consumer_key=keys.get('customer_key'),
                               consumer_secret=keys.get('customer_secret'))
    auth.set_access_token(key=keys.get('access_key'), secret=keys.get('access_secret'))
    api = tweepy.API(auth_handler=auth)

    # stream
    stream_listener = StreamListener(conf, conn)
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener, tweet_mode='extended')

    # headers
    utils.write_csv_header(conf)

    # go!
    stream.filter(track=conf.get('tags'))


class StreamListener(tweepy.StreamListener):
    # Stream listener lass inherits from tweepy.StreamListener
    # and overwrites on_status/on_error method
    def __init__(self, configuration, db_connection):
        super(StreamListener, self).__init__()
        self.conf = configuration
        self.conn = db_connection

    def on_status(self, status):
        print("new item:", status.text)
        is_retweet = hasattr(status, "retweeted_status")
        is_extended = hasattr(status, "extended_tweet")
        is_quoted = hasattr(status, "quoted_status")
        is_quote_truncated = False if not is_quoted else hasattr(status.quoted_status,
                                                                 "extended_tweet")

        created_at = status.created_at.strftime("%Y%m%d%H%M%S")
        screen_name = status.user.screen_name
        user_id = status.author.id

        tweet_text = utils.get_full_text(status, is_extended)
        tweet_text = utils.cleanup(tweet_text)

        quoted_text = ""
        if is_quoted:
            quoted_text = utils.get_full_text(status.quoted_status, is_quote_truncated)
            quoted_text = utils.cleanup(quoted_text)

        # persistence
        # TODO: data sanitization
        to_insert = [str(user_id),
                     created_at,
                     screen_name.replace("'", "''"),
                     str(is_retweet*1),
                     str(is_quoted*1),
                     tweet_text.replace("'", "''"),
                     quoted_text.replace("'", "''")]
        
        # write to CSV
        # TODO: print headers once here
        with open(self.conf.get('output_file_path_twitter'), "a", encoding="utf-8") as f:
            f.write(",".join(to_insert)+"\n")
        # write to DB
        insert_tweet(self.conn, to_insert)

    def on_error(self, status_code):
        print("error in streaming", status_code)


