def get_full_text(status, is_extended):
    if is_extended:
        return status.extended_tweet["full_text"]

    status_text = status.text
    try:
        retweeted_status_text = status.retweeted_status.text
    except AttributeError:
        return status_text

    try:
        retweeted_status_extended_tweet_text = status.retweeted_status.extended_tweet.get('full_text')
    except AttributeError:
        return retweeted_status_text
    return retweeted_status_extended_tweet_text


def write_csv_header(conf):
    with open(conf.get('output_file_path_twitter'), "w") as f:
        f.write(",".join(conf.get('twitter_status_fields_to_report_headers'))+"\n")
