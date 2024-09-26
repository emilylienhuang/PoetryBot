from CLHW1Functions import *
import os

def writePoemToFile(folder_path, file_lang, language, file_to):

    #create the directory if not already created
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    file_path = os.path.join(folder_path, file_to)

    poem = writePoem(file_lang, language, 4, 9)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(poem)



# def writePoem(file_path, lang, stanzas, line_length):
#writePoem('./English/English200.txt', 'en_core_web_sm',  4, 6)

def genAllPoems(folder_path, lang, new_folder):
    for file_name in os.listdir(folder_path):
        for i in range(5):
            prefix = file_name.strip('.txt')
            poem_name = prefix + "Poem" + str(i) + ".txt"
            absolute_path = folder_path + file_name
            writePoemToFile(new_folder, absolute_path, lang, poem_name)
'''
genAllPoems('./Assamese', 'xx_sent_ud_sm', './AssamesePoems')
genAllPoems('./Bengali', 'xx_sent_ud_sm', './BengaliPoems')
'''
genAllPoems('./English/', 'en_core_web_sm', './EnglishPoems')
'''
genAllPoems('./Hindi', 'xx_sent_ud_sm', './HindiPoems')
genAllPoems('./Spanish', 'es_core_news_sm', './SpanishPoems')
genAllPoems('./Ukrainian', 'uk_core_news_sm', './UkranianPoems')
'''