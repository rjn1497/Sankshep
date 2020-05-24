from os.path import abspath, dirname
from re import split
from typing import List
import sys
sys.path.insert(1, dirname(abspath(__file__)))
import scripts.Lemmatizer as lt


parent_directory = dirname(dirname(abspath(__file__)))
stopwords_path = parent_directory + "/resources/hindi_stopwords.txt"
with open(stopwords_path) as f:
    hindi_stopwords = f.read()
    hindi_stopwords = hindi_stopwords.split("\n")

SentTok = List[str]

def get_paragraphs(text: str):
    """
    Returns a list containing all paragraphs.

    Input(s):
    1) text - Original source text.

    Output(s):
    1) paragraphs - List containing all paragraphs.
    """

    paragraphs = text.splitlines()
    paragraphs = list(filter(lambda y: y != "", 
        list(map(lambda x: x.strip(), 
            paragraphs))))

    return paragraphs

def get_sentences(text: str):
    """
    Returns a list of sentences in source text.

    Input(s):
    1) text - Original source text.

    Output(s):
    1) sentences - List of all sentences in original text.
    """

    sentences = list(map(lambda x: x.strip(), split(r'[\|।॥!\?]', text)))

    return [i for i in sentences if i != '']

def get_tokens(text: str):
    """
    Returns all tokens from text.

    Input(s):
    1) text - Original source text.

    Output(s):
    1) tokens - List containing all tokens grouped by sentences.
    2) List containing all tokens.
    """

    sentences = get_sentences(text)
    tokens = []
    for line in sentences:
        temp = split(r'[\s,;]', line)
        tokens.append(temp)

    return tokens, sum(tokens, [])

def clean(tokens: List[str]):
    """
    Returns a list of unique tokens without any stopwords.

    Input(s):
    1) tokens - List containing all tokens.

    Output(s):
    1) unique_tokens - List of unique tokens with all stopwords
                       removed.
    """

    # handle alphanumeric strings

    unique_tokens = list(set(tokens))
    for word in unique_tokens:
        if word in hindi_stopwords:
            unique_tokens.pop(word)

    return unique_tokens

def lemmatize_tokens(tokens: List[str]=None, tokens_per_sentence: List[SentTok]=None):
    """
    Lemmatizes tokens.

    Input(s):
    1) tokens - Optional argument; Contains a 1d list of tokens.
    2) tokens_per_sentence - Optional argument; Contains a 2d list of all
                             tokens grouped by sentence.

    Output(s):
    1) Lemmas: Either a 1d list containing all Lemmas or a 2d list
               containing Lemmas grouped by sentence.
    """

    Lemmas = []
    if tokens:
        Lemmas.append(lt.lemmatize(tokens))
    if tokens_per_sentence:
        for sentence in toketokens_per_sentence:
            Lemmas.append(lt.lemmatize(sentence))

    return Lemmas

def preprocess(text: str):
    """
    Handles all the preprocessing required for ranking and scoring.

    Argument(s):
    1) text - The original body of text.

    Output(s):
    1) paragraphs - List of all paragraphs in original text.
    2) sentences - List of all sentences in original text.
    3) lemmatized_tokens - All unique, lemmatized tokens without
                           any stopwords.
    4) lemmatized_token_sentences - All unique, lemmatized tokens,
                                    grouped by sentence.
    """

    paragraphs = get_paragraphs(text)

    sentences = get_sentences(text)
    tokens_per_sentence, original_tokens = get_tokens(text)
    
    cleaned_tokens = clean(original_tokens)

    lemmatized_tokens = lemmatize(cleaned_tokens)
    lemmatized_token_sentences = lemmatize(tokens_per_sentence)

    return paragraphs, sentences, lemmatized_tokens, lemmatized_token_sentences