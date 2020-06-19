# TODO: GloVe model (glove.840B.300d.zip)
# TODO: word2vec GoogleNews model (Bolukbasi)


# import spacy
# import annoy
import numpy as np
import gc

import get_ressources
import reader_saver
# import spacy_functions
from evaluator import get_bias_score_matrix


# TODO: CREATE FUNCTION TO GET PLOTTER WORDS
# 1st: rank words by bolukbasi-lists
# 2nd: rank words by he - she
# 3rd: return list: [[he-she-value, bolukbasi-value, "word"], ...]

################
# PIPELINES... #
################
# ...that implement one step of workflow from loading data to saving data

# pipeline_1 ranks words and saves them as a dict with the following format:
# word -> origin -> selection metric -> glove gender value -> fastText gender value
def pipeline_1() -> bool:
    # initialize dict
    word_score = {}

    # Load word embedding 1
    print("Choose the GLOVE word embedding .PKL you want to load")
    pkl_dict = reader_saver.load_pkl_to_dict()

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

    # load the word list you want to rank
    print("Now choose the origin of the word list:")
    print("patternbasedwriting.com = 1")
    print("Oxford Dictionary = 2")
    print("Glove = 3")
    print("fastText = 4")
    while True:
        try:
            origin_int = int(input("Enter the corresponding number:"))
            if origin_int < 1 or origin_int > 4:
                raise ValueError
            elif origin_int == 1:
                origin = "patternbasedwriting.com"
                print("You chose \"patternbasedwriting.com\" as origin")
                print("Now choose the corresponding wordlist in .txt format")
                word_list = reader_saver.load_vocab_to_list_at_2nd_pos()
                break
            elif origin_int == 2:
                origin = "Oxford Dictionary"
                print("You chose \"Oxford Dictionary\" as origin")
                # print("Now choose the corresponding wordlist in .txt format")
                print("No Oxford list available yet")
                break
            elif origin_int == 3:
                origin = "Glove"
                print("You chose \"Glove\" as origin")
                print("Now choose the corresponding wordlist in .txt format")
                word_list = reader_saver.load_nested_vocab_to_list()
                break
            elif origin_int == 4:
                origin = "fastText"
                print("You chose \"fastText\" as origin")
                print("Now choose the corresponding wordlist in .txt format")
                word_list = reader_saver.load_nested_vocab_to_list()
                break

        except ValueError:
            print("Please enter an int between 1 - 4")

    # ranking with he-she and Glove
    print("Ranking with he-she and Glove")
    ranked_words = get_bias_score_matrix(word_list, male_vectors, female_vectors, pkl_dict)
    for elem in ranked_words:
        word_score[elem[0]] = {}
        word_score[elem[0]]["origin"] = origin
        word_score[elem[0]]["Glove_he_she"] = elem[1]
        if elem[1] < 0:
            word_score[elem[0]]["Glove_bolukbasi"] = -99
            word_score[elem[0]]["fastText_he_she"] = -99
            word_score[elem[0]]["fastText_bolukbasi"] = -99
        else:
            word_score[elem[0]]["Glove_bolukbasi"] = 99
            word_score[elem[0]]["fastText_he_she"] = 99
            word_score[elem[0]]["fastText_bolukbasi"] = 99

    # ranking with bolukbasi and Glove
    print("Ranking with bolukbasi and Glove")
    ranked_words = get_bias_score_matrix(word_list, male_vectors_boluk, female_vectors_boluk, pkl_dict)
    for elem in ranked_words:
        word_score[elem[0]]["Glove_bolukbasi"] = elem[1]

    # Load word embedding 2
    print("Choose the fastText word embedding .PKL you want to load")
    pkl_dict = None
    gc.collect()
    pkl_dict = reader_saver.load_pkl_to_dict()

    # convert words to corresponding vectors
    male_vectors = np.array([pkl_dict.get(male_word) for male_word in male_words])
    female_vectors = np.array([pkl_dict.get(female_word) for female_word in female_words])
    male_vectors_boluk = np.array([pkl_dict.get(male_word) for male_word in male_words_boluk])
    female_vectors_boluk = np.array([pkl_dict.get(female_word) for female_word in female_words_boluk])

    # ranking with he-she and fastText
    print("Ranking with he-she and fastText")
    ranked_words = get_bias_score_matrix(word_list, male_vectors, female_vectors, pkl_dict)
    for elem in ranked_words:
        if elem[0] in word_score:
            word_score[elem[0]]["fastText_he_she"] = elem[1]
        else:
            word_score[elem[0]] = {}
            word_score[elem[0]]["origin"] = origin
            if elem[1] < 0:
                word_score[elem[0]]["Glove_he_she"] = -99
                word_score[elem[0]]["Glove_bolukbasi"] = -99
            else:
                word_score[elem[0]]["Glove_he_she"] = 99
                word_score[elem[0]]["Glove_bolukbasi"] = 99
            word_score[elem[0]]["fastText_he_she"] = elem[1]


    # ranking with bolukbasi and fastText
    print("Ranking with bolukbasi and fastText")
    ranked_words = get_bias_score_matrix(word_list, male_vectors_boluk, female_vectors_boluk, pkl_dict)
    for elem in ranked_words:
        word_score[elem[0]]["fastText_bolukbasi"] = elem[1]

    for key in word_score:
        word_score[key]["sum_all"] = word_score[key]["Glove_he_she"] + word_score[key]["Glove_bolukbasi"] + \
                                     word_score[key]["fastText_he_she"] + word_score[key]["fastText_bolukbasi"]

    # TODO: save lists in correct format (see beginning of this pipeline)
    # modify the "reader_saver.write_list_to_file" for this

    # Save the dict to a file
    print(word_score)
    for key in word_score:
        print(key, ":")
        for sub_key in word_score[key]:
            print(sub_key, "->", word_score[key][sub_key])
    reader_saver.write_nested_dict_to_file(word_score, sorted(word_score, key=lambda x: word_score[x]["sum_all"]))

    return True


if __name__ == "__main__":
    print("main")
    pipeline_1()
