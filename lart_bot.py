"""
Twitter Python Bot
L'Art Du Monde @l_art365
Searches for the most popular art on twitter based on art type.
Library: Tweepy
http://docs.tweepy.org/en/v3.6.0/getting_started.html
"""
# use for date
from datetime import date, timedelta
# use for dictionary sorting
from collections import OrderedDict
from operator import itemgetter
# use for ez config files
import configparser, sys
# tweepy library
import tweepy

if __name__ == '__main__':

    # python info: 3.6
    # print(sys.version)
    # check the number of args
    config_file_path = ''

    if len(sys.argv) > 1:
        config_file_path = sys.argv[1]
    else:
        # print('Usage: %s config.ini' % (sys.argv[0],))
        sys.exit()

    # load the configuration from the config file
    config = configparser.ConfigParser()

    # print for debugging
    # print('Using config file located at: ', sys.argv[1])

    # read the config file and use it for the config parser
    with open(config_file_path, 'r') as f:
        config.read_file(f)

    # load the key and secrets from the config file
    consumer_key = config['Twitter']['consumer_key']
    consumer_secret = config['Twitter']['consumer_secret']
    access_token = config['Twitter']['access_token']
    access_token_secret = config['Twitter']['access_token_secret']

    # logs in using the user authorized
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # log in with a specific access token
    auth.set_access_token(access_token, access_token_secret)

    # get the api w/ the auth specified
    # NOTE: rate limit 180 calls every 15 minutes
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # print tweepy version
    # print('tweepy version ' + tweepy.__version__)

    # logged into the service, get the username
    logged_in_user = api.me()
    # print('connected to api as user', logged_in_user.name)

    # Yesterday's date
    yy = str(date.today() - timedelta(1))

    # categories of hashtags used for search
    categories = ["#art", "#contemporaryart", "#modernart", "#abstractart", "#surrealism", "#impressionism", "#modernism",
                  "#popart", "#expressionism", "#streetart", "#cubism", "#romanticism", "#realism", "#classicism"]

    # contains tweets id and count of retweets and likes
    # key: tweet id  value: interest count
    lib = {}

    # limit on API search requests
    limit = 150

    # Check if tweet is stored in txt file
    # Check if tweet was previously used by me
    def tweeted(tweets, tweet):
        for tweet_id in tweets:
            if tweet_id == tweet:
                return True
        return False

    # Post 2 Tweets at a time
    def post_tweet(lib, tweets, file, tweet_count):
        for k in lib.keys():
            if not tweeted(tweets, k):
                try:
                    if tweet_count != 0:
                        write_to_file(k, file)
                        api.retweet(k)
                        tweet_count -= 1
                        print("Printing tweet with id: " + str(k))
                    else: break
                except tweepy.TweepError:
                    if tweepy.TweepError == "[{'code': 327, 'message': 'You have already retweeted this Tweet.'}]":
                        tweet_count += 1
                        continue

    # Write to File
    def write_to_file(id, file):
        file.write(str(id) + "\n")

    for hashtag in categories:
    # Note: search delay is about 29 sec
        for tweet in tweepy.Cursor(api.search, q=hashtag, result_type = "mix", since = yy, include_entities = True).items(limit):
            if 'media' in tweet.entities:
                interest_count = tweet.favorite_count + tweet.retweet_count
                if interest_count >= 10:
                    lib[tweet.id] = interest_count

    # order the lib from highest to lowest in engagement
    lib = OrderedDict(sorted(lib.items(), key = itemgetter(1), reverse = True))

    # open file containing previous tweets
    file = open("tweets.txt", "r+")
    tweets = file.readlines()
    post_tweet(lib, tweets, file, 2)
    #print(tweeted(tweets, "000000000000000000"))

    # for key in lib:
    #     file.write(str(key)+"\n")

    # check manually for tweet
    # https://twitter.com/statuses/id