import os
import argparse

import yaml

from commandparser.classification_parser import ClassifyParser
from commandparser.messaging import Messaging
import commandparser.util as util


def _return_closure(text):
    def _inner_function():
        return text
    return _inner_function


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
        data = [(util.clean_text(d), intent_name) for d in intent_data['data']]
        training_data.extend(data)

    classifier = ClassifyParser(training_data)

    for intent_name, intent_data in all_intent_data.items():
        response = None
        try:
            response = intent_data['response']
            classifier.associate_label_with_action(intent_name,
                                                   _return_closure(response))

        except KeyError:
            pass

        probability = intent_data['probability']
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
