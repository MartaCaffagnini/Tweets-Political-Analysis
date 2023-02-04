import json
import pandas as pd
import datetime
import os

def get_name_text_lang_timestamp(json_tweet):
    tweet = json.loads(json_tweet)
    timestamp = datetime.datetime.utcfromtimestamp(tweet['created_at'])
    return [tweet["screen_name"], " ".join(tweet["text"].splitlines()), str(tweet["lang"]), str(timestamp)]


#------------------------------------------------------------------------------------------------------------------------------


with open('original_tweets.json') as json_file:
    tweets = [get_name_text_lang_timestamp(json_tweet) for json_tweet in json_file]

tweets = pd.DataFrame(tweets, columns=["politician_name", "text", "original_text_lang", "created_at"])

os.chdir("..")
desidered_path = os.getcwd() + '/preprocess_data/tweets.csv'
tweets.to_csv(desidered_path, index=False)