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

#load spacy english model
# en : english
# core : basic
# web: source of text corpus
# sm : small size, light, less memory storage needed
# need to manually download using python interpreter
#spacy.cli.download("en_core_web_sm")
#spacy.cli.download("en_core_web_lg")
# read in text base using spacy to create a given lexicon
'''
genLexicon generates a lexicon for the given language.
Inputs:
file_path - the path to the corresponding corpus
lang - the language parsing type used for the spacy model
Outputs:
text - a list of all words in the corpus in the ordering they appear
'''
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


'''
genNGrams is a wrapper to create ngrams using the nltk library.
Input: 
text - list of text words
num - n-gram number, unigram, bigram, or trigram 
'''
def genNGrams(text, num):
    return list(ngrams(text, num))

# calculate the bigram probabilities given a list of bi-grams in this case a generator
'''
calculateBiGramProbabilities calculates the bigram probabilities given a list of bi-grams in this case a generator
Input:
bigrams - a generator list of bigrams
Output:
bi_count - the count of times two words appear together in a particular ordering
bi_prob - the bigram probabilities of each two-word tuple
'''
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

'''
calculateTriGramProbabilities calculates the tri-gram probabilities given a list of tri-grams in this case a generator
Input:
bigrams - a generator list of bigrams
trigrams - a generator list of trigrams
Output:
tri_prob - the trigram probabilities of each three-word tuple
'''
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
loadHeapTri takes in two words and generates a heap of the word most likely to occur next
Input:
pair - a pair of two words that already have been seen in a particular order in the poem
probs - the tri-gram probabilities from the original inpu text
Output:
heap - a max heap where the most likely to occur word is on top
'''
def loadHeapTri(pair, probs):
    heap = []
    for g, p in probs.items():
        if (g[0], g[1]) == pair:
            heapq.heappush(heap, (-p, g[2]))
    return heap


'''
loadHeapBi takes in an input word and generates a heap of the word most likely to occur next
Input:
word - the word that has already been seen first in the text
probs - the bi-gram probabilities from the original input text
Output:
heap - a max heap where the most likely to occur word is on top
'''
def loadHeapBi(word, probs):
    heap = []
    for g, p in probs.items():
        if g[0] == word:
            heapq.heappush(heap, (-p, g[1]))
    return heap
'''
chooseTheme Randomly assigns a theme from the given nouns inside of the corpus.
Part of speech tagging is used to choose a "theme" for the Poem given the nouns in the corpus.
Input: 
doc - the nlp tokens per word
Output:
a random choice from the nouns in the corpus.
'''
def chooseTheme(doc):
    topics = [token.text for token in doc if token.pos_ == 'NOUN']
    return random.choice(topics)

'''
chooseRandomRelatedWord takes in a theme and randomly chooses a word likely to occur next given the theme.
Input:
nlp - the pre-loaded natural language processing model using spacy
text - the lest of words in particular ordering in the corpus as a list of strings
theme - the original theme of the poem as a string input
seen - a set of the words that have already occurred in the poem
Output:
a randomly selected word related to the theme and not already in the poem
'''


def genProbs(file_path, lang):
    # create the body of text
    nlp, doc, text = genLexicon(file_path, lang)

    # calculate the grams
    bigrams = genNGrams(text, 2)
    trigrams = genNGrams(text, 3)

    # assign probabilities
    _, probsBi = calculateBiGramProbabilities(bigrams)
    probsTri = calculateTriProbabilities(bigrams, trigrams)
    return [probsBi, probsTri, nlp, doc, text]
'''
writePoem creates the poem given inputs
Inputs:
file_path - text string representing where to retrieve the corpus
lang - a string representing the spacy language model to load
stanzas - the count of how many stanzas are to be desired in the randomly generated poem
line_length - an integer representing the maximum number of words in a line
'''

def writePoem(probsBi, probsTri, nlp, doc, text, stanzas, line_length, model=True):

    poem = []
    seen = set()

    theme = random.choice(text)
    if model:
        theme = chooseTheme(doc)

    theme_token = nlp(theme)

    filtered_tokens = []
    if model:
        filtered_tokens = [token for token in doc if token.is_alpha and token.similarity(theme_token) >= 0.5]


    for _ in range(3):
        # how many lines per stanza
        for _ in range(stanzas):
            phrase = []
            heap = []
            if filtered_tokens:
                next_word = random.choice(filtered_tokens).text
            else:
                next_word = random.choice(text)
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

                if next_word in seen:
                    coin_flip = random.randint(0,1)
                    if coin_flip and filtered_tokens:
                        next_word = random.choice(filtered_tokens).text
                    else:
                        next_word = random.choice(text)

                seen.add(next_word)
                phrase.append(next_word)
                heap = []

            phrase[0] = phrase[0][0].upper() + phrase[0][1:]
            string = ' '.join(phrase[:-1]) + ' ' + phrase[-1] + ","
            poem.append(string)
        poem.append('')
    poem[-2] = poem[-2][:-1] + "."
    print("Wrote Poem")
    return [theme, theme + '\n' + '\n'.join(poem)]

'''
writePoem creates the poem given inputs
Inputs:
file_path - text string representing where to retrieve the corpus
lang - a string representing the spacy language model to load
stanzas - the count of how many stanzas are to be desired in the randomly generated poem
line_length - an integer representing the maximum number of words in a line
'''
def writePoemXX(file_path, lang, stanzas, line_length):
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

    theme = random.choice(text)

    for _ in range(3):
        # how many lines per stanza
        for _ in range(stanzas):
            phrase = []
            heap = []
            next_word = random.choice(text)
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

                while next_word in seen:
                    next_word = random.choice(text)


                seen.add(next_word)
                phrase.append(next_word)
                heap = []

            phrase[0] = phrase[0][0].upper() + phrase[0][1:]
            string = ' '.join(phrase[:-1]) + ' ' + phrase[-1] + ","
            poem.append(string)
        poem.append('')
    poem[-2] = poem[-2][:-1] + "."
    return [theme, theme + '\n' + '\n'.join(poem)]

probsBi, probsTri, nlp, doc, text = genProbs('./English/English200.txt', 'en_core_web_sm')

theme, poem = writePoem(probsBi, probsTri, nlp, doc, text, 4, 6, False)
#print(poem)

'''
genCoherence checks if the poem is similar to its theme using the spacy library
Inputs:
theme - a string word representation of the poem's topic
poem - a string representing the poem's entire content
lang - the spacy language model to load
Output:
a "coherence" score referencing the similarity of the poem to its theme on a [0,1] interval
'''
def genCoherence(theme, poem, lang):
    nlp = spacy.load(lang)
    poem_words = nlp(poem)
    theme_token = nlp(theme)
    return theme_token.similarity(poem_words)
#print(poem)
#print(genCoherence(theme, poem, 'en_core_web_md'))


'''
genReadingEase outputs a score based on the Flesch reading ease metric, returns a score on the 0, 100 interval.
100 being completely easy to read, 0 being impossible to read.
Input:
poem - the string representing the entire poem
lang - the text_stat language model to load
Output:
The Flesch reading ease metric.
'''
def genReadingEase(poem, lang):
    textstat.set_lang(lang)
    return textstat.flesch_reading_ease(poem)

'''
genGradeLevel outputs a numeric representation of the American school system's grade number 
needed to understand a piece of input text.
Input: 
poem - the string representing the entire poem
lang - the text_stat language model to load
Output:
the associated reading level of the piece
'''
def genGradeLevel(poem, lang):
    textstat.set_lang(lang)
    return textstat.flesch_kincaid_grade(poem)
print(genReadingEase(poem, "en"))
#print(genGradeLevel(poem, "en"))