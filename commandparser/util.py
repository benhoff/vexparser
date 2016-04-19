import os as _os
import nltk as _nltk

if not "stopwords" in _os.listdir(_nltk.data.find("corpora")):
    _nltk.download("stopwords")


from nltk.corpus import stopwords
stopwords = set(stopwords.words('english'))
