from CLHW1Functions import genLexicon
import os
import json
import spacy

#spacy.cli.download("es_core_news_sm")
#spacy.cli.download("xx_sent_ud_sm")
#spacy.cli.download("uk_core_news_sm")
output_folder = 'Lexicons'

# go through each language and write output to a file
#Assamese
file_name = '1kAssameseLexicon.json'

file_path = os.path.join(output_folder, file_name)

lexicon = genLexicon('./Assamese/Assamese1k.txt', 'xx_sent_ud_sm')

with open(file_path, 'w') as file:
    json.dump(lexicon, file)
#Bengali
file_name = '1kBengaliLexicon.json'

file_path = os.path.join(output_folder, file_name)

lexicon = genLexicon('./Bengali/Bengali1k.txt', 'xx_sent_ud_sm')

with open(file_path, 'w') as file:
    json.dump(lexicon, file)
#English
file_name = '1kEnglishLexicon.json'

file_path = os.path.join(output_folder, file_name)

lexicon = genLexicon('./English/English1k.txt', 'en_core_web_sm')

with open(file_path, 'w') as file:
    json.dump(lexicon, file)

# Hindi
file_name = '1kHindiLexicon.json'

file_path = os.path.join(output_folder, file_name)

lexicon = genLexicon('./Hindi/Hindi1k.txt', 'xx_sent_ud_sm')

with open(file_path, 'w') as file:
    json.dump(lexicon, file)

#Spanish
file_name = '1kSpanishLexicon.json'

file_path = os.path.join(output_folder, file_name)

lexicon = genLexicon('./Spanish/Spanish1k.txt', 'es_core_news_sm')

with open(file_path, 'w') as file:
    json.dump(lexicon, file)

#Ukranian
file_name = '1kUkranianLexicon.json'

file_path = os.path.join(output_folder, file_name)

lexicon = genLexicon('./Ukrainian/Ukranian1k.txt', 'uk_core_news_sm')

with open(file_path, 'w') as file:
    json.dump(lexicon, file)