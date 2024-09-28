from CLHW1Functions import *
import os
#spacy.cli.download("xx_sent_ud_md")
def writePoemToFile(folder_path, file_to, probsBi, probsTri, nlp, doc, text, model=True):

    #create the directory if not already created
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, file_to)

    _, poem = writePoem(probsBi, probsTri, nlp, doc, text, 4, 9, model)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(poem)


def genAllPoems(folder_path, lang, new_folder, model=True):
    for file_name in os.listdir(folder_path):
        probsBi, probsTri, nlp, doc, text = genProbs(folder_path + file_name, lang)
        for i in range(10):
            prefix = file_name.strip('.txt')
            poem_name = prefix + "Poem" + str(i) + ".txt"
            absolute_path = folder_path + file_name
            writePoemToFile(new_folder, poem_name, probsBi, probsTri, nlp, doc, text, model)

def writePoemToFileXX(folder_path, file_lang, language, file_to):

    #create the directory if not already created
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, file_to)

    _,poem = writePoemXX(file_lang, language, 4, 9)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(poem)

# def writePoem(file_path, lang, stanzas, line_length):
#writePoem('./English/English200.txt', 'en_core_web_sm',  4, 6)

#genAllPoems('./Assamese/', 'xx_sent_ud_sm', './AssamesePoems', False)

#genAllPoems('./Bengali/', 'xx_sent_ud_sm', './BengaliPoems', False)

#genAllPoems('./English/', 'en_core_web_sm', './EnglishPoems')
#genAllPoems('./English/', 'en_core_web_md', './EnglishPoems')
#genAllPoems('./Hindi/', 'xx_sent_ud_sm', './HindiPoems', False)
#genAllPoems('./Spanish/', 'es_core_news_md', './SpanishPoems')
#genAllPoems('./Ukrainian/', 'uk_core_news_md', './UkranianPoems')
