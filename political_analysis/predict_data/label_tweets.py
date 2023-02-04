import pandas as pd
import numpy as np
import joblib
from sklearn.feature_selection import SelectKBest, f_classif
import os



def get_vectorized_texts(tweets_texts):
    tfidf_vectorizer = joblib.load('FittedTfidfVectorizer.pkl')
    return tfidf_vectorizer.transform(tweets_texts)


def get_text_with_selected_features(vectorized_tweets_texts):
    feature_selector = joblib.load('FittedSelectKBest.pkl')
    return feature_selector.transform(vectorized_tweets_texts)


def get_well_presented_probabilities(prediction_probabilities):  
    normalized_probabilities = []

    for bad_probability, good_probability in prediction_probabilities:
        if abs(good_probability - bad_probability) < 0.075:
            normalized_probabilities.append(["neutral/not defined", round(bad_probability, 3)])
        elif bad_probability > good_probability:
            normalized_probabilities.append(["bad", round(bad_probability, 3)])
        else:
            normalized_probabilities.append(["good", round(good_probability, 3)])

    return normalized_probabilities


def get_predictions(vectorized_text):
    predictor = joblib.load('TrainedBernoulliNB.pkl')
    return get_well_presented_probabilities(predictor.predict_proba(vectorized_text))


def parse_to_matrix_column(array):
    return np.array([[element] for element in array])


def write_labelled_tweets_on_csv(tweets, predictions):
    predictions = np.array(predictions)

    labels = parse_to_matrix_column(predictions[:, 0])
    # probabilities = parse_to_matrix_column(predictions[:, 1])
    
    politicians_names = parse_to_matrix_column(tweets[:, 0])
    texts = parse_to_matrix_column(tweets[:, 1])
    originals_texts_langs = parse_to_matrix_column(tweets[:, 2])
    created_at = parse_to_matrix_column(tweets[:, 3])

    labelled_tweets = np.concatenate((labels, politicians_names, texts, originals_texts_langs, created_at), axis=1) 

    labelled_tweets = pd.DataFrame(labelled_tweets, columns=["label", "politician_name", "text", "original_text_lang", "created_at"])

    os.chdir("..")
    desidered_path = os.getcwd() + '/make_analysis/labelled_tweet.csv'
    labelled_tweets.to_csv(desidered_path, index=False)   



#################################################################################################################
#                                                ______
#                                               | MAIN |
#                                                 
#################################################################################################################

tweets = pd.read_csv('political_tweets_preprocessed.csv')

tweets_texts = tweets["text"].values

tweets = tweets.values

processed_text = get_vectorized_texts(tweets_texts)

processed_text = get_text_with_selected_features(processed_text)

predictions = get_predictions(processed_text)

write_labelled_tweets_on_csv(tweets, predictions)