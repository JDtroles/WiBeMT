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


def pipeline_0():
    """
    pipeline_0 loads a word_embedding from .txt / .vec and saves it as .pkl

    :return: None
    """
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
                word_embedding = reader_saver.load_txt_to_dict()

                break
        except ValueError:
            print("Please enter an int between 1 - 2")

    # save word_embedding to .pkl file
    reader_saver.save_dict_to_pkl(word_embedding)
    return


#####
# 1 #
#####
# pipeline_1 ranks words and saves them as a dict with the following format:
# word -> origin -> emb_1_he_she -> emb_1_boluk -> emb_2_he_she -> emb_2_boluk
def pipeline_1(embedding_1: str, embedding_2: str, word_list: list = None, origin_of_word_list: str = None):
    """
    pipeline_1 ranks a word list with two embeddings and writes the results to a runtime specified file

    :param embedding_1: str of Embedding 1 one wants to load
    :param embedding_2: str of Embedding 2 one wants to load
    :param word_list: list of words to be ranked
    :param origin_of_word_list: str where the list of words originates from
    :return: None
    """
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
    pkl_dict = None
    gc.collect()
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

    return


#####
# 2 #
#####
# pipeline_2
# IN: verb_sentence_skeletons & occupations
# TASK 1: create full sentences from input data
# TASK 2: write sentences structured into list
# OUT: write sentence list to file
def pipeline_2():
    """
    loads verb_sentence_skeletons, occupations, adjectives

    creates finished sentences

    saves those sentences

    :return: None
    """
    print("Choose the verb sentences file you want to use.")
    verb_sentences: list = reader_saver.load_verb_sentence_to_list_at_2nd_pos()
    print("Choose the list of occupations you want to load")
    occupations: list = reader_saver.load_vocab_to_list_at_1st_pos()
    print("Choose list of adjectives you want to load.")
    adjectives: list = reader_saver.load_vocab_to_list_at_1st_pos()
    # ID: VF01OccF01AdjF01 ->   V for verb, F for gender of verb (F, M), 01 is an incremented int,
    #                           Occ for occupation, F for gender of occupation (F, N, M), 01 is an incremented int,
    #                           Adj for adjective, F for gender of adjective (F, M), 01 is an incremented int
    finished_sentences = {}
    for sentence_info in verb_sentences:
        sentence: str = sentence_info[0]
        sentence_verb = sentence_info[1]
        sentence_gender = sentence_info[2]
        sentence_number = sentence_info[3]
        id_base: str = "V" + sentence_gender + str(sentence_number).zfill(2)
        for occupation_info in occupations:
            occupation = occupation_info[0]
            occupation_gender = occupation_info[1]
            occupation_number = occupation_info[2]
            id_base_2: str = id_base + "Occ" + occupation_gender + str(occupation_number)
            sentence_plus_occupation = sentence.replace("XY", occupation)
            no_adj_id = id_base_2 + "AdjNone"
            finished_sentences[no_adj_id]: dict = {}
            finished_sentences[no_adj_id]["sentence"]: str = sentence_plus_occupation
            finished_sentences[no_adj_id]["verb"]: str = sentence_verb
            finished_sentences[no_adj_id]["occupation"]: str = occupation
            finished_sentences[no_adj_id]["adjective"]: str = None
            for adjectives_info in adjectives:
                adjective = adjectives_info[0]
                adjective_gender = adjectives_info[1]
                adjective_number = adjectives_info[2]
                full_id = no_adj_id + "Adj" + adjective_gender + str(adjective_number)
                replacement = adjective + " " + occupation
                sentence_plus_adj = sentence.replace(occupation, replacement)
                finished_sentences[full_id]: dict = {}
                finished_sentences[full_id]["sentence"]: str = sentence_plus_adj
                finished_sentences[full_id]["verb"]: str = sentence_verb
                finished_sentences[full_id]["occupation"]: str = occupation
                finished_sentences[full_id]["adjective"]: str = adjective
    # TODO: write dict to file

    return


#####
# 3 #
#####
# pipeline_3
# IN:
# TASK 1:
# TASK 2:
# OUT:
def pipeline_3():
    # TODO: Implement
    return


#####
# 4 #
#####
# pipeline_4
# IN:
# TASK 1:
# TASK 2:
# OUT:
def pipeline_4():
    # TODO: Implement
    return
