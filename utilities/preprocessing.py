from os.path import abspath, dirname
from re import split
from itertools import chain
from typing import List

"""
TODO: 1) lemmatization
      2) improve tokenization
"""      

parent_directory = dirname(dirname(abspath(__file__)))
stopwords_path = parent_directory + "/resources/hindi_stopwords.txt"
with open(stopwords_path) as f:
    hindi_stopwords = f.read()

SentTok = List[str]

def get_sentences(text: str):
    return split(r'[\|।॥!\?]', text)

def get_tokens(text: str):
    sentences = get_sentences(text)
    tokens = []
    for line in sentences:
        temp = split(r'[\s,;]', line)
        tokens.append(temp)
    return tokens, list(chain.from_iterable(tokens))

def clean(tokens: List[str]):
    unique_tokens = list(set(tokens))
    for word in unique_tokens:
        if word in hindi_stopwords:
            unique_tokens.pop(word)
    return unique_tokens

def lemmatize_tokens(tokens: List[str]=None, tokens_per_sentence: List[SentTok]=None):
    #in progress
    if tokens:
        pass
    if tokens_per_sentence:
        pass
    return lemmatized_tokens

def preprocess(text: str):
    sentences = split_sentences(text)
    tokens_per_sentence, original_tokens = get_tokens(text)
    
    cleaned_tokens = clean(original_tokens)

    lemmatized_tokens = lemmatize(cleaned_tokens)
    lemmatized_token_sentences = lemmatize(tokens_per_sentence) #polymorphic function

    return sentences, lemmatized_tokens, lemmatized_token_sentences