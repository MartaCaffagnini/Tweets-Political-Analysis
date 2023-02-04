import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# HO SOMMATO TUTTI I TWEET BUONI - CATTIVI E NEUTRALI/NON DEFINITI E PER OGNUNA DI QUESTE SOMME
# HO CALCOLATO IN PERCENTUALE QUANTI TWEET APPARTENESSERO A UN PARTITO RISPETTO AD UN ALTRO 


def tweets_percentual_for_any_label_and_party(tweets_users):
    absolute_comparison = tweets_users.groupby(["label", "political_party"]).count().reset_index()
    absolute_comparison.columns = ["label", "political_party", "tweets_number"]

    tweet_count_foreach_category = absolute_comparison["tweets_number"].tolist()

    i = 0
    while i < len(tweet_count_foreach_category):
        percentual_maker = 100 / (tweet_count_foreach_category[i] + tweet_count_foreach_category[i + 1]) 
        tweet_count_foreach_category[i] *= percentual_maker
        tweet_count_foreach_category[i + 1] *= percentual_maker

        i += 2

    absolute_comparison["tweets_number"] = tweet_count_foreach_category 

    return absolute_comparison


def format_dataframe_for_plotting(absolute_comparison):
    dem_count = absolute_comparison[absolute_comparison["political_party"] == "Dem"][["label","tweets_number"]]
    dem_count.columns = ["label", "dem_tweets_number"]

    rep_count = absolute_comparison[absolute_comparison["political_party"] == "Rep"][["tweets_number"]]

    dem_count["rep_tweets_number"] = rep_count["tweets_number"].tolist() 
    absolute_comparison = dem_count.copy()
    absolute_comparison.index = [0, 1, 2]

    print(absolute_comparison)

    return absolute_comparison


def plot_results(absolute_comparison):
    absolute_comparison_plot = absolute_comparison.plot(x = 'label', kind = 'barh', stacked = True, 
                                                        color = ["red", "blue"], mark_right = True) 

    plt.legend(loc="best")

    absolute_comparison_plot.set_ylabel("tweets classifications")
    absolute_comparison_plot.set_xlabel("tweets percentual")

    dem_tweets_count = []
    rep_tweets_count = []

    for i in range(len(absolute_comparison)):
        dem_tweets_count.append(absolute_comparison.loc[i]["dem_tweets_number"])
        rep_tweets_count.append(absolute_comparison.loc[i]["rep_tweets_number"])

    for bar, tweet_count in zip(absolute_comparison_plot.patches, dem_tweets_count + rep_tweets_count):
        x_position_to_write = bar.get_x() + bar.get_width() / 2
        y_position_to_write = bar.get_y() + bar.get_height() / 2

        absolute_comparison_plot.text(x_position_to_write, y_position_to_write, str(round(tweet_count, 2)) + " %", ha='center', 
                                      va='center', fontsize=16, fontweight='bold', color='white')

    plt.show()




#################################################################################################################
#                                                ______
#                                               | MAIN |
#                                                 
#################################################################################################################


os.chdir("..")
os.chdir("..")

desidered_path = os.getcwd() + '/labelled_tweet.csv'
tweets = pd.read_csv(desidered_path)

desidered_path = os.getcwd() + '/users.csv'
users = pd.read_csv(desidered_path)

tweets_users = pd.merge(tweets[["label", "politician_name"]], users[['politician_name', 'political_party']], on='politician_name', how='left')


absolute_comparison = tweets_percentual_for_any_label_and_party(tweets_users)

absolute_comparison = format_dataframe_for_plotting(absolute_comparison)

plot_results(absolute_comparison)