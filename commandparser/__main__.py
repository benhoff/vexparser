import os
import argparse

import yaml

from commandparser.classification_parser import ClassifyParser
from commandparser.messaging import Messaging
from commandparser.util import stopwords


def _return_closure(text):
    def _inner_function():
        return text
    return _inner_function


def _clean_text(data: list,
                intent: str):

    result = []
    for d in data:
        # splits the string into a list based on whitespace
        word_list = d.split()
        # removes caps and all stop words
        word_list = [w.lower() for w in word_list if w not in stopwords]
        # join the list back into a single sentence w/ whitespace and intent
        result.append((" ".join(word_list), intent))

    return result


def main(**kwargs):
    # FIXME
    if not kwargs:
        kwargs = _get_kwargs()

    data_file = kwargs['data_file']
    with open(data_file) as f:
        file_data = yaml.load(f)

    intent_data = file_data.pop('intents')
    training_data = []

    for intent_name, data in intent_data.items():
        # this adds the training data with the intent name
        training_data.extend(_clean_text(data['data'], intent_name))

    classifier = ClassifyParser(training_data)

    for intent_name, data in intent_data.items():
        response = None
        try:
            response = data['response']
            classifier.associate_label_with_action(intent_name,
                                                   _return_closure(response))

        except KeyError:
            pass

        probability = data['probability']
        classifier.define_minimum_probability_for_action(intent_name,
                                                         probability)

    messaging = Messaging(classifier, **file_data)
    messaging.run()


def _get_kwargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', action='store')

    return vars(parser.parse_args())

if __name__ == '__main__':
    main()
