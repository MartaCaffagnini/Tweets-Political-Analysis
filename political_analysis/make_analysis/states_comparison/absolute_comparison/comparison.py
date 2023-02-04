import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import shapely
import matplotlib.patches as mpatches
import geopandas as gpd
import geoplot as gplt
import os


# HO SOMMATO TUTTI I TWEET BUONI - CATTIVI E NEUTRALI/NON DEFINITI DEI POLITICI DI UNO STATO
# (INDIPENDENTEMENTE CHE SIANO DEM O REP) E NE HO CALCOLATO LE PERCENTUALI SUI TWEET TOTALI 
# DELLO STATO. 


def tweets_percentual_for_any_label_and_state(tweets_users):
    tweets_users_with_location = tweets_users[tweets_users["account_location"] != "none"]

    absolute_comparison = tweets_users_with_location.groupby(["label", "account_location"]).count().reset_index()
    absolute_comparison.columns = ["label", "account_location", "tweets_number"]

    # TRANSFORM STRUCTURE OF DATA
    absolute_comparison_temp = pd.DataFrame()
    absolute_comparison_temp["account_location"] = sorted(list(set(absolute_comparison["account_location"])))
    absolute_comparison_temp["good_tweets"] = absolute_comparison[absolute_comparison["label"] == "good"]["tweets_number"].tolist()
    absolute_comparison_temp["bad_tweets"] = absolute_comparison[absolute_comparison["label"] == "bad"]["tweets_number"].tolist()
    absolute_comparison_temp["neutral/not defined"] = absolute_comparison[absolute_comparison["label"] == "neutral/not defined"]["tweets_number"].tolist()

    # MUST PARSE TO FLOAT 
    for column in absolute_comparison_temp.columns[1:]:
        absolute_comparison_temp[column] = absolute_comparison_temp[column].astype(float)

    # PERCENTUAL
    for label in absolute_comparison_temp.index:
        total_tweets = sum([absolute_comparison_temp.loc[label][column] for column in absolute_comparison_temp.columns[1:]])
        absolute_comparison_temp.at[label, "good_tweets"] *= 100 / total_tweets 
        absolute_comparison_temp.at[label, "bad_tweets"] *= 100 / total_tweets 
        absolute_comparison_temp.at[label, "neutral/not defined"] *= 100 / total_tweets

    return absolute_comparison_temp.copy()


def plot_results(absolute_comparison):
    usa = gpd.read_file('states_comparison/geo_data/states.shp')
    usa = usa[usa["STATE_NAME"] != "District of Columbia"]
    usa = usa[["STATE_NAME", "geometry"]]
    usa = usa.sort_values(by=['STATE_NAME'])
    usa.index = range(50)

    usa["good_tweets"] = absolute_comparison["good_tweets"]
    usa["bad_tweets"] = absolute_comparison["bad_tweets"]
    usa["neutral/not defined"] = absolute_comparison["neutral/not defined"]

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

tweets_users = pd.merge(tweets[["label", "politician_name"]], users[['politician_name', 'account_location']], on='politician_name', how='left')

absolute_comparison = tweets_percentual_for_any_label_and_state(tweets_users)

plot_results(absolute_comparison)