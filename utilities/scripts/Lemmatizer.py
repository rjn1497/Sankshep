from os.path import dirname, abspath
from tinydb import TinyDB, where
from typing import List


parent_directory = dirname(dirname(abspath(__file__)))
lemmas_path = parent_directory + "/resources/lemmas.json"

db = TinyDB('lemmas_path')

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
        bigrams = get_character_ngrams(token, 2)
        options = db.search(where('letter') == token[0])
        options = options[0] if options else options

        if options:
            if token in options["words"]:
                lemma_list.append(token)
            else:
                similarity_score = 0.0
                for lemma in options["words"]:
                    temp = similarity(bigrams, lemma["bigrams"])
                    similarity_score = temp if (temp > similarity_score) else similarity_score
    
                if round(similarity_score):
                    lemma_list.append(lemma)
                else:
                    lemma_list.append(token)
        else:
            lemma_list.append(token)

        return lemma_list