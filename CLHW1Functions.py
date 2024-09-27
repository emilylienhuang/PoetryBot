import collections
import heapq
import random

import spacy
import nltk
from nltk import ngrams
from collections import defaultdict

import re
import itertools
import textstat
from gensim.models import Word2Vec

#load spacy english model
# en : english
# core : basic
# web: source of text corpus
# sm : small size, light, less memory storage needed
# need to manually download using python interpreter
#spacy.cli.download("en_core_web_sm")
#spacy.cli.download("en_core_web_md")
# read in text base using spacy to create a given lexicon

def genLexicon(file_path, lang):
    nlp = spacy.load(lang)
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # create lexicon
    #remove the "start of and end of delimeters" as seen in text
    cleaned_txt = re.sub(r'<\|startoftext\|>|<\|endoftext\|>', '', text)

    #process the cleaned text through nlp pipline using spacy
    doc = nlp(cleaned_txt)

    lexicon = []

    #extract tokens to create the lexicon
    for token in doc:
        # remove punctuations, excess white spaces, words
        if not token.is_punct and not token.is_space and not token.is_stop and not token.is_digit:
            # use all lowercase for easy probabality parsings later
            lexicon.append(token.lower_)

    return [nlp, doc, lexicon]

#wrapper to create ngrams using the nltk library
#text is a list of words
# num is the n in ngram
# outputs a generator that can be indexed with tuples as keys
def genNGrams(text, num):
    return list(ngrams(text, num))

# calculate the bigram probabilities given a list of bi-grams in this case a generator
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
        w1, w2, _ = tg
        tri_prob[tg] = tri_count[tg] / bi_count[(w1,w2)]
    return tri_prob

'''
Given that we've see "pair" push the most likely next occurring word onto the heap with its 
corresponding probabilitity
'''
def loadHeapTri(pair, probs):
    heap = []
    for g, p in probs.items():
        if (g[0], g[1]) == pair:
            heapq.heappush(heap, (-p, g[2]))
    return heap


'''
Given that we've seen a word, what is the most likely subsequent word to follow pushed onto the heap
'''
def loadHeapBi(word, probs):
    heap = []
    for g, p in probs.items():
        if g[0] == word:
            heapq.heappush(heap, (-p, g[1]))
    return heap
'''
Part of speech tagging used to choose a "theme" for the Poem given the nouns in the corpus.
'''
def chooseTheme(doc):
    topics = [token.text for token in doc if token.pos_ == 'NOUN']
    return random.choice(topics)

def chooseRandomRelatedWord(nlp, text, theme, seen):
    words = ' '.join(text)
    doc = nlp(words)
    theme_token = nlp(theme)
    new_word = random.choice(doc)
    while new_word.similarity(theme_token) < 0.5 or new_word.text in seen:
        new_word = random.choice(doc)
    return new_word.text
'''
logic: I choose from the most likely to occur next words. 
If I can't choose from that. ie. there is no choice for most likely to occur next, 
I choose a random word from the corpus
'''
def writePoem(file_path, lang, stanzas, line_length):
    # create the body of text
    nlp, doc, text = genLexicon(file_path, lang)

    #calculate the grams
    bigrams = genNGrams(text, 2)
    trigrams = genNGrams(text, 3)

    # assign probabilities
    _, probsBi = calculateBiGramProbabilities(bigrams)
    probsTri = calculateTriProbabilities(bigrams, trigrams)

    poem = []
    seen = set()

    theme = chooseTheme(doc)

    for _ in range(3):
        # how many lines per stanza
        for _ in range(stanzas):
            phrase = []
            heap = []
            next_word = chooseRandomRelatedWord(nlp, text, theme, seen)
            # randomly choose how many words per line
            for _ in range(random.randint(3, line_length)):
                if len(phrase) >= 2:
                    # we are able to use the tri-gram probabilities
                    bigram = tuple(phrase[-2:])
                    heap = loadHeapTri(bigram, probsTri)
                elif len(phrase) == 1:
                    # we will use bigram probabilities
                    heap = loadHeapBi(phrase[0], probsBi)

                if heap:
                    _, next_word = heapq.heappop(heap)

                seen.add(next_word)
                phrase.append(next_word)
                heap = []

            phrase[0] = phrase[0][0].upper() + phrase[0][1:]
            string = ' '.join(phrase[:-1]) + ' ' + phrase[-1] + ","
            poem.append(string)
        poem.append('')
    poem[-2] = poem[-2][:-1] + "."
    return [theme, 'On ' + theme + '\n' + '\n'.join(poem)]



theme, poem = writePoem('./English/English200.txt', 'en_core_web_md',  4, 6)

'''
Here we are going to validate the poem by checking how much one phrase leading into another
makes sense or is similar to the preceding phrase.
'''
def genCoherence(theme, poem, lang):
    nlp = spacy.load(lang)

    poem_words = nlp(poem)
    theme_token = nlp(theme)
    return theme_token.similarity(poem_words)
print(poem)
print(genCoherence(theme, poem, 'en_core_web_md'))


'''
Based on the Flesch reading ease metric, returns a score on the 0, 100 interval
'''
def genReadingEase(poem, lang):
    textstat.set_lang(lang)
    return textstat.flesch_reading_ease(poem)

def genGradeLevel(poem, lang):
    textstat.set_lang(lang)
    return textstat.flesch_kincaid_grade(poem)
print(genReadingEase(poem, "en"))
print(genGradeLevel(poem, "en"))