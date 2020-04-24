# TODO: GloVe model (glove.840B.300d.zip)
# TODO: word2vec GoogleNews model (Bolukbasi)


import spacy
import annoy
import numpy as np
import math
from tqdm import tqdm
import pickle
import time
from statistics import mean
import re
from string import digits
from pathlib import Path
import os.path
import tkinter as tk
from tkinter import filedialog
import lists as word_lists
import reader_saver


"""Translates text into the target language.

Target must be an ISO 639-1 language code.
See https://g.co/cloud/translate/v2/translate-reference#supported_languages
"""
"""
from google
translate_client = translate.Client()

if isinstance(text, six.binary_type):
    text = text.decode('utf-8')

# Text can also be a sequence of strings, in which case this method
# will return a sequence of results for each text.
result = translate_client.translate(
    text, target_language=target)

print(u'Text: {}'.format(result['input']))
print(u'Translation: {}'.format(result['translatedText']))
print(u'Detected source language: {}'.format(
    result['detectedSourceLanguage']))
    """


# from sklearn.metrics.pairwise import cosine_similarity

# Load Vectors in Python (source: https://fasttext.cc/docs/en/english-vectors.html)
# import io
#
#
# def load_vectors(fname):
#     fin = io.open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore')
#     n, d = map(int, fin.readline().split())
#     data = {}
#     for line in fin:
#         tokens = line.rstrip().split(' ')
#         data[tokens[0]] = map(float, tokens[1:])
#     return data

# Load GloVe vectors in SpaCy
# vectors = spacy.vectors.Vectors()
# vectors.from_glove("/home/jonas/Documents/GitRepos/PretrainedWordVectors/GloVe840B/")


def distance(coord1, coord2, cosine):
    # note, this is VERY SLOW, don't use for actual code
    if cosine:
        dot = np.dot(coord1, coord2)
        norma = np.linalg.norm(coord1)
        normb = np.linalg.norm(coord2)
        cos = dot / (norma * normb)
        return cos
    else:
        return math.sqrt(sum([(i - j) ** 2 for i, j in zip(coord1, coord2)]))


def closest(space, coord, n=10):
    closest = []
    for key in sorted(space.keys(),
                      key=lambda x: distance(coord, space[x]))[:n]:
        closest.append(key)
    return closest


def get_bias_score(comp_word, male_words, female_words, word_embedding, cosine):
    if comp_word in word_embedding:
        male_values = []
        for male_word in male_words:
            male_values.append(distance(word_embedding.get(comp_word), word_embedding.get(male_word), cosine))
        female_values = []
        for female_word in female_words:
            female_values.append(distance(word_embedding.get(comp_word), word_embedding.get(female_word), cosine))
        return mean(male_values) - mean(female_values)
    else:
        print(comp_word, " is not in the dictionary.")
        return None


def evaluate_words_for_gender(word_list, male_words, female_words, word_embedding, cosine):
    tuples_word_rank = []
    for word in tqdm(word_list, desc="Evaluating words in list: "):
        word = re.sub(r"\s+", "", word, flags=re.UNICODE)
        word = word.translate(str.maketrans('', '', digits))
        if word in word_embedding:
            tuples_word_rank.append([word, get_bias_score(word, male_words, female_words, word_embedding, cosine)])
        else:
            print(word, "not in embedding")
    return tuples_word_rank


def get_min_or_max_values(tuples, n, min):
    tuples.sort(key=lambda tup: tup[1])
    if min:
        return tuples[:n]
    else:
        return tuples[(len(tuples) - n):]


