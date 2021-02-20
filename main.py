import tweepy
import yaml
import utils


def stream_go(conf, keys):
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
    stream_listener = StreamListener(conf)
    stream = tweepy.Stream(auth=api.auth, listener=stream_listener, tweet_mode='extended')

    # headers
    utils.write_csv_header(conf)

    # go!
    stream.filter(track=conf.get('tags'))


class StreamListener(tweepy.StreamListener):
    # Stream listener lass inherits from tweepy.StreamListener
    # and overwrites on_status/on_error method
    def __init__(self, configuration):
        super(StreamListener, self).__init__()
        self.conf = configuration

    def on_status(self, status):
        print("stream", status.id_str)
        is_retweet = hasattr(status, "retweeted_status")
        is_extended = hasattr(status, "extended_tweet")
        is_quoted = hasattr(status, "quoted_status")
        is_quote_truncated = False if not is_quoted else hasattr(status.quoted_status,
                                                                 "extended_tweet")

        created_at = status.created_at.strftime("%Y%m%d%H%M%S")
        screen_name = status.user.screen_name

        tweet_text = utils.get_full_text(status, is_extended)
        tweet_text = utils.cleanup(tweet_text)

        quoted_text = ""
        if is_quoted:
            quoted_text = utils.get_full_text(status.quoted_status, is_quote_truncated)
            quoted_text = utils.cleanup(quoted_text)

        with open(self.conf.get('output_file_path_twitter'), "a", encoding="utf-8") as f:
            f.write(",".join([created_at, screen_name, str(is_retweet), str(is_quoted),
                              tweet_text, quoted_text])+"\n")

    def on_error(self, status_code):
        print("error in streaming", status_code)


if __name__ == "__main__":
    # get config
    with open("conf.yml", "r") as conf_file:
        conf = yaml.load(conf_file, Loader=yaml.FullLoader)
        if not conf:
            print("no configurations")
        else:
            with open("twitter_keys.yml", "r") as twitter_keys_file:
                keys = yaml.load(twitter_keys_file, Loader=yaml.FullLoader)
                if not keys:
                    print("no Twitter keys")

                stream_go(conf, keys)

