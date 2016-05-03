from gensim import corpora, models

from vexparser.util import clean_text

class TopicParser:
    def __init__(self, training_data, number_topics: int):
        self.callback_managers = []
        self.dictionary = corpora.Dictionary(training_data)
        corpus = [self.dictionary.doc2bow(text) for text in training_data]
        self.model = models.LdaModel(corpus,
                                     num_topics=number_topics,
                                     id2word=self.dictionary,
                                     # TODO: look up what this is
                                     passes=20)

        print(self.model.show_topics())

    def parse(self, text):
        text = clean_text(text)
        print(text)
        split_text = text.split()
        doc_bow = self.dictionary.doc2bow(split_text)
        text_lda = self.model[doc_bow]
        print(text_lda, text)


    def add_callback_manager(self, manager):
        self.callback_managers.append(manager)

    def remove_callback_manager(self, manager):
        self.callback_managers.remove(manager)
