import os
import argparse

import yaml
from zmq import ZMQError

from vexparser.classification_parser import ClassifyParser
from vexparser.mark_parser import MarkParser
from vexparser.messaging import Messaging
from vexparser.callback_manager import CallbackManager
import vexparser.util as util


def _return_closure(text):
    def _inner_function():
        return text
    return _inner_function


def main(**kwargs):
    # FIXME
    if not kwargs:
        kwargs = _get_kwargs()

    data_file = kwargs['settings_path']
    with open(data_file) as f:
        file_data = yaml.load(f)

    all_intent_data = file_data.pop('intents')
    training_data = []

    for intent_name, intent_data in all_intent_data.items():
        # this adds the training data with the intent name
        data = [(util.clean_text(d), intent_name) for d in intent_data['data']]
        training_data.extend(data)

    classify_parser = ClassifyParser(training_data)
    mark_parser = MarkParser()

    parsers = [classify_parser, mark_parser]
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

        except KeyError:
            pass

        probability = intent_data['probability']
        classify_parser.define_minimum_probability_for_action(intent_name,
                                                              probability)

    parsers = [mark_parser, classify_parser]

    already_running = False

    # FIXME
    try:
        messaging = Messaging(parsers, **file_data)
        messaging.run()
    except ZMQError:
        pass



def _get_kwargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--settings_path',
                        action='store')

    return vars(parser.parse_args())

if __name__ == '__main__':
    main()
