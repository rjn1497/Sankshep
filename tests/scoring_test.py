import pytest

class ScoringTest:
    raw_sentences = []
    para_list = []
    grouped_tokens = []
    tokens = []

    def test_get_tf(self):
        freq_dict = {}

        assert freq_dict == get_tf(tokens)

    def test_get_idf(self):
        idf_dict = {}

        assert idf_dict == get_idf(para_list, tokens)

    def test_get_sentence_ranks(self):
        ranked_sents = [(), ()]

        assert ranked_sents == get_sentence_ranks()