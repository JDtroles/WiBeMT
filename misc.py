import numpy as np
from tqdm import tqdm

import get_ressources
from evaluator import get_bias_score


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


def get_gender_ranking_vectors(pkl_dict):
    # he / she as word lists
    male_words = ["he"]
    female_words = ["she"]
    # bolukbasi gender word lists
    male_words_boluk = get_ressources.get_bolukbasi_male_list()
    female_words_boluk = get_ressources.get_bolukbasi_female_list()
    # convert words to corresponding vectors
    male_vectors = np.array([pkl_dict.get(male_word) for male_word in male_words])
    female_vectors = np.array([pkl_dict.get(female_word) for female_word in female_words])
    male_vectors_boluk = np.array([pkl_dict.get(male_word) for male_word in male_words_boluk])
    female_vectors_boluk = np.array([pkl_dict.get(female_word) for female_word in female_words_boluk])
    return female_vectors, female_vectors_boluk, male_vectors, male_vectors_boluk


def normalize_ranked_words(ranked_words):
    all_values = [value[1] for value in ranked_words]
    min_all_values = min(all_values)
    max_all_values = max(all_values)
    lower_bound: int = -1
    upper_bound: int = 1
    for value in ranked_words:
        value[1] = lower_bound + (((value[1] - min_all_values) * (upper_bound - lower_bound)) /
                                  (max_all_values - min_all_values))
    return ranked_words


def normalize_sum_all(results_dict):
    all_values = [results_dict[key]["sum_all"] for key in results_dict]
    min_all_values = min(all_values)
    max_all_values = max(all_values)
    lower_bound: int = -1
    upper_bound: int = 1
    for key in results_dict:
        results_dict[key]["sum_all"] = lower_bound + (
                    ((results_dict[key]["sum_all"] - min_all_values) * (upper_bound - lower_bound)) /
                    (max_all_values - min_all_values))
    return results_dict
