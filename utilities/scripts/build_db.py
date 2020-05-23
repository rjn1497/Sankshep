from os.path import dirname, abspath, isfile
from re import match
from tinydb import TinyDB, Query
from Lemmatizer import get_character_ngrams


parent_directory = dirname(dirname(dirname(abspath(__file__))))
raw_lemmas_path = parent_directory + "/resources/raw_lemmas.txt"
db_path = parent_directory + "/resources/lemmas.json"

with open(raw_lemmas_path, encoding="utf-16") as f:
    raw_lemmas = f.read()
raw_lemmas = raw_lemmas.split("\n")

for lemma in raw_lemmas:
    if match(r".+\s.+", lemma):
        raw_lemmas.remove(lemma)


if not isfile(db_path):
    with open(db_path, "w+") as f:
        pass

db = TinyDB(db_path)

def get_letters(source):
    letters = []
    for word in source:
        if word[0] not in letters:
            source.append(word[0])

    return letters

def segregate_into_documents(raw_lemmas, letters):
    documents = {l: {} for l in letters}
    for lemma in raw_lemmas:
        init = lemma[0]
        if lemma not in documents[init]:
            documents[lemma[0]][lemma] = get_character_ngrams(lemma, 2)

    return documents


def write_to_db(document_dict, letters):
    for l in letters:
        db.insert({"letter": l,
            "words": document_dict[l]})

LETTERS = get_letters(raw_lemmas)
print("letters fetched")
print(LETTERS)
#documents = segregate_into_documents(raw_lemmas, LETTERS)
#write_to_db(documents, LETTERS)