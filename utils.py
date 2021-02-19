def get_full_text( status, is_truncated):
    if is_truncated:
        return status.extended_tweet["full_text"]
    return status.text


def cleanup(text):
    whitespace = " "
    return text.replace("\n", whitespace).replace(",", whitespace)


def write_csv_header(conf):
    with open(conf.output_file_path_twitter, "w") as f:
        f.write(",".join(conf.twitter_status_fields_to_report_headers))