def sort_bolukbasi_gender_list(gender_list_path, fem_list, ma_list, word_emb):
    gender_list_female = []
    gender_list_male = []
    with open(gender_list_path, 'r', encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Creating vocab list: "):
            values = line.split(", ")
            for word in values:
                if word in word_emb:
                    if get_bias_score(word, ma_list, fem_list, word_emb, True) < 0:
                        gender_list_male.append(word)
                    else:
                        gender_list_female.append(word)
    return gender_list_male, gender_list_female


def get_occupations(path) -> list:
    occupations = set()
    with open(path, 'r', encoding="utf-8") as f:
        for line in f:
            values = line.split("\t")
            occu = values[3].replace("the ", "")
            occu = occu.replace("The ", "")
            occu = occu.replace("a ", "")
            occu = occu.replace("an ", "")
            occupations.add(re.sub(r"\s+", "", occu, flags=re.UNICODE))
    occupations_list = list(occupations)
    occupations_list.sort()
    with open("/home/jonas/Documents/GitRepos/Words/occupations_WinoMT.txt", "w") as f:
        for elem in occupations_list:
            f.write(elem)
            f.write("\n")
    print("Occupations:", len(occupations_list), "\n", occupations_list)
    return occupations_list


def get_unique_sentences(path_sentences, occupations_list):
    sentences_set = set()
    with open(path_sentences, 'r', encoding="utf-8") as f:
        for line in f:
            values = line.split("\t")
            occupation = values[3].replace("the ", "").replace("The ", "").replace("a ", "").replace("an ", "").rstrip()
            sentence = values[2].replace(occupation, "X")
            for elem in occupations_list:
                sentence = sentence.replace(elem, "Y")
            # she, he = X1; her, his = X2; her, him = X3
            gender_pronoun_space = [" she ", " he ", " her ", " him ", " his "]
            for elem in gender_pronoun_space:
                sentence = sentence.replace(elem, " X1 ")
            gender_pronoun_dot = [" she.", " he.", " her.", " him.", " his."]
            for elem in gender_pronoun_dot:
                sentence = sentence.replace(elem, " X1.")
            sentences_set.add(sentence)
    sentences_list = list(sentences_set)
    sentences_list.sort()
    with open("/home/jonas/Documents/GitRepos/Words/sentences_WinoBias.txt", "w") as f:
        for elem in sentences_list:
            f.write(elem)
            f.write("\n")
    print("Unique sentences:", len(sentences_list), "\n", sentences_list)


def add_adj_to_sentences(path_sentences, adj_list):
    # TODO: add try except block to read function
    '''
    try:
    with open('/etc/hosts') as f:
        print(f.readlines())
        # Do something with the file
    except FileNotFoundError:
        print("File not accessible")
    '''
    with open(path_sentences, "r", encoding="utf-8") as f:
        adj_sentences: list = []
        n_of_letters: int = 0
        for line in f:
            line = line.strip("\n")
            values = line.split("\t")
            occupation = values[3].replace("The ", "").replace("the ", "")
            sentence = values[2]
            for adj in adj_list:
                replacement = adj + " " + occupation
                sentence_plus_adj = sentence.replace(occupation, replacement)
                n_of_letters += len(sentence_plus_adj)
                adj_sentences.append(sentence_plus_adj)
    with open("/home/jonas/Documents/GitRepos/Words/sentences_WinoBias_with ADJECTIVES.txt", "w") as f:
        for elem in adj_sentences:
            f.write(elem)
            f.write("\n")
    print("Zeichen:", n_of_letters)





if __name__ == "__main__":
    reader_saver.save_dict_to_pkl({1})
    reader_saver.write_nested_list_to_file([[1,2,3,4,5,6],["a", "b", "c"], ["trallalala"]])
    occupations_list_WinoBias = get_occupations("/home/jonas/Documents/GitRepos/Words/WinoBias.txt")
    get_unique_sentences("/home/jonas/Documents/GitRepos/Words/WinoBias.txt", occupations_list_WinoBias)
    # get_occupations("/home/jonas/Documents/GitRepos/Words/Sentences_Occupations_Stanovsky.txt")

    add_adj_to_sentences("/home/jonas/Documents/GitRepos/Words/WinoBias.txt",
                         ["sassy", "brunette", "gorgeous", "grizzled", "burly", "scruffy"])

    adjectives_list = reader_saver.load_vocab_to_list()
    verbs_list = reader_saver.load_vocab_to_list()

    # embeddings_dict = load_txt_to_dict("/home/jonas/Documents/GitRepos/PretrainedWordVectors/crawl-300d-2M.vec")

    start_time = time.time()
    # save_dict_to_pkl(embeddings_dict, pkl_path_crawl)
    duration = time.time() - start_time
    print("You dumped the pickle in ", duration, " seconds!")

    start_time = time.time()
    pkl_dict = reader_saver.load_pkl_to_dict()
    duration = time.time() - start_time
    print("You loaded the pickle in ", duration, " seconds!")


    '''
    evaluated_words = evaluate_words_for_gender(list(pkl_dict.keys()), bolukbasi_male_list, bolukbasi_female_list, pkl_dict, True)
    print("Get all gender Female words: ")
    for word in get_min_or_max_values(evaluated_words, 20, True):
        print(word)
    print("Get all gender Male words: ")
    for word in get_min_or_max_values(evaluated_words, 20, False):
        print(word)
    '''

    # if "penis" in embeddings_dict:
    #     print("Yes, 'penis' is one of the keys in the embeddings_dict dictionary")
    #     print(embeddings_dict.get("penis"))
    #
    # for elem in gender_list:
    #     print(elem)
    #     print(get_bias_score(elem, male_list, female_list, embeddings_dict))

    # print("Penis neighbours in embeddings_dict", closest(embeddings_dict, embeddings_dict.get("penis")))
    # print("Penis neighbours in pkl_dict", closest(pkl_dict, pkl_dict.get("penis")))
