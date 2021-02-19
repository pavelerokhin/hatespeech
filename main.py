import tweepy
import yaml
import utils


def stream_go(conf):
    """
    main function launching twitter filtered streaming
    input from config file
    output goes to the output/[csv_file]
    """
    # authorisation
    auth = tweepy.OAuthHandler(conf.customer_key, conf.customer_secret)
    auth.set_access_token(conf.access_key, conf.access_secret)
    api = tweepy.API(auth)

    # stream
    stream_listener = StreamListener(conf)
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener, tweet_mode='extended')

    # headers
    utils.write_csv_header(conf)

    # go!
    stream.filter(conf.tags)


class StreamListener(tweepy.StreamListener):
    # Stream listener lass inherits from tweepy.StreamListener
    # and overwrites on_status/on_error method
    def __init__(self, configuration):
        self.conf = configuration

    def on_status(self, status):
        print("stream", status.id_str)
        is_retweet = hasattr(status, "retweeted_status")
        is_truncated = hasattr(status, "extended_tweet")
        is_quoted = hasattr(status, "quoted_status")
        is_quote_truncated = False if not is_quoted else hasattr(status.quoted_status,
                                                                 "extended_tweet")
        tweet_text = utils.get_full_text(status, is_truncated)
        tweet_text = utils.cleanup(tweet_text)

        quoted_text = ""
        if is_quoted:
            quoted_text = utils.get_full_text(status.quoted_status, is_quote_truncated)
            quoted_text = utils.cleanup(quoted_text)

        with open(self.conf.output_file_path_twitter, "w", encoding="utf-8") as f:
            values_to_write = iter(exec(field) for field in
                                   self.conf.twitter_status_fields_to_report)
            f.write(",".join(values_to_write))

    def on_error(self, status_code):
        print("error in streaming", status_code)


if __name__ == "__main__":
    # get config
    with open("cong.yml", "r") as yf:
        conf = yaml.load(yf, Loader=yaml.FullLoader)
        if not conf:
            print("no configurations")
        else:
            stream_go(conf)

