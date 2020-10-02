from os.path import dirname, abspath
from tinydb import TinyDB, where
from typing import List
from distance import levenshtein
from jellyfish import jaro_winkler_similarity
from functools import lru_cache

parent_directory = dirname(dirname(dirname(abspath(__file__))))
lemmas_path = parent_directory + "/resources/lemmas.json"

db = TinyDB(lemmas_path)

@lru_cache(maxsize=300)
def get_character_ngrams(token: str, n: int):
    """
    Returns character n-grams for given words.

    Input(s):
    1) token - The word to be used for generating
               n-gram.
    2) n - Size of n-gram

    Output(s):
    1) A list containing character n-grams.
    """

    return [token[char:char+n] for char in range(len(token)-n+1)]

def similarity(set1: List[str], set2: List[str]):
    """
    Returns the similarity of two sets using Dice's Coeffcient
    Formula.

    Dice's Coefficient Formula:
    d = (2nt) / (nx + ny)
    where, nt = number of character bigrams common to both strings
           nx = number of character bigrams in string x
           ny = number of character bigrams in string y

    Input(s):
    1) set1 - First set to be compared.
    2) set2 - Second set to be compared.

    Output(s):
    1) score - Tells us how similar two sets are (1.0 being highest i.e.
               both sets are the same).
    """

    len1 = len(set1)
    len2 = len(set2)

    set1.sort()
    set2.sort()

    if not len1 or not len2:
        return 0.0

    if len1 == 1 or len2 == 1:
        return 0.0

    if set1 == set2:
        return 1.0

    matches = i = j = 0
    while (i < len1 and j < len2):
        if set1[i] == set2[j]:
            matches += 2
            i += 1
            j += 1
        elif set1[i] < set2[j]:
            i += 1
        else:
            j += 1

    score = float(2 * matches)/float(len1 + len2)

    return score

@lru_cache(maxsize=300)
def get_distance(str1: str, str2: str) -> int:
    """
    Uses Levenshtein Distance
    str1 - token to be lemmatized
    str2 - lemma from dictionary
    """
    if (len(str2) > len(str1)):
        return -1

    return levenshtein(str1, str2)

@lru_cache(maxsize=300)
def generate_stem_words(word):
        suffixes = {
        1: [u"ो",u"े",u"ू",u"ु",u"ी",u"ि",u"ा"],
        2: [u"कर",u"ाओ",u"िए",u"ाई",u"ाए",u"ने",u"नी",u"ना",u"ते",u"ीं",u"ती",u"ता",u"ाँ",u"ां",u"ों",u"ें"],
        3: [u"ाकर",u"ाइए",u"ाईं",u"ाया",u"ेगी",u"ेगा",u"ोगी",u"ोगे",u"ाने",u"ाना",u"ाते",u"ाती",u"ाता",u"तीं",u"ाओं",u"ाएं",u"ुओं",u"ुएं",u"ुआं"],
        4: [u"ाएगी",u"ाएगा",u"ाओगी",u"ाओगे",u"एंगी",u"ेंगी",u"एंगे",u"ेंगे",u"ूंगी",u"ूंगा",u"ातीं",u"नाओं",u"नाएं",u"ताओं",u"ताएं",u"ियाँ",u"ियों",u"ियां"],
        5: [u"ाएंगी",u"ाएंगे",u"ाऊंगी",u"ाऊंगा",u"ाइयाँ",u"ाइयों",u"ाइयां"],
        }
        for L in 5, 4, 3, 2, 1:
            if len(word) > L + 1:
                for suf in suffixes[L]:
                    #print type(suf),type(word),word,suf
                    if word.endswith(suf):
                        #print 'h'
                        return word[:-L]
        return word


def lemmatize(tokens: List[str]):
    """
    Accepts a list of tokens and returns a list containg
    lemmas of those tokens.

    Input(s):
    1) tokens - A list containg tokens to be lemmatized.

    Output(s):
    1) lemma_list - A list containing lemmas of tokens for which
                    lemmas could be found and the tokens themselves
                    for which no lemmas were found.
    """

    lemma_list = []
    for token in tokens:
        bigrams = get_character_ngrams(generate_stem_words(token), 2)
        options = db.search(where('letter') == token[0])
        options = options[0] if options else options
        similarity_score = len(token)

        if options:
            if token in options["words"]:
                lemma_list.append(token)
            else:
                candidates = []
                for lemma in options["words"]:
                    temp = get_distance(token, lemma)
                    if (temp != -1) and (temp <= similarity_score):
                        similarity_score = temp
                        candidates.append(lemma)
                    else:
                        pass
                similarity_score = 0.0
                jw_similarity_score = 0.0
                add = ""
                for i in candidates:
                    cand_big = options["words"][i]
                    temp = similarity(bigrams, cand_big)
                    temp_jw = jaro_winkler_similarity(token, i)
                    if (temp > similarity_score) and (temp_jw > jw_similarity_score):
                        similarity_score = temp
                        jw_similarity_score = temp_jw
                        add = i
                if round(similarity_score) == 1:
                    lemma_list.append(add)  
                else:
                    lemma_list.append(token)      
        else:
            lemma_list.append(token)

    return list(zip(tokens, lemma_list))