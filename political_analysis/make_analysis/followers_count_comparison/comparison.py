import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os


def tweets_percentual_for_any_label_and_politician(tweets, users):
    tweets = tweets[["label", "politician_name", "text"]]
    tweets = tweets.groupby(["label", "politician_name"]).count().reset_index()
    tweets.columns = ["label", "politician_name", "tweets_number"]

    # HANDLE MISSING DATA
    tweets = tweets.append({'politician_name': 'Rep_Matt_Gaetz', 'label': "neutral/not defined", 'tweets_number': 0}, ignore_index=True)
    tweets = tweets.append({'politician_name': 'GregHarper', 'label': "neutral/not defined", 'tweets_number': 0}, ignore_index=True)
    tweets.sort_values(by=['politician_name'], inplace=True)
    tweets.index = range(len(tweets))

    # TRANSFORM STRUCTURE OF DATA
    tweets_temp = pd.DataFrame()
    tweets_temp["politician_name"] = sorted(list(set(tweets["politician_name"])))
    tweets_temp["good_tweets"] = tweets[tweets["label"] == "good"]["tweets_number"].tolist()
    tweets_temp["bad_tweets"] = tweets[tweets["label"] == "bad"]["tweets_number"].tolist()
    tweets_temp["neutral/not defined"] = tweets[tweets["label"] == "neutral/not defined"]["tweets_number"].tolist()

    # MUST PARSE TO FLOAT 
    for column in tweets_temp.columns[1:]:
        tweets_temp[column] = tweets_temp[column].astype(float)

    # PERCENTUAL FOR EACH USER
    for row in tweets_temp.index:
        total_tweets = sum([tweets_temp.loc[row][column] for column in tweets_temp.columns[1:]])
        tweets_temp.at[row, "good_tweets"] *= 100 / total_tweets 
        tweets_temp.at[row, "bad_tweets"] *= 100 / total_tweets
        tweets_temp.at[row, "neutral/not defined"] *= 100 / total_tweets


    tweets_temp = pd.merge(tweets_temp, users[['politician_name', 'followers_count']], on='politician_name', how='left')

    # print(tweets)

    return tweets_temp.copy()


def plot_results(comparison):

    # SET PLOTTING
    x = np.array(sorted(comparison["followers_count"]))[:535]
    plt.xlabel("followers count")
    plt.ylabel("tweets percentual")
    
    # PLOT GOOD
    y = comparison["good_tweets"].tolist()[:535]
    plt.plot(x, y, 'o', color='yellow', label='good tweets')
    
    # PLOT BAD 
    y = comparison["bad_tweets"].to_numpy()[:535]
    plt.plot(x, y, 'o', color='purple', label='bad tweets')

    # PLOT NEUTRAL / NOT DEFINED 
    y = comparison["neutral/not defined"].to_numpy()[:535]
    plt.plot(x, y, 'o', color='green', label='neutral/not defined tweets')
    
    
    plt.legend(loc='best')
    plt.show()




#################################################################################################################
#                                                ______
#                                               | MAIN |
#                                                 
#################################################################################################################


os.chdir("..")

desidered_path = os.getcwd() + '/labelled_tweet.csv'
tweets = pd.read_csv(desidered_path)

desidered_path = os.getcwd() + '/users.csv'
users = pd.read_csv(desidered_path)

comparison = tweets_percentual_for_any_label_and_politician(tweets, users)

plot_results(comparison)