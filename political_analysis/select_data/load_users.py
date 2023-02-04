import json
import pandas as pd
import datetime
import os

from string import punctuation

def get_info_from(json_user):
    user = json.loads(json_user)
    return [user["screen_name"], user["location"], user["followers_count"], user["statuses_count"], user["created_at"], user["id_str"]]


def get_parsed_location(location):
    locations_postals_codes = pd.read_csv('/state_to_postalcode.csv')

    locations_postals_codes = {postal_code: state for state, postal_code in locations_postals_codes.values.tolist()}
    
    location = location.replace("'s", "")
    location = location.translate(str.maketrans('', '', punctuation))
    location = location.replace("Washington DC", "")
        
    for word in location.split():
        if word in set(locations_postals_codes.keys()):
            return locations_postals_codes[word]
        elif word in set(locations_postals_codes.values()):
            return word
    
    return location


with open('original_users.json') as json_file:
    users = [get_info_from(json_user) for json_user in json_file]



#################################################################################################################
#                                                ______
#                                               | MAIN |
#                                                 
#################################################################################################################


users = [[user[0], user[2], user[3], user[4], user[5]] for user in users]

users = pd.DataFrame(users, columns=["politician_name", "followers_count", "posted_tweet_number", "account_created_at", "account_id"])

os.chdir("..")
desidered_path = os.getcwd() + '/make_analysis/users.csv'
users.to_csv(desidered_path, index=False)