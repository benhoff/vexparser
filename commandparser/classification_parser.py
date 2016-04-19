from textblob.classifiers import NaiveBayesClassifier
from textblob.classifiers import MaxEntClassifier


class _Classifier:
    def __init__(self, data):
        # self._classifier = NaiveBayesClassifier(data)
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
        self._labels_data= {}

        def _default_action():
            return None

        for label in self._classifier.labels():
            label_dict = {'action': _default_action,
                          'minimal_probability': 0.99}

            self._labels_data[label] = label_dict

    def associate_label_with_action(self, label, action):
        self._labels_data[label]['action'] = action

    def define_minimum_probability_for_action(self, label, probability):
        self._labels_data[label]['minimum_probability'] = probability

    def parse(self, text):
        # need to define a min probability for when to take action
        probability_distribution = self._classifier.probability(text)
        results = []
        for k, v in self._labels_data.items():
            value_prob = probability_distribution.prob(k)
            print(value_prob, k)
            if v['minimum_probability'] < value_prob:
                action_result = v['action']()

                results.append(action_result)

        return results
