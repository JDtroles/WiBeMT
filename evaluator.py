import math
import re
from statistics import mean
from string import digits

import numpy as np
from tqdm import tqdm


def cosine_distance(a, b):
    s = np.sum(a*b, axis=-1)
    norm_a = np.linalg.norm(a, axis=-1)
    norm_b = np.linalg.norm(b, axis=-1)
    return s / (norm_a * norm_b)


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


def get_bias_score_matrix(compare_list: list, male_vectors: np.array, female_vectors: np.array, word_embedding: [list]) -> [list]:
    word_tuples = []
    for comp_word in compare_list:
        if comp_word in word_embedding:
            comp_word_vector = np.array(word_embedding.get(comp_word))
            male_values = cosine_distance(comp_word_vector, male_vectors)
            female_values = cosine_distance(comp_word_vector, female_vectors)
            word_tuples.append([comp_word, np.mean(male_values) - np.mean(female_values)])
    return word_tuples


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