import pandas as pd
import difflib


# source --> https://github.com/CivilServiceUSA/us-house/blob/master/us-house/data/us-house.csv
def get_member_parties_1():
    political_info = pd.read_csv('party_member.csv')

    return political_info["name"].tolist(), political_info["party"].tolist()


# source --> https://github.com/unitedstates/congress-legislators/blob/master/legislators-current.yaml
def get_member_parties_2():
    with open('party_member_2.csv') as political_info:

        alreadySet = False

        political_members = []

        parties = []

        for row in political_info:
            if "wikipedia" in row:
                political_member_name = row.replace(" ","").replace("wikipedia:","").replace("\n","")
                
                if "(" in political_member_name:
                    political_member_name = political_member_name[:political_member_name.index('(')]
                
                political_members.append(political_member_name)
                alreadySet = False
            elif "party" in row and not alreadySet:
                political_member_party = row.replace(" ","").replace("party:","").replace("\n","")
                parties.append(political_member_party)
                alreadySet = True

    return political_members, parties


# source --> https://github.com/unitedstates/congress-legislators/blob/master/committee-membership-current.yaml
def get_member_parties_3():
    with open('party_member_3.csv') as political_info:

        political_members = []

        parties = []

        for row in political_info:
            if "name" in row:
                political_member_name = row.replace(" ","").replace("-","").replace("name:","").replace("\n","")
                political_members.append(political_member_name)
            elif "party" in row:
                political_member_party = row.replace(" ","").replace("party:","").replace("\n","")
                
                if political_member_party == "majority":
                    parties.append("Democratic")
                else:
                    parties.append("Republican")


    return political_members, parties


def normalize_party(party_name):
    if "epub" in party_name: 
        return "Rep" 
    else:
        return "Dem"


def get_member_parties():
    members_1, parties_1 = get_member_parties_1()
    members_2, parties_2 = get_member_parties_2()
    members_3, parties_3 = get_member_parties_3()

    parties = list(map(normalize_party, parties_1 + parties_2 + parties_3))

    return members_1 + members_2 + members_3, parties



def get_user_party(user_name, members, parties):
    match = difflib.get_close_matches(user_name, members)

    if match != []:
        return parties[members.index(match[0])] 
    else:
        return "none"



def assign_parties_to_users(users, members, parties):

    setted_users = [
                    [name, location, followers, posted_tweet, account_created_at, get_user_party(name, members, parties)]
                    for name, location, followers, posted_tweet, account_created_at in users.values.tolist()
                   ]

    setted_users = pd.DataFrame(setted_users, columns=["politician_name", "account_location", "followers_count", "posted_tweet_number", "account_created_at", "political_party"])

    setted_users.to_csv('users.csv', index=False)        




#------------------------------------------------------------------------------------------------------------------------

users = pd.read_csv('users.csv')

members, parties = get_member_parties()

assign_parties_to_users(users, members, parties)
    