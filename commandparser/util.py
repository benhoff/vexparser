import os as _os
import nltk as _nltk
import unicodedata
import sys

_tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                     if unicodedata.category(chr(i)).startswith('P'))

if not "stopwords" in _os.listdir(_nltk.data.find("corpora")):
    _nltk.download("stopwords")


from nltk.corpus import stopwords as stopwords


_stopwords = dict.fromkeys(s for s in set(stopwords.words('english')))


def clean_text(str):
    # get rid of the puncuation
    str = str.translate(_tbl)
    # get rid of the stopwords
    str = str.translate(_stopwords)
    # lowercase everything
    str.lower()
    return str
