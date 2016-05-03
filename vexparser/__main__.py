import os
import argparse

from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
import yaml

from vexparser.topic_parser import TopicParser
from vexparser.classification_parser import ClassifyParser
from vexparser.mark_parser import MarkParser
from vexparser.messaging import Messaging
from vexparser.callback_manager import CallbackManager
import vexparser.util as util


stop_words = get_stop_words('en')


def _return_closure(text):
    def _inner_function():
        return text
    return _inner_function


def _register_aliases(intent_data, text_return_callback, callback_manager):
    try:
        aliases = intent_data['aliases']
        for alias in aliases:
            callback_manager.associate_key_with_callback(alias,
                                                         text_return_callback)

    except KeyError:
        pass


def _topic_parser_clean_data(training_data):
    results = []
    porter_stemmer = PorterStemmer()
    for data in training_data:
        split_data = data.split()
        # FIXME
        stopped_words = [w for w in split_data if not w in stop_words]
        # stemmed_data = [porter_stemmer.stem(word) for word in stopped_words]
        results.append(stopped_words)

    return results


def main(**kwargs):
    # FIXME
    if not kwargs:
        kwargs = _get_kwargs()

    data_file = kwargs['data_file']
    with open(data_file) as f:
        file_data = yaml.load(f)

    all_intent_data = file_data.pop('intents')
    training_data = []

    for intent_name, intent_data in all_intent_data.items():
        # this adds the training data with the intent name
        # data = [(util.clean_text(d), intent_name) for d in intent_data['data']]
        data = [util.clean_text(d) for d in intent_data['data']]
        training_data.extend(data)

    # NOTE: training data changed below. Don't get comfy
    # classify_parser = ClassifyParser(training_data)
    mark_parser = MarkParser()

    # clean up the data to be how topic parser expects it
    training_data = _topic_parser_clean_data(training_data)
    # get the number of topics
    number_of_topics = len(all_intent_data)
    # create the topics
    topic_parser = TopicParser(training_data, number_of_topics)

    # parsers = [topic_parser, classify_parser, mark_parser]
    parsers = [topic_parser, mark_parser]
    callback_manager = CallbackManager()

    for parser in parsers:
        # register the callback manager with the parsers
        parser.add_callback_manager(callback_manager)

    for intent_name, intent_data in all_intent_data.items():
        response = None
        try:
            response = intent_data['response']
            text_return_callback = _return_closure(response)

            callback_manager.associate_key_with_callback(intent_name,
                                                         text_return_callback)

            _register_aliases(intent_data,
                              text_return_callback,
                              callback_manager)


        except KeyError:
            pass

        probability = intent_data['probability']
        # classify_parser.define_minimum_probability_for_action(intent_name,
        #                                                       probability)

    messaging = Messaging(parsers, **file_data)

    messaging.run()


def _get_kwargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', action='store')

    return vars(parser.parse_args())

if __name__ == '__main__':
    main()
