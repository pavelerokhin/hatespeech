import tweepy
from itertools import chain

# tokens
customer_key = ""
customer_secret = ""
access_key = ""
access_secret = ""

# configurations
output_file_path_twitter = "output/out.csv"
twitter_status_fields_to_report = ["status.created_at",
                                   "status.user.screen_name",
                                   "is_retweet",
                                   "is_quote",
                                   "text",
                                   "quoted_text"]
twitter_status_fields_to_report_headers = ["created at",
                                           "user name",
                                           "is retweet",
                                           "is quote",
                                           "text",
                                           "quoted text"]
tags = ["hate speech"]


def get_full_text(status, is_truncated):
    if is_truncated:
        return status.extended_tweet["full_text"]
    return status.text


def cleanup(text):
    whitespace = " "
    return text.replace("\n", whitespace).replace(",", whitespace)


def write_csv_header():
    with open(output_file_path_twitter, "w") as f:
        f.write(",".join(twitter_status_fields_to_report_headers))


class StreamListener(tweepy.StreamListener):
    # Stream listener lass inherits from tweepy.StreamListener
    # and overwrites on_status/on_error method
    def on_status(self, status):
        print("stream", status.id_str)
        is_retweet = hasattr(status, "retweeted_status")
        is_truncated = hasattr(status, "extended_tweet")
        is_quoted = hasattr(status, "quoted_status")
        is_quote_truncated = False if not is_quoted else hasattr(status.quoted_status,
                                                                 "extended_tweet")
        tweet_text = get_full_text(status, is_truncated)
        tweet_text = cleanup(tweet_text)

        quoted_text = ""
        if is_quoted:
            quoted_text = get_full_text(status.quoted_status, is_quote_truncated)
            quoted_text = cleanup(quoted_text)

        with open(output_file_path_twitter, "w", encoding="utf-8") as f:
            values_to_write = iter(exec(field) for field in twitter_status_fields_to_report)
            f.write(",".join(values_to_write))

    def on_error(self, status_code):
        print("error in streaming", status_code)


if __name__ == "__main__":
    # authorisation
    auth = tweepy.OAuthHandler(customer_key, customer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # stream
    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener, tweet_mode='extended')

    # headers
    write_csv_header()

    # go!
    stream.filter(tags)

