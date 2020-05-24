import pytest
from os.path import dirname, abspath
import sys
sys.path.insert(1, dirname(dirname(abspath(__file__))))
from utilities.preprocessing import *


class PreprocessingTest:
    source_text_1 = ""
    source_text_2 = ""
    raw_tokens = []

    def test_get_paragraphs(self):
        para_list_1 = []
        para_list_2 = []

        assert para_list_1 == get_paragraphs(source_text_1)
        assert para_list_2 == get_paragraphs(source_text_2)

    def test_get_sentences(self):
        sentence_list_1 = []
        sentence_list_2 = []

        assert sentence_list_1 == get_sentences(source_text_1)
        assert sentence_list_2 == get_sentences(source_text_2)

    def test_get_tokens(self):
        token_list_1 = []
        token_list_2 = []

        assert token_list_1 == get_tokens(source_text_1)
        assert token_list_2 == get_tokens(source_text_2)

    def test_clean(self):
        clean_tokens = []

        assert clean_tokens == clean(raw_tokens)
