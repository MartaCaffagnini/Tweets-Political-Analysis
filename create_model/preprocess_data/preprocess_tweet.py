import pandas as pd
from string import punctuation
import time
import os

from nltk.corpus import words as all_english_words
from nltk import WordNetLemmatizer
from nltk.tokenize import TweetTokenizer 
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk import pos_tag as pos_tag_text

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

all_english_words = set(all_english_words.words())

emojis_emoticon = dict(pd.read_csv('emoji_emoticon.csv').values.tolist())


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


def get_text_whit_emojis_and_emoticons_parsed(text):  
    return " ".join([if_is_an_emoji_or_emoticon_parse_it(word) for word in text.split()])


def get_text_whit_corrected_misspelled_words(text):
    return " ".join([get_correct_word_if_it_is_mispelled(word) for word in text.split()])


def get_text_whitout_uncorrect_words(text):
    return " ".join([word for word in text.split() if  word in all_english_words])


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
    text = get_text_whit_emojis_and_emoticons_parsed(text)
    text = get_text_whitout_punctuation(text)
    # text = get_text_whit_corrected_misspelled_words(text)
    text = get_text_whitout_uncorrect_words(text)
    text = get_text_whitout_stopwords(text)
    text = get_lemmatized_text(text)

    return text


def get_label(tweet):
    return tweet[0]


def get_text(tweet):
    return tweet[1].lower()


def preprocess_tweets(tweets):
    tweets = tweets.values.tolist()

    start = time.clock()

    normalized_tweets = [(get_label(tweet), get_normalized_text(get_text(tweet))) for tweet in tweets]

    normalized_tweets = [tweet for tweet in normalized_tweets if get_text(tweet) != ""]
    
    total_execution_time = (time.clock() - start) / 60
    print("total: " + str(total_execution_time) + " minute")    

    normalized_tweets = pd.DataFrame(set(normalized_tweets), columns=["label", "text"])

    os.chdir("..")
    desidered_path = os.getcwd() + '/get_model/preprocessed_training.csv'
    normalized_tweets.to_csv(desidered_path, index=False)


#################################################################################################################
#                                                ______
#                                               | MAIN |
#                                                 
#################################################################################################################



tweets = pd.read_csv('training.csv')

preprocess_tweets(tweets)