import time
import pandas as pd
import numpy as np
import joblib
import os
from random import shuffle


from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from sklearn.feature_selection import SelectKBest, chi2, f_classif

from sklearn.model_selection import train_test_split

from sklearn.naive_bayes import MultinomialNB, GaussianNB, BernoulliNB, CategoricalNB, ComplementNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC, LinearSVC



def train_test_classificators_and_get_the_best_one(classificators, X_train, X_test, y_train, y_test):
    best_accuracy = -1

    for clf, name in classificators:
        start = time.clock()
        
        clf.fit(X_train, y_train)
        score = round(clf.score(X_test, y_test) * 100, 2)

        execution_time = (time.clock() - start) / 60
        
        print(name + ": " + str(score) + " %, execution time: " + str(execution_time))

        if best_accuracy < score:
            best_accuracy = score
            best_clf = clf
            best_clf_name = name
    
    return best_clf, best_clf_name


def get_X_and_y_after_features_extraction(tweets):
    vectorizer = TfidfVectorizer(ngram_range=(1, 3)) 

    X = vectorizer.fit_transform(tweets["text"].astype('U').tolist())
    y = tweets["label"].tolist()

    os.chdir("..")
    os.chdir("..")
    desidered_path = os.getcwd() + '/political_analysis/predict_data/FittedTfidfVectorizer.pkl'
    joblib.dump(vectorizer, desidered_path)

    print("ngram range " + str(vectorizer.ngram_range))
    # print(vectorizer.get_feature_names(), sep='\n')
    print("total features number " + str(len(vectorizer.get_feature_names())))

    return X, y


def get_X_after_feature_selection(X, y):
    best_feature_number = 450000
    feature_selector = SelectKBest(score_func=f_classif, k=best_feature_number)
    selected_feature = feature_selector.fit_transform(X, y)

    desidered_path = os.getcwd() + '/political_analysis/predict_data/FittedSelectKBest.pkl'
    joblib.dump(feature_selector, desidered_path)
    
    print("selected features number " + str(best_feature_number) + "\n")
    return selected_feature


def get_label(tweet):
    return tweet[0]


def get_balanced_dataframe(tweets):
    tweets = tweets.values.tolist()
    
    shuffle(tweets)

    good_tweets = [tweet for tweet in tweets if get_label(tweet) == 4]
    bad_tweets = [tweet for tweet in tweets if get_label(tweet) == 0]

    print("total tweets number " + str(len(tweets)))
    print("good tweets number " + str(len(good_tweets)))
    print("bad tweets number " + str(len(bad_tweets)))

    balanced_number_of_tweets = min(len(good_tweets), len(bad_tweets))
   
    print("selected tweets number for each class " + str(balanced_number_of_tweets))
    
    balanced_tweets = good_tweets[:balanced_number_of_tweets] + bad_tweets[:balanced_number_of_tweets]

    balanced_tweets = pd.DataFrame(balanced_tweets, columns=["label", "text"])

    return balanced_tweets


# def is_dataframe_balanced(tweets):
#     i = j = 0

#     for label in tweets["label"].tolist():
#         if label == 4:
#             i += 1
#         else:
#             j += 1

#     print("dataset balancing " + str(i) + " " + str(j))



#################################################################################################################
#                                                ______
#                                               | MAIN |
#                                                 
#################################################################################################################

test_size = 0.125

tweets = pd.read_csv('preprocessed_training.csv') #, encoding="latin-1"

tweets = get_balanced_dataframe(tweets)

# print(is_dataframe_balanced(tweets))

X, y = get_X_and_y_after_features_extraction(tweets)

X = get_X_after_feature_selection(X, y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

print("training - test ratio = " + str((1 - test_size) * 100) + "/" + str(test_size * 100))

classificators = [
                    #(MultinomialNB(), "multinomial bayes"),
                    (BernoulliNB(alpha=1.0e-10, fit_prior=False), "BernoulliNB"),                       
                    #(ComplementNB(), "complement bayes"),
                    #(LogisticRegression(), "LogisticRegression"), 
                    #(SGDClassifier(loss="modified_huber", max_iter=10000, alpha=0.5), "SGDClassifier"),                       
                    #   (KNeighborsClassifier(), "KNeighborsClassifier"),                   # lento
                    # (DecisionTreeClassifier(max_depth=10, random_state=101, min_samples_leaf=15), "DecisionTreeClassifier"),                               # non buoni risultati
                    # (RandomForestClassifier(n_estimators=70, oob_score=True, n_jobs=-1, random_state=101, min_samples_leaf=30), "RandomForestClassifier"), # lento
                    # (SVC(kernel='linear', probability=True, class_weight=None), "SVM")
                    #(LinearSVC(C=0.025, random_state=42), "linear SVC")
                ]

best_clf, best_clf_name = train_test_classificators_and_get_the_best_one(classificators, X_train, X_test, y_train, y_test)

print("best clf: " + best_clf_name)

desidered_path = os.getcwd() + '/political_analysis/predict_data/Trained' + best_clf_name + '.pkl'
joblib.dump(best_clf, desidered_path)