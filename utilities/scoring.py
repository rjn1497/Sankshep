from typing import List, Dict, Tuple
from collections import Counter
from math import log


SentList = List[str]

def get_tf(sentences: List[SentList]) -> Dict[str, float]:
    """
    Returns a dictionary containing the (normalised frequencies) of all
    tokens in source text.

    Input(s):
    1) sentences - List of tokens grouped by sentence.

    Output(s):
    1) frequencies - Dictionary containing normalised frequency of all 
                     tokens .
    """

    sentences = sum(sentences, [])
    frequencies = dict(Counter(sentences))
    max_freq = max(frequencies.values())
    frequencies = {token: float(freq)/max_freq
     for (token, freq) in frequencies.items()}

    return frequencies

def get_idf(paragraphs: List[str], tokens: List[str]) -> Dict[str, float]:
    """
    Returns a dictionary containing the Inverse Document Freqeuencies
    of all tokens in the original text.

    Input(s):
    1) paragraphs - List containing all paragraphs.
    2) tokens - List containing all unique, important tokens.

    Output(s):
    1) idf_dict - Dictionary containing idfs of all tokens.
    """

    documents = len(paragraphs)
    #idf_dict = {token:
    # log(float(documents)/len([token[0] in para for para in paragraphs]))
    # for token in tokens}
    idf_dict = {}
    for token in tokens:
        c = 1
        for para in paragraphs:
            if token[0] in para:
                c += 1
            idf_dict[token] = log(documents/float(c))

    return idf_dict

def get_sentence_ranks(sentences: List[str], 
    tokens_per_sentence: List[SentList], 
    paragraphs: List[str], 
    tokens: List[str]) -> List[Tuple[int, str]]:
    """
    Returns a list of sentences, ordered by importance.

    Input(s):
    1) sentences - List of all sentences.
    2) tokens_per_sentence - 2d List containing tokens grouped
                             by sentence.
    3) paragraphs - List of all paragraphs.
    4) tokens - List of all unique, important tokens.

    Output(s):
    1) sentences - List containing sentences and their ranks (as tuples)
                   sorted in descending order by rank.
    """

    tf = get_tf(tokens_per_sentence)
    idf = get_idf(paragraphs, tokens)

    ranks = []
    for sent in range(len(sentences)):
        score = 0
        for token in tokens_per_sentence[sent]:
            if token in tokens:
                score += tf[token] * idf[token]
        ranks.append(score)

    sentences = sorted(list(zip(ranks, sentences)), reverse=True)

    return sentences