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

def calculateBiGramProbabilities(bigrams):
    bi_prob = {}
    uni_count = collections.defaultdict(int)
    bi_count = collections.defaultdict(int)

    for bg in bigrams:
        w1, _ = bg
        uni_count[w1] += 1
        bi_count[bg] += 1

    for bg, count in bi_count.items():
        w1, _ = bg
        bi_prob[bg] = count / uni_count[w1]
    return [bi_count, bi_prob]

def calculateTriProbabilities(bigrams, trigrams):
    bi_count, _ = calculateBiGramProbabilities(bigrams)
    tri_prob = {}
    tri_count = collections.defaultdict(int)
    for tg in trigrams:
        tri_count[tg] += 1

    for tg, count in tri_count.items():
        w1, w2, w3 = tg
        tri_prob[tg] = tri_count[tg] / bi_count[(w1,w2)]
    return tri_prob


def loadHeapTri(pair, probs):
    heap = []
    for g, p in probs.items():
        if (g[0], g[1]) == pair:
            heapq.heappush(heap, (-p, g[2]))
    return heap

def loadHeapBi(word, probs):
    heap = []
    for g, p in probs.items():
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
    bigrams = genNGrams(text, 2)
    trigrams = genNGrams(text, 3)

    # assign probabilities
    _, probsBi = calculateBiGramProbabilities(bigrams)
    probsTri = calculateTriProbabilities(bigrams, trigrams)


    poem = []
    for _ in range(3):
        for _ in range(stanzas):
            phrase = []
            heap = []
            next_word = ""
            for _ in range(random.randint(3, line_length)):
                if len(phrase) >= 2:
                    heap = loadHeapTri(phrase[-2:], probsTri)
                elif len(phrase) == 1:
                    heap = loadHeapBi(phrase[0], probsBi)
                    _, next_word = heapq.heappop(heap)
                    phrase.append(next_word)
                    continue
                else:
                    # if there is not a corresponding ngram or we are at the start of a new line
                    for _ in range(20):
                        heapq.heappush(heap, (-random.randint(0, 100)/100.0, random.choice(text)))
                #choose randomly from most likely sentence continuations
                seen = set(phrase)
                if heap:
                    _, next_word = heapq.heappop(heap)
                else:
                    # there was nothing on the heap, then there was no corresponding tri-gram or bi-gram to match the chosen word
                    next_word = random.choice(text)
                while heap and next_word in seen:
                    _, next_word = heapq.heappop(heap)
                phrase.append(next_word)
                heap = []
            string = ' '.join(phrase[:-1]) + ' ' + phrase[-1] + ","
            poem.append(string)
        poem.append('')
    return '\n'.join(poem)

def formatPoem(poem, stanza):
        for line in poem:
            print(line)
print(writePoem('./English/English200.txt', 'en_core_web_sm',  4, 6))
#


