import collections
import heapq
import random

import spacy
import nltk
from nltk import ngrams
from collections import defaultdict

import re

#load spacy english model
# en : english
# core : basic
# web: source of text corpus
# sm : small size, light, less memory storage needed
# need to manually download using python interpreter
#spacy.cli.download("en_core_web_sm")

# read in text base
def genLexicon(file_path, lang):
    nlp = spacy.load(lang)
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # create lexicon
    #remove the "start of and end of delimeters"
    cleaned_txt = re.sub(r'<\|startoftext\|>|<\|endoftext\|>', '', text)

    #process the cleaned text through nlp pipline using spacy
    doc = nlp(cleaned_txt)

    lexicon = []
    #do I want have repeated values in my lexicon

    #extract tokens to create the lexicon
    for token in doc:
        # remove punctuations, excess white spaces, words
        if not token.is_punct and not token.is_space and not token.is_stop and not token.is_digit:
            lexicon.append(token.lower_)

    return lexicon

#wrapper to create ngrams using the nltk library
#text is a list of words
# num is the n in ngram
# outputs a generator that can be indexed
def genNGrams(text, num):
    return list(ngrams(text, num))

def calculateProbabilities(grams):
    gram_to_prob = {}
    for g in grams:
        gram_to_prob[g] = 1 + gram_to_prob.get(g,0)
    for gram, prob in gram_to_prob.items():
        gram_to_prob[gram] /= len(gram_to_prob.values())
    return gram_to_prob

def loadHeap(word, probs):
    heap = []
    for g,p in probs.items():
        if g[0] == word:
            heapq.heappush(heap, (-p, g[1]))
    return heap
'''
logic: I choose one of the most likely occurring choices
if no choice availbale, I choose a random word to get the ball rolling again
I'm making nonsense... Make it make more sense with 3-grams?
'''
def writePoem(file_path, lang, stanzas, line_length):
    # create the body of text
    text = genLexicon(file_path, lang)

    #calculate the grams
    grams = genNGrams(text, 2)

    # assign probabilities
    probs = calculateProbabilities(grams)


    poem = []
    for _ in range(3):
        for _ in range(stanzas):
            phrase = []
            heap = []
            for _ in range(line_length):
                if phrase:
                    heap = loadHeap(phrase[-1], probs)
                if not phrase or not heap:
                    # if there is not a corresponding ngram or we are at the start of a new line
                    for _ in range(20):
                        heapq.heappush(heap, (-random.randint(0, 100)/100.0, random.choice(text)))
                #alternate between least and most occurring
                for _ in range(random.randint(1,3)):
                    if heap:
                        _, new_word = heapq.heappop(heap)
                    else:
                        break
                phrase.append(new_word)
                heap = []
            string = ' '.join(phrase[:-1]) + ' ' + phrase[-1] + ","
            poem.append(string)
        poem.append('')
    return poem

def formatPoem(poem, stanza):
        for line in poem:
            print(line)
formatPoem(writePoem('./English/English200.txt', 'en_core_web_sm',  4, 4), 4)
#


