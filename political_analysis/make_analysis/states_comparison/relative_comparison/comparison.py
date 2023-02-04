import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import shapely
import matplotlib.patches as mpatches
import geopandas as gpd
import geoplot as gplt
import os

# HO CALCOLATO PER OGNI POLITICO QUANTI TWEET BUONI, CATTIVI E NEUTRALI/NON DEFINITI HA PUBBLICATO
# E HO CALCOLATO LE PERCENTUALI SUI SUOI TWEET TOTALI.
# SUCCESSIVAMENTE PER OGNI STATO HO CALCOLATO LA MEDIA DEI TWEET BUONI, CATTIVI E NEUTRALI/NON DEFINITI
# DEI PROPRI POLITICI (QUI NEL GRAFICO HO RAPPRESENTATO SOLAMENTE "LA DENSITÀ DELLA BONTÀ DEI TWEET")



def tweets_percentual_for_any_label_and_state(tweets, users):

    tweets = tweets[["politician_name", "label", "text"]]
    tweets = tweets.groupby(["politician_name", "label"]).count().reset_index()
    tweets.columns = ["politician_name", "label", "tweets_number"]

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


    tweets_temp = pd.merge(tweets_temp, users[['politician_name', 'account_location']], on='politician_name', how='left')
    tweets_temp = tweets_temp[["account_location", "good_tweets", "bad_tweets", "neutral/not defined"]]
    tweets_temp = tweets_temp[tweets_temp["account_location"] != "none"]
    
    # PERCENTUAL FOR EACH STATE
    tweets_temp = tweets_temp.groupby(["account_location"]).mean().reset_index()

    return tweets_temp.copy()


def plot_results(relative_comparison):
    usa = gpd.read_file('states_comparison/geo_data/states.shp')
    usa = usa[usa["STATE_NAME"] != "District of Columbia"]
    usa = usa[["STATE_NAME", "geometry"]]
    usa = usa.sort_values(by=['STATE_NAME'])
    usa.index = range(50)

    usa["good_tweets"] = relative_comparison["good_tweets"]
    usa["bad_tweets"] = relative_comparison["bad_tweets"]
    usa["neutral/not defined"] = relative_comparison["neutral/not defined"]

    usa.plot(column='good_tweets', legend=True)

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
 
relative_comparison = tweets_percentual_for_any_label_and_state(tweets, users)

plot_results(relative_comparison)