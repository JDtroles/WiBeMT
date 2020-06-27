import gc

import reader_saver
from evaluator import get_bias_score_matrix


################
# PIPELINES... #
################
# ...that implement one step of workflow from loading data to saving data

#####
# 0 #
#####
# pipeline_0 loads word_embedding files into dictionaries and saves those as a .pkl file
from misc import get_gender_ranking_vectors
from reader_saver import save_ranked_words_dict_to_file, select_word_list


def pipeline_0() -> bool:
    print("Ckhoose the word embedding type you want to load:")
    print("GloVe = 1")
    print("fastText = 2")
    while True:
        try:
            embedding_type_int = int(input("Enter the corresponding number:"))
            if embedding_type_int < 1 or embedding_type_int > 2:
                raise ValueError
            elif embedding_type_int == 1:
                # load GloVe
                print("You chose to load a GloVe word embedding")
                print("Now choose the corresponding GloVe file in .txt format")
                word_embedding = reader_saver.load_txt_to_dict()
                break
            elif embedding_type_int == 2:
                # load fastText
                print("You chose to load a fastText word embedding")
                print("Now choose the corresponding fastText file in .vec format")
                word_embedding = reader_saver.load_fasttext_vectors()

                break
        except ValueError:
            print("Please enter an int between 1 - 2")

    # save word_embedding to .pkl file
    reader_saver.save_dict_to_pkl(word_embedding)
    return True

#####
# 1 #
#####
# pipeline_1 ranks words and saves them as a dict with the following format:
# word -> origin -> emb_1_he_she -> emb_1_boluk -> emb_2_he_she -> emb_2_boluk
def pipeline_1(embedding_1: str, embedding_2: str, word_list: list = None, origin_of_word_list: str = None) -> bool:
    # initialize dict
    word_score = {}
    embedding_1_he_she: str = embedding_1 + "_he_she"
    embedding_1_bolukbasi: str = embedding_1 + "_bolukbasi"
    embedding_2_he_she: str = embedding_2 + "_he_she"
    embedding_2_bolukbasi: str = embedding_2 + "_bolukbasi"


    # Load word embedding 1
    print("Choose the", embedding_1, "word embedding .PKL you want to load")
    pkl_dict = reader_saver.load_pkl_to_dict()

    female_vectors, female_vectors_boluk, male_vectors, male_vectors_boluk = get_gender_ranking_vectors(pkl_dict)

    # Select a word_list if None is given to pipeline_1
    if word_list is None:
        origin, word_list = select_word_list()
    else:
        origin = origin_of_word_list

    # ranking with he-she and Glove
    print("Ranking with he-she and", embedding_1)
    ranked_words = get_bias_score_matrix(word_list, male_vectors, female_vectors, pkl_dict)
    for elem in ranked_words:
        word_score[elem[0]] = {}
        word_score[elem[0]]["origin"] = origin
        word_score[elem[0]][embedding_1_he_she] = elem[1]
        if elem[1] < 0:
            word_score[elem[0]][embedding_1_bolukbasi] = -99
            word_score[elem[0]][embedding_2_he_she] = -99
            word_score[elem[0]][embedding_2_bolukbasi] = -99
        else:
            word_score[elem[0]][embedding_1_bolukbasi] = 99
            word_score[elem[0]][embedding_2_he_she] = 99
            word_score[elem[0]][embedding_2_bolukbasi] = 99

    # ranking with bolukbasi and Glove
    print("Ranking with bolukbasi and", embedding_1)
    ranked_words = get_bias_score_matrix(word_list, male_vectors_boluk, female_vectors_boluk, pkl_dict)
    for elem in ranked_words:
        word_score[elem[0]][embedding_1_bolukbasi] = elem[1]

    # Load word embedding 2
    print("Choose the", embedding_2, "word embedding .PKL you want to load")
    # pkl_dict = None
    # gc.collect()
    pkl_dict = reader_saver.load_pkl_to_dict()

    # get new vectors from new word embedding
    female_vectors, female_vectors_boluk, male_vectors, male_vectors_boluk = get_gender_ranking_vectors(pkl_dict)


    # ranking with he-she and fastText
    print("Ranking with he-she and ", embedding_2)
    ranked_words = get_bias_score_matrix(word_list, male_vectors, female_vectors, pkl_dict)
    for elem in ranked_words:
        if elem[0] in word_score:
            word_score[elem[0]][embedding_2_he_she] = elem[1]
        else:
            word_score[elem[0]] = {}
            word_score[elem[0]]["origin"] = origin
            if elem[1] < 0:
                word_score[elem[0]][embedding_1_he_she] = -99
                word_score[elem[0]][embedding_1_bolukbasi] = -99
            else:
                word_score[elem[0]][embedding_1_he_she] = 99
                word_score[elem[0]][embedding_1_bolukbasi] = 99
            word_score[elem[0]][embedding_2_he_she] = elem[1]


    # ranking with bolukbasi and fastText
    print("Ranking with bolukbasi and ", embedding_2)
    ranked_words = get_bias_score_matrix(word_list, male_vectors_boluk, female_vectors_boluk, pkl_dict)
    for elem in ranked_words:
        word_score[elem[0]][embedding_2_bolukbasi] = elem[1]

    for key in word_score:
        word_score[key]["sum_all"] = word_score[key][embedding_1_he_she] + word_score[key][embedding_1_bolukbasi] + \
                                     word_score[key][embedding_2_he_she] + word_score[key][embedding_2_bolukbasi]

    # Save the dict to a file
    save_ranked_words_dict_to_file(word_score)

    return True


#####
# 2 #
#####
# pipeline_2
# IN: verb_sentence_skeletons & gender_verbs & occupations
# TASK 1: create full sentences from input data
# TASK 2: write sentences structured into list
# OUT: write sentence list to file
def pipeline_2():

    return
