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
import concurrent.futures

import lists as word_lists
import reader_saver
import spacy_functions

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

def cosine_distance(a,b):
    s = np.sum(a*b, axis=-1)
    norm_a = np.linalg.norm(a, axis=-1)
    norm_b = np.linalg.norm(b, axis=-1)
    return s / (norm_a * norm_b)

def closest(space, coord, n=10):
    closest = []
    for key in sorted(space.keys(),
                      key=lambda x: distance(coord, space[x]))[:n]:
        closest.append(key)
    return closest


def get_bias_score(compare_list: list, male_words: list, female_words: list, word_embedding: dict,
                   cosine: bool) -> dict:
    word_dict = {}
    for comp_word in compare_list:
        if comp_word in word_embedding:
            male_values = []
            for male_word in male_words:
                male_values.append(distance(word_embedding.get(comp_word), word_embedding.get(male_word), cosine))
            female_values = []
            for female_word in female_words:
                female_values.append(distance(word_embedding.get(comp_word), word_embedding.get(female_word), cosine))
            word_dict[comp_word] = mean(male_values) - mean(female_values)
    return word_dict

def get_bias_score_matrix(compare_list: list, male_vectors: np.array, female_vectors: np.array, word_embedding: dict,
                   cosine: bool) -> dict:
    word_dict = {}
    for comp_word in compare_list:
        if comp_word in word_embedding:
            comp_word_vector = np.array(word_embedding.get(comp_word))
            male_values = cosine_distance(comp_word_vector, male_vectors)
            female_values = cosine_distance(comp_word_vector, female_vectors)
            word_dict[comp_word] = np.mean(male_values) - np.mean(female_values)
    return word_dict


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


def split_dict_equally(input_dict, chunks=1000):
    return_list = [dict() for idx in range(chunks)]
    idx = 0
    for key in input_dict:
        return_list[idx][key] = None
        if idx < chunks - 1:
            idx += 1
        else:
            idx = 0
    return return_list


def split_list_equally(lst, size_of_chunks):
    for i in range(0, len(lst), size_of_chunks):
        yield lst[i:i + size_of_chunks]


'''def run_pool(*, strategy, max_workers=4, comp_word_list=[], male_list=[], fem_list=[], word_emb={}, cosine=True):
    start = time.time()
    with strategy(max_workers=max_workers) as executor:
        result = executor.map(get_bias_score, comp_word_list, male_list, fem_list, word_emb, cosine)
        end = time.time()
    print(f'\nTime to complete using {strategy}, with {max_workers} workers: {end - start:.2f}s\n')

    print(result) # returns an iterator
    print(list(result))'''


if __name__ == "__main__":
    # occupations_list_WinoBias = get_occupations("/home/jonas/Documents/GitRepos/Words/WinoBias.txt")
    # get_unique_sentences("/home/jonas/Documents/GitRepos/Words/WinoBias.txt", occupations_list_WinoBias)
    # get_occupations("/home/jonas/Documents/GitRepos/Words/Sentences_Occupations_Stanovsky.txt")

    # add_adj_to_sentences("/home/jonas/Documents/GitRepos/Words/WinoBias.txt", ["sassy", "brunette", "gorgeous", "grizzled", "burly", "scruffy"])

    # adjectives_list = reader_saver.load_vocab_to_list()
    # verbs_list = reader_saver.load_vocab_to_list()

    # embeddings_dict = load_txt_to_dict("/home/jonas/Documents/GitRepos/PretrainedWordVectors/crawl-300d-2M.vec")

    # Reformat textfile with nested list
    # reader_saver.write_list_to_file(reader_saver.load_nested_vocab_to_list())

    start_time = time.time()
    # save_dict_to_pkl(embeddings_dict, pkl_path_crawl)
    duration = time.time() - start_time
    print("You dumped the pickle in ", duration, " seconds!")

    start_time = time.time()
    pkl_dict = reader_saver.load_pkl_to_dict()
    duration = time.time() - start_time
    print("You loaded the pickle in ", duration, " seconds!")

    adjectives = list(pkl_dict.keys())
    results = []


    '''    run_pool(strategy=concurrent.futures.ThreadPoolExecutor,
             max_workers=4,
             comp_word_list=adjectives,
             male_list = ["he"],
             fem_list = ["she"],
             word_emb=pkl_dict,
             cosine=True)
    '''
    male_words = word_lists.get_bolukbasi_male_list()
    female_words= word_lists.get_bolukbasi_female_list()

    male_vectors = np.array([pkl_dict.get(male_word) for male_word in male_words])
    female_vectors = np.array([pkl_dict.get(female_word) for female_word in female_words])

    #score1 = get_bias_score_matrix(adjectives, male_vectors, female_vectors, pkl_dict, True)
    #score2 = get_bias_score(adjectives, male_words, female_words, pkl_dict, True)
    #print(score1)
    #print(score2)
    #breakpoint()



    #some single threading..
    chunk_size = 3000
    split = split_list_equally(adjectives, chunk_size)
    bias_score_dict = {}
    for list_part in tqdm(split, desc="Get scoring of words: ", total=len(adjectives) // chunk_size):
        bias_score_dict.update(get_bias_score_matrix(list_part, male_vectors, female_vectors, pkl_dict, True))

    breakpoint()

    # some fancy multithreading..
    chunk_size = 1000
    executor = concurrent.futures.ThreadPoolExecutor()
    futures = []
    for list_part in tqdm(split_list_equally(adjectives, chunk_size), desc="Get scoring of words: "):
        futures.append(executor.submit(get_bias_score_matrix, list_part, male_vectors, female_vectors, pkl_dict, True))

    bias_score_dict = {}
    for future in tqdm(futures, desc="working.."):
        bias_score_dict.update(future.result())

    breakpoint()
    '''
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for list_part in tqdm(split_list_equally(adjectives, 500), desc="Get scoring of words: "):
            future = executor.submit(get_bias_score(list_part, ["he"], ["she"], pkl_dict, True))
            result = future.result()
            print(result)
    '''

    '''
    nlp = spacy_functions.NLPWorker()
    adjectives = []
    verbs = []
    for dict_part in tqdm(split_dict_equally(pkl_dict), desc="Tagging words: "):
        adj, ver = nlp.get_adj_verbs(dict_part)
        adjectives.append(adj)
        verbs.append(ver)
    reader_saver.write_list_to_file(adjectives)
    reader_saver.write_list_to_file(verbs)
    '''

    #    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #        for dict_part in tqdm(split_dict_equally(pkl_dict), desc="Multithreadingtest: "):
    #            future = executor.submit(nlp.get_adj_verbs(dict_part))
    #            print(future)

    #for item in split_dict_equally(pkl_dict):
    #    print(len(item))

    #for word_list in spacy_functions.get_adj_verbs(pkl_dict):
    #    reader_saver.write_list_to_file(word_list)

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