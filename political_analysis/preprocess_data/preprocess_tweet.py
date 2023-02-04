import pandas as pd
from string import punctuation
import time

from nltk.corpus import words as english_vocabolary
from nltk import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer 
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import pos_tag as pos_tag_text
import os

from autocorrect import Speller
# from textblob import TextBlob



#################################################################################################################
#                                                ________________________
#                                               | POSSIBILI MIGLIORAMENTI |
#
#                                                 
#################################################################################################################
  


# get_stemmed_word = PorterStemmer().stem

tweet_useless_punctuation = punctuation.replace("'", "")

tokenize = TweetTokenizer().tokenize

lemmatize = WordNetLemmatizer().lemmatize

get_correct_word_if_it_is_mispelled = Speller(fast=True)

english_stopwords = set(stopwords.words('english'))

all_english_words = set(english_vocabolary.words())

os.chdir("..")
os.chdir("..")
desidered_path = os.getcwd() + '/create_model/preprocess_data/emoji_emoticon.csv'
emojis_emoticon = dict(pd.read_csv(desidered_path).values.tolist())


# def get_stemmed_text(text):
#     return " ".join([get_stemmed_word(word) for word in text.split()])

def get_parsed_pos_tag(tag):
    if tag.startswith("V"): # VB, VBD, VBG, VBN, VBP, VBZ
        return wordnet.VERB
    elif tag.startswith("J"): # JJ, JJR, JJS
        return wordnet.ADJ
    elif tag.startswith("RB"): #RB, RBR, RBS
        return wordnet.ADV
    else:
        return wordnet.NOUN # NN, NNP, NNS


def get_lemmatized_word(word, tag): 
    return lemmatize(word, pos=get_parsed_pos_tag(tag))


def get_all_pos_tagged_words(text):
    return pos_tag_text(text.split())


def get_lemmatized_text(text):
    # return " ".join([get_lemmatized_word(word, tag) for word, tag in get_all_pos_tagged_words(text)])
    return " ".join([lemmatize(word) for word in text.split()])


def get_tokenized_text(text):
    return " ".join(tokenize(text))


def normalize(word):
    return ''.join(word.split())


def if_is_an_emoji_or_emoticon_parse_it(word):
    if word in set(emojis_emoticon.keys()):
        return normalize(emojis_emoticon[word])
    else:
        return word


def get_text_whit_emojis_and_emoticon_parsed(text):  
    return " ".join([if_is_an_emoji_or_emoticon_parse_it(word) for word in text.split()])


def get_text_whit_corrected_misspelled_words(text):
    return " ".join([get_correct_word_if_it_is_mispelled(word) for word in text.split()])


def is_the_word_correct(word):
    return word in all_english_words


def get_text_whitout_uncorrect_words(text):
    return " ".join([word for word in text.split() if is_the_word_correct(word)])


def get_text_whitout_stopwords(text):
    return " ".join([word for word in text.split() if word not in english_stopwords])


def get_text_whitout_links_and_urls(text):
    return " ".join([word for word in text.split() if 'http' not in word and 'www.' not in word])


def get_text_whitout_hashtag_and_mentions(text):
    return " ".join([word for word in text.split() if '#' not in word and '@' not in word])


def get_text_whitout_punctuation(text):
    return text.translate(str.maketrans('', '', punctuation))
    # return text.translate(str.maketrans('', '', tweet_useless_punctuation))


def get_normalized_text(text):
    text = get_tokenized_text(text)
    text = get_text_whitout_links_and_urls(text)
    text = get_text_whitout_hashtag_and_mentions(text)
    text = get_text_whitout_punctuation(text)
    text = get_text_whit_emojis_and_emoticon_parsed(text)
    # text = get_text_whit_corrected_misspelled_words(text)
    text = get_text_whitout_uncorrect_words(text)
    text = get_text_whitout_stopwords(text)
    text = get_lemmatized_text(text)
    # text = get_stemmed_text(text)

    return text


def get_created_at(tweet):
    return tweet[3]


def get_lang(tweet):
    return tweet[2]


def get_politician_name(tweet):
    return tweet[0]


def get_text(tweet):
    return tweet[1].lower()


def preprocess_tweets(tweets):
    start = time.clock()

    normalized_tweets = [(get_politician_name(tweet), 
                         get_normalized_text(get_text(tweet)), 
                         get_lang(tweet), 
                         get_created_at(tweet), 
                         ) 
                         for tweet in tweets.values.tolist()]

    normalized_tweets = {tweet for tweet in normalized_tweets if get_text(tweet) != ""}
    
    print(len(normalized_tweets))
    
    total_execution_time = (time.clock() - start) / 60
    print("total: " + str(total_execution_time) + " minute")    

    normalized_tweets = pd.DataFrame(normalized_tweets, columns=["politician_name", "text", "original_text_lang", "created_at"])

    desidered_path = os.getcwd() + '/political_analysis/predict_data/political_tweets_preprocessed.csv'
    normalized_tweets.to_csv(desidered_path, index=False)



#################################################################################################################
#                                                ______
#                                               | MAIN |
#                                                 
#################################################################################################################



tweets = pd.read_csv('political_analysis/preprocess_data/tweets.csv')

preprocess_tweets(tweets)