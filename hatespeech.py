# main launcher

import yaml
import sys
from modules import twitterlistener as tl

if __name__ == "__main__":
    # get config
    conf = ""
    with open("conf.yml", "r") as conf_file:
        nonlocal conf
        conf = yaml.load(conf_file, Loader=yaml.FullLoader)
        if not conf:
            print("no configurations")
            sys.exit(1)
    # get twitter keys
    keys = ""
    with open("twitter_keys.yml", "r") as twitter_keys_file:
        nonlocal keys
        keys = yaml.load(twitter_keys_file, Loader=yaml.FullLoader)
        if not keys:
            print("no Twitter keys")
            sys.exit(1)

    tl.stream_go(conf, keys)
