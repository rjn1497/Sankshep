from os.path import dirname, abspath
from typing import List

parent_directory = dirname(dirname(abspath(__file__)))
lemmas_path = "/resources/lemmas.json"

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

def lemmatize(tokens: List[str]):
    """
    Accepts a list of tokens and returns a list containg
    lemmas of those tokens.

    Input(s):
    1) tokens - A list containg tokens to be lemmatized.

    Output(s):
    """