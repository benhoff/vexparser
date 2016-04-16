import argparse

import yaml

from commandparser.classification_parser import ClassifyParser
from commandparser.messaging import Messaging

def _return_closure(text):
    def _inner_function():
        return text
    return _inner_function



def main():
    kwargs = _get_kwargs()
    data_file = kwargs['data_file']
    with open(data_file) as f:
        file_data = yaml.load(f)

    training_data = []

    intent_data = file_data.pop('intents')

    for intent_name, data in intent_data.items():
        # this adds the training data with the intent name
        training_data.extend([(d, intent_name) for d in data['data']])
        # NOTE: filters unimplemented
        filter = data['filter']

    # TODO: create and apply a common word filter
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
