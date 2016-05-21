import unicodedata as _unicodedata
import sys as _sys

from nltk.corpus import stopwords as stopwords
"""
if not "stopwords" in _os.listdir(_nltk.data.find("corpora")):
    _nltk.download("stopwords")
"""

_tbl = None
_stopwords = None


def _get_stopwords():
    global _tbl, _stopwords
    _tbl = dict.fromkeys(i for i in range(_sys.maxunicode)
                         if _unicodedata.category(chr(i)).startswith('P'))

    _stopwords = dict.fromkeys(s for s in set(stopwords.words('english')))


def clean_text(str):
    if _tbl is None or _stopwords is None:
        _get_stopwords()

    # get rid of the puncuation
    str = str.translate(_tbl)
    # get rid of the stopwords
    str = str.translate(_stopwords)
    # lowercase everything
    str.lower()
    return str
