from textblob.classifiers import NaiveBayesClassifier
from textblob.classifiers import MaxEntClassifier


class _Classifier:
    def __init__(self, data):
        #self._classifier = NaiveBayesClassifier(data)
        self._classifier = MaxEntClassifier(data)

    def update(self, data):
        """
        data needs to be an iterable(list or tuple) of iterables
        the inner iterable needs to be in the format of ('str', 'label')
        """
        self._classifier.update(data)

    def probability(self, text):
        return self._classifier.prob_classify(text)

    def labels(self):
        return self._classifier.labels()


class ClassifyParser:
    def __init__(self, training_data):
        self._classifier = _Classifier(training_data)
        self.callback_managers = []
        self._labels_data= {}

        def _default_action():
            return None

        for label in self._classifier.labels():
            label_dict = {'action': _default_action,
                          'minimal_probability': 0.90}

            self._labels_data[label] = label_dict

    def parse(self, text):
        # need to define a min probability for when to take action
        probability_distribution = self._classifier.probability(text)
        results = []
        for k, v in self._labels_data.items():
            value_prob = probability_distribution.prob(k)
            print(value_prob, k)
            if v.get('minimum_probability', 0.9) < value_prob:
                result = self._callback_helper(k)
                results.extend(result)

        return results

    def add_callback_manager(self, manager):
        self.callback_managers.append(manager)

    def remove_callback_manager(self, manager):
        self.callback_managers.remove(manager)

    def define_minimum_probability_for_action(self, label, probability):
        self._labels_data[label]['minimum_probability'] = probability

    def _callback_helper(self, key):
        """
        returns list
        """
        result = []
        for manager in self.callback_managers:
            callback_result = manager.call_callback(key)
            if callback_result:
                # TODO: take a look at this and make sure
                # don't want to return a list
                result.extend(callback_result)

        return result
