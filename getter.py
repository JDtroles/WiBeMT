import re

import numpy as np

import lists as word_lists
from evaluator import get_bias_score_matrix
from main import pkl_dict


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


def get_plotting_word_list(words: list, word_emb) -> [list]:
    male_words = word_lists.get_bolukbasi_male_list()
    female_words = word_lists.get_bolukbasi_female_list()

    male_vectors = np.array([pkl_dict.get(male_word) for male_word in male_words])
    female_vectors = np.array([pkl_dict.get(female_word) for female_word in female_words])

    he_vector = np.array(pkl_dict.get("he"))
    she_vector = np.array(pkl_dict.get("she"))

    words_to_plot = []

    for word in words:
        x_val = get_bias_score_matrix([word], he_vector, she_vector, word_emb)
        print(x_val)
        y_val = get_bias_score_matrix([word], male_vectors, female_vectors, word_emb)
        words_to_plot.append([word, x_val[0][1], y_val[0][1]])
    print(words_to_plot)
    return words_to_plot