# Let's create a FAQ for my stream
# 1. Nyancat / vim / IDE
# 2. How many years I've been programming AKA EXPERIENCE
# 2. How to start programming
import json
import sys
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import IntentDeterminationEngine


tokenizer = EnglishTokenizer()
trie = Trie()
tagger = EntityTagger(trie, tokenizer)
parser = Parser(tokenizer, tagger)

engine = IntentDeterminationEngine()

# need to create 3 intents using the IntentBuilder
# register those 3 intents with our engine

experience_keywords = [
        'years',
        'languages',
        'time'
        'long',
        ]

working_on_keywords = [
        'making',
        'doing',
        'working',
        'coding',
        ]

environment_keywords = [
        'nyancat',
        'IDE',
        'vim',
        'cursor',
        ]

keyword_labels = ['experience_keyword',
                  'working_on_keyword',
                  'environment_keyword']

keyword_values = (experience_keywords,
                  working_on_keywords,
                  environment_keywords)

# Need to register each of our kewywords with the keyword label in our `Engine`
# so do some nasty looping to accomplish this
for keyword_label, keywords in zip(keyword_labels, keyword_values):
    for member in keywords:
        engine.register_entity(member, keyword_label)

experience_intent = IntentBuilder("experience_intent").require('experience_keyword').build()

working_on_intent = IntentBuilder('working_on_intent').require('working_on_keyword').build()

environment_intent = IntentBuilder('environment_intent').require('environment_keyword').build()

engine.register_intent_parser(experience_intent)
engine.register_intent_parser(working_on_intent)
engine.register_intent_parser(environment_intent)

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
                          'nice nyan cat as a cursor',
                          'nice cursor')

working_on_utterances = ('what are you coding',
                         'what are you making',
                         'what are you doing',
                         'what are you working on',
                         'what you making')

bogus_utterances = (
        'if you going to use nltk u may want to check this out spacy .io',
        'sup people? I see the weather\'s getting better over there, Ben.',
        'i had the same problem your having so thats my i made my own.',
        'try http, instead of https'
        )

# TODO: Figure out how to make this stronger
dual_utterance = ('how long have you been coding and what IDE do you use',)

for utterance in dual_utterance:
    print(utterance)
    for intent in engine.determine_intent(utterance):
        if intent and intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))

"""
for utterance in environment_utterances:
    for intent in engine.determine_intent(utterance):
        if intent and intent.get('confidence') > 0:
            print(utterance, '\n', json.dumps(intent, indent=4))

for utterance in working_on_utterances:
    for intent in engine.determine_intent(utterance):
        if intent and intent.get('confidence') > 0:
            print(utterance, '\n', json.dumps(intent, indent=4))
"""
