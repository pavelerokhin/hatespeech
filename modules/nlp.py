import spacy

nlp = spacy.load("en_core_web_sm")

WHITESPACE = " "


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
        .replace("\n", WHITESPACE)\
        .replace(",", WHITESPACE)\
        .replace(",./\\", "")\
        .split()

    return " ".join(words)


def extract_entities(text):
    if text:
        doc = nlp(text)
        return doc.ents if doc.ents else []
    return []


def extract_tweet_components(text):
    #extract hashtags
    #extract emails
    #extract other users

    pass