from os.path import dirname, abspath, isfile
from itertools import groupby
from re import compile, match
from tinydb import TinyDB
from Lemmatizer import get_character_ngrams


parent_directory = dirname(dirname(dirname(abspath(__file__))))
raw_lemmas_path = parent_directory + "/resources/raw_lemmas.txt"
db_path = parent_directory + "/resources/lemmas.json"

LETTERS = [
    'अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ऍ', 'ए', 'ऐ', 'ऑ', 'ओ',
    'औ', 'क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ', 'ट', 
    'ठ', 'ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न', 'प', 'फ', 'ब', 'भ', 
    'म', 'य', 'र', 'ल', 'व', 'श', 'ष', 'स', 'ह'
    ]

with open(raw_lemmas_path, encoding="utf-16") as f:
    raw_lemmas = f.read()
raw_lemmas = list(map(lambda x: x.strip(), raw_lemmas.split("\n")))
exp = compile("(?!.+\s+.+)|(?!(^-.+))|.+-.+")
raw_lemmas = list(filter(exp.match, raw_lemmas))

f = lambda x: x[0]
raw_lemmas = sorted(raw_lemmas, key=f)
raw_lemmas = [list(ele) for i, ele in groupby(raw_lemmas, f)]
raw_lemmas.pop(0)

if not isfile(db_path):
    with open(db_path, "w+") as f:
        pass

db = TinyDB(db_path)

def segregate_into_documents(raw_lemmas, letters):
    documents = [
        {"letter": letters[l], 
        "words": {
            word: get_character_ngrams(word, 2) 
            for word in raw_lemmas[l]}} 
        for l in range(len(letters))
        ]
    return documents


def write_to_db(document_list):
    for doc in document_list:
        db.insert(doc)

documents = segregate_into_documents(raw_lemmas, LETTERS)
write_to_db(documents)