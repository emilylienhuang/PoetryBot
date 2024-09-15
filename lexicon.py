import spacy

import spacy_ngram
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

    lexicon = set()

    #extract tokens to create the lexicon
    for token in doc:
        # remove punctuations, excess white spaces, words
        if not token.is_punct and not token.is_space and not token.is_stop and not token.is_digit:
            # chop off and only add root words or meanings into the vocabulary to dumb down to
            #simplest parts
            if token.lemma_ not in lexicon:
                lexicon.add(token.lemma_.lower())
    return lexicon
lexicon = genLexicon('./English/English1k.txt', 'en_core_web_sm')
