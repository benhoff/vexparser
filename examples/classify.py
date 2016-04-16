from textblob.classifiers import NaiveBayesClassifier

# Let's create a FAQ for my stream
experience_utterances = ('how many years have you programming',
                         'how long have you been coding python',
                         'what languages do you know',
                         'what languages do you code',
                         'how long are you with python')

environment_utterances = ('how do you get the nyancat',
                          'nyancat',
                          'cool IDE',
                          'whats that IDE',
                          'what\'s your vim setup',
                          'what is the editor',
                          'nice nyan cat as a cursor',
                          'nice cursor')

working_on_utterances = ('what are you coding',
                         'what are you making',
                         'what are you doing',
                         'what are you doing at the moment',
                         'what are you working on',
                         'what you making')

experience_utterances = [(x, 'experience') for x in experience_utterances]
environment_utterances = [(x, 'enivornment') for x in environment_utterances]
working_on_utterances = [(x, 'working') for x in working_on_utterances]

# FIXME: find better way to flatten lists together
training_set = []
training_set.extend(experience_utterances)
training_set.extend(environment_utterances)
training_set.extend(working_on_utterances)


classifier = NaiveBayesClassifier(training_set)

bogus_utterances = (
        'if you going to use nltk u may want to check this out spacy .io',
        'sup people? I see the weather\'s getting better over there, Ben.',
        'i had the same problem your having so thats my i made my own.',
        'try http, instead of https'
        )

# TODO: Figure out how to make this stronger
dual_utterance = ('how long have you been coding and what IDE do you use',)

test_utterances = ('what are you making',
                   'hey that nyancat is cool, how do you get that?')

for t in test_utterances:
    prob_dist = classifier.prob_classify(t)
    print(t, '\n', prob_dist.max(), prob_dist.prob(prob_dist.max()))
