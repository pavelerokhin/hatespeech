

def sanitize(text):
    return sanitize_punctuation_and_white_spaces(
        sanitize_single_quote_for_sql(text))


def sanitize_single_quote_for_sql(text):
    """
    substitutes a single quote into two single quotes (following SQL syntax)
    """
    return text.replace("'", "''")


def sanitize_punctuation_and_white_spaces(text):
    """
    removes unnecessary punctuation and white spaces
    """
    words = text.lower()\
        .replace(",./\\", "")\
        .split(r'\W+', text)

    return "".join(words)

def sentiment(text):

    pass

def extract_tweet_components(text):
    #extract hashtags
    #extract emails
    #extract other users

    pass