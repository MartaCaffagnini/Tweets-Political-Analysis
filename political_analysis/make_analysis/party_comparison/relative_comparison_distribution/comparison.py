import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

# HO CALCOLATO PER OGNI POLITICO QUANTI TWEET BUONI, CATTIVI E NEUTRALI/NON DEFINITI HA PUBBLICATO.
# SUCCESSIVAMENTE IN OGNI SUBPLOT HO PLOTTATO LE DISTRIBUZIONI DEI TWEET BUONI, CATTIVI E 
# NEUTRALI/NON DEFINITI DEI MEMBRI DI OGNI PARTITO


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




def plot_results(relative_comparison):

    with sns.axes_style(style="whitegrid"):
        
        plt.subplots_adjust(wspace=0.35)

        # GOOD COMPARISON
        good_dem_tweets_percentual = relative_comparison[relative_comparison["political_party"] == "Dem"]["good_tweets"].tolist() 
        good_rep_tweets_percentual = relative_comparison[relative_comparison["political_party"] == "Rep"]["good_tweets"].tolist()

        plt.subplot(131)
        fig = sns.kdeplot(good_dem_tweets_percentual, shade=True, color="red")
        fig = sns.kdeplot(good_rep_tweets_percentual, shade=True, color="blue")
        plt.xlabel("good tweets percentual")

        # BAD COMPARISON
        bad_dem_tweets_percentual = relative_comparison[relative_comparison["political_party"] == "Dem"]["bad_tweets"].tolist() 
        bad_rep_tweets_percentual = relative_comparison[relative_comparison["political_party"] == "Rep"]["bad_tweets"].tolist()

        plt.subplot(132)
        fig = sns.kdeplot(bad_dem_tweets_percentual, shade=True, color="red")
        fig = sns.kdeplot(bad_rep_tweets_percentual, shade=True, color="blue")
        plt.xlabel("bad tweets percentual")

        # NEUTRAL/NOT DEFINED COMPARISON
        neutral_notdefined_dem_tweets_percentual = relative_comparison[relative_comparison["political_party"] == "Dem"]["neutral/not defined"].tolist() 
        neutral_notdefined_rep_tweets_percentual = relative_comparison[relative_comparison["political_party"] == "Rep"]["neutral/not defined"].tolist()

        plt.subplot(133)
        fig = sns.kdeplot(neutral_notdefined_dem_tweets_percentual, shade=True, color="red")
        fig = sns.kdeplot(neutral_notdefined_rep_tweets_percentual, shade=True, color="blue")
        plt.xlabel("neutral_notdefined tweets percentual")


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

# FORMAT FOR PLOTTING
relative_comparison = relative_comparison.drop('tweets_number', 1)
relative_comparison = pd.merge(relative_comparison, users[['politician_name', 'political_party']], on='politician_name', how='left')


plot_results(relative_comparison)