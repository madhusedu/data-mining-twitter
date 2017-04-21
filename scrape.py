import multiprocessing
import time
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import argparse
import string
import json

Timer=30

def get_parser():
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    parser.add_argument("-d",
                        "--data-dir",
                        dest="data_dir",
                        help="Output/Data Directory")
    return parser


class MyListener(StreamListener):
    def __init__(self, data_dir, query):
        query_fname = format_filename(query)
        self.outfile = "%s/stream_%s.json" % (data_dir, query_fname)

    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                data=data.encode('utf-8')
                f.write(data)
                print(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True


def format_filename(fname):
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status

def stream_func():
    parser = get_parser()
    args = parser.parse_args()
    auth = OAuthHandler('Xk2Ahw2n4YSvofc492foBeZe5', 't0F8eBEWKzGjAOkZlwpzX7lxpI2gcr9Hre7JNIyKqq4qruCsNG')
    auth.set_access_token('840939171816517632-VmLPKuAENvcMcWwhdcNqxvf9461rLBD', '9V3PUnuz90PB2rrNQsONJaUjmWlKf5gzLN2bHzxAMaFRa')
    api = tweepy.API(auth)

    twitter_stream = Stream(auth, MyListener(args.data_dir, args.query))
    twitter_stream.filter(track=[args.query])

if __name__ == '__main__':
    p = multiprocessing.Process(target= stream_func)
    p.start()

    time.sleep(Timer)

    p.terminate()

    p.join()



