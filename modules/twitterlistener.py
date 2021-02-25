import tweepy
import utils

from modules import nlp, databaseaccess
from modules.databaseaccess import insert_tweet_to_db, insert_entities_to_db


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
    last_id = databaseaccess.get_last_id(conn)
    stream_listener = StreamListener(conf, conn, last_id)
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener, tweet_mode='extended')

    # headers
    utils.write_csv_header(conf)

    # go!
    stream.filter(languages=conf.get('language'), track=conf.get('tags'))


class StreamListener(tweepy.StreamListener):
    # Stream listener lass inherits from tweepy.StreamListener
    # and overwrites on_status/on_error method
    def __init__(self, configuration, db_connection, last_id):
        super(StreamListener, self).__init__()
        self.conf = configuration
        self.conn = db_connection
        self.last_id = last_id

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
        quoted_text = ""
        if is_quoted:
            quoted_text = utils.get_full_text(status.quoted_status, is_quote_truncated)
            quoted_text = nlp.sanitize(quoted_text)

        extracted_entities_in_tweet = nlp.extract_entities(tweet_text)
        extracted_entities_in_quote = nlp.extract_entities(quoted_text)
        entities_tweet = []
        entities_quote = []

        tweet_text = nlp.sanitize(tweet_text)
        quoted_text = nlp.sanitize(quoted_text)

        # persistence
        # TODO: data sanitization
        self.last_id += 1

        tweet = [str(self.last_id),
                 str(user_id),
                 created_at,
                 screen_name,
                 str(is_retweet*1),
                 str(is_quoted*1),
                 tweet_text,
                 nlp.sanitize(quoted_text)]

        if extracted_entities_in_tweet:
            for et in extracted_entities_in_tweet:
                entities_tweet.append([
                    self.last_id,
                    et.text,
                    et.label,
                    et.label_
                ])
            print("entities in tweet", entities_tweet)

        if extracted_entities_in_quote:
            for eq in extracted_entities_in_quote:
                entities_quote.append([
                    self.last_id,
                    nlp.sanitize(eq.text),
                    eq.label,
                    eq.label_
                ])
            print("entities in quotation", entities_quote)

        # write to CSV
        # TODO: print headers once here
        with open(self.conf.get('output_file_path_twitter'), "a", encoding="utf-8") as f:
            f.write(",".join(tweet)+"\n")
        # write to DB
        insert_tweet_to_db(self.conn, tweet)
        if entities_tweet:
            for et in entities_tweet:
                insert_entities_to_db(self.conn, et)

    def on_error(self, status_code):
        print("error in streaming", status_code)


