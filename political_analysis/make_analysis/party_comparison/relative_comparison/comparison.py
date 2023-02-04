import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# HO CALCOLATO PER OGNI POLITICO QUANTI TWEET BUONI, CATTIVI E NEUTRALI/NON DEFINITI HA PUBBLICATO 
# E HO CALCOLATO LE PERCENTUALI SUI SUOI TWEET TOTALI.
# SUCCESSIVAMENTE PER OGNI PARTITO HO CALCOLATO LA MEDIA DEI TWEET BUONI, CATTIVI E NEUTRALI/NON DEFINITI
# DEI PROPRI POLITICI


def tweets_percentual_for_any_label_and_party(tweets_users):
    relative_comparison = tweets_users.groupby(["politician_name", "label"]).count().reset_index()
    relative_comparison.columns = ["politician_name", "label", "tweets_number"]

    # PREPARE DATA
    good_politicians_tweets = relative_comparison[relative_comparison["label"] == "good"]["tweets_number"].tolist()
    bad_politicians_tweets = relative_comparison[relative_comparison["label"] == "bad"]["tweets_number"].tolist()

    relative_comparison = relative_comparison.drop('label', 1)

    relative_comparison = relative_comparison.groupby(["politician_name"]).sum()

    relative_comparison["good_tweets"] = good_politicians_tweets
    relative_comparison["bad_tweets"] = bad_politicians_tweets
    relative_comparison["neutral/not defined"] = relative_comparison["tweets_number"] - relative_comparison["good_tweets"] - relative_comparison["bad_tweets"]


    # PERCENTUAL
    for column in relative_comparison:
        relative_comparison[column] = relative_comparison[column].astype(float)


    for label in relative_comparison.index:
        relative_comparison.loc[label]["good_tweets"] *= 100 / relative_comparison.loc[label]["tweets_number"]
        relative_comparison.loc[label]["bad_tweets"] *= 100 / relative_comparison.loc[label]["tweets_number"]
        relative_comparison.loc[label]["neutral/not defined"] *= 100 / relative_comparison.loc[label]["tweets_number"]

    return relative_comparison


def format_dataframe_for_plotting(relative_comparison):
    relative_comparison = relative_comparison.drop('tweets_number', 1)

    relative_comparison = pd.merge(relative_comparison, users[['politician_name', 'political_party']], on='politician_name', how='left')

    relative_comparison = relative_comparison.groupby(["political_party"]).mean().reset_index()
    relative_comparison.columns = ["label", "good_tweets", "bad_tweets", "neutral/not defined"]

    relative_comparison_temp = pd.DataFrame()

    relative_comparison_temp["label"] = ["good_tweets", "bad_tweets", "neutral/not defined"]
    relative_comparison_temp["Dem"] = relative_comparison.loc[0].tolist()[1:]
    relative_comparison_temp["Rep"] = relative_comparison.loc[1].tolist()[1:]
    
    return relative_comparison_temp.copy()


def plot_results(relative_comparison):
    relative_comparison_plot = relative_comparison.plot(x = 'label', kind = 'bar', title = 'relative party comparison', 
                                                    color = ["red", "blue"], mark_right = True) 

    relative_comparison_plot.set_ylabel("tweets percentual")
    relative_comparison_plot.set_xlabel("")

    plt.xticks(rotation=0)


    dem_tweets_count = []
    rep_tweets_count = []

    for i in range(len(relative_comparison)):
        dem_tweets_count.append(relative_comparison.loc[i]["Dem"])
        rep_tweets_count.append(relative_comparison.loc[i]["Rep"])


    for bar, tweet_count in zip(relative_comparison_plot.patches, dem_tweets_count + rep_tweets_count):
        x_position_to_write = bar.get_x() + bar.get_width() / 2
        y_position_to_write = bar.get_y() + bar.get_height() / 2

        relative_comparison_plot.text(x_position_to_write, y_position_to_write, str(round(tweet_count, 2)) + " %", ha='center', 
                                      va='center', fontsize=6, fontweight='bold', color='white')

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

relative_comparison = tweets_percentual_for_any_label_and_party(tweets_users)

relative_comparison = format_dataframe_for_plotting(relative_comparison)

plot_results(relative_comparison)