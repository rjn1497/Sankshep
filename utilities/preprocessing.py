from os.path import abspath, dirname

parent_directory = dirname(dirname(abspath(__file__)))
stopwords_path = parent_directory + "/resources/hindi_stopwords.txt"
with open(stopwords_path) as f:
    hindi_stopwords = f.read()


def clean(tokens):
    for word in tokens:
        if word in hindi_stopwords:
            tokens.pop(word)
