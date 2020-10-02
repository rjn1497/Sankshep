from .preprocessing import preprocess
from scoring import get_sentence_ranks
from functools import lru_cache

@lru_cache(maxsize=100)
def Summary(
    text: str, percentage: float=None,
    abstractive: bool=False
    ) -> str:
    """
    Returns a summary of original text.

    Input(s):
    1) text - Original text to be summarized.
    2) percentage - Optional argument; Percentage by which text is to be
                    summarized.
    3) abstractive - Optional argument; wether abstractive summarization to
                     be used or not.

    Output(s):
    1) summary - A summary of the text provided.
    """

    paragraphs, sentences, tokens, tokens_by_sentence = preprocess(text)
    ranked_sents = get_sentence_ranks(sentences, 
        tokens_by_sentence, 
        paragraphs, 
        tokens)

    summary = ""
    if percentage:
        count = 100 - float(percentage)
        count = round(len(ranked_sents) * (count/100.0))
        count = 1 if (count < 1) else count
        
        for c in range(count):
            summary += f"{ranked_sents[c][1]} "
    else:
        threshold = sum([sc for (sc, sent) in ranked_sents])/len(ranked_sents)
        for sent in ranked_sents:
            if sent[0] > threshold:
                summary += f"{sent[1]} "
        percentage = 100 - ((len(summary)/len(text)) * 100)

    return summary.strip(), percentage