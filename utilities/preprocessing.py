from os.path import abspath, dirname
from re import split
from typing import List
import scripts.Lemmatizer as lt


parent_directory = dirname(dirname(abspath(__file__)))
stopwords_path = parent_directory + "/resources/hindi_stopwords.txt"
with open(stopwords_path) as f:
    hindi_stopwords = f.read()
    hindi_stopwords = hindi_stopwords.split("\n")
"""
fix stopwords
['म', 'मझको', 'मरा', 'अपन आप को', 'हमन', 'हमारा', 'अपना', 'हम', 'आप', 'आपका', 'तम्हारा', 'अपन आप',
'स्वय', 'वह', 'इस', 'उसक', 'खद को', 'कि वह', 'उसकी', 'उसका', 'खद ही', 'यह', 'इसक', 'उन्होन', 'अपन',
'क्या', 'जो', 'किस', 'किसको', 'कि', 'य', 'ह', 'होता ह', 'रह', 'थी', 'थ', 'होना', 'गया', 'किया जा रहा ह', 
'किया ह', 'ह', 'पडा', 'होन', 'करना', 'करता ह', 'किया', 'रही', 'एक', 'लकिन', 'अगर', 'या', 'क्यकि', 'जसा', 
'जब तक', 'जबकि', 'की', 'पर', 'द्वारा', 'क लिए', 'साथ', 'क बार म', 'खिलाफ', 'बीच', 'म', 'क माध्यम स', 
'दौरान', 'स पहल', 'क बाद', 'ऊपर', 'नीच', 'को', 'स', 'तक', 'स नीच', 'करन म', 'निकल', 'बद', 'स अधिक', 
'तहत', 'दबारा', 'आग', 'फिर', 'एक बार', 'यहा', 'वहा', 'कब', 'कहा', 'क्यो', 'कस', 'सार', 'किसी', 'दोनो', 
'प्रत्यक', 'ज्यादा', 'अधिकाश', 'अन्य', 'म कछ', 'ऐसा', 'म कोई', 'मात्र', 'खद', 'समान', 'इसलिए', 'बहत', 
'सकता', 'जायग', 'जरा', 'चाहिए', 'अभी', 'और', 'कर दिया', 'रख', 'का', 'ह', 'इस', 'होता', 'करन', 'न', 
'बनी', 'तो', 'ही', 'हो', 'इसका', 'था', 'हआ', 'वाल', 'बाद', 'लिए', 'सकत', 'इसम', 'दो', 'व', 'करत', 'कहा', 
'वर्ग', 'कई', 'कर', 'होती', 'अपनी', 'उनक', 'यदि', 'हई', 'जा', 'कहत', 'जब', 'होत', 'कोई', 'हए', 'व', 'जस', 
'सभी', 'करता', 'उनकी', 'तरह', 'उस', 'आदि', 'इसकी', 'उनका', 'इसी', 'प', 'तथा', 'भी', 'परत', 'इन', 'कम', 
'दर', 'पर', 'गय', 'तम', 'म', 'यहा', 'हय', 'कभी', 'अथवा', 'गयी', 'प्रति', 'जाता', 'इन्ह', 'गई', 'अब', 'जिसम', 
'लिया', 'बड़ा', 'जाती', 'तब', 'उस', 'जात', 'लकर', 'बड़', 'दसर', 'जान', 'बाहर', 'स्थान', 'उन्ह ', 'गए', 'ऐस', 'जिसस', 
'समय', 'दोनो', 'किए', 'रहती', 'इनक', 'इनका', 'इनकी', 'सकती', 'आज', 'कल', 'जिन्ह', 'जिन्हो', 'तिन्ह', 'तिन्हो', 'किन्हो', 
'किन्ह', 'इत्यादि', 'इन्हो', 'उन्हो', 'बिलकल', 'निहायत', 'इन्ही', 'उन्ही', 'जितना', 'दसरा', 'कितना', 'साबत', 'वग़रह', 'कौनसा', 
'लिय', 'दिया', 'जिस', 'तिस', 'काफ़ी', 'पहल', 'बाला', 'मानो', 'अदर', 'भीतर', 'परा', 'सारा', 'उनको', 'वही', 'जहा', 'जीधर', 
'\ufeffक', 'एव', 'कछ', 'कल', 'रहा', 'जिस', 'जिन', 'तिस', 'तिन', 'कौन', 'किस', 'सग', 'यही', 'बी', 'उसी', 
'मगर', 'कर', 'म', 'एस', 'उन', 'सो', 'अत', '']

Entire phrases showing up
possible fix => use re to search phrases within source text and substitute with null character ""
"""
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