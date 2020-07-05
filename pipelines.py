import gc
import random

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
from misc import get_gender_ranking_vectors, normalize_ranked_words, normalize_sum_all
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
def pipeline_1(word_embeddings_strs: list, word_emb_paths: list = None, word_list: list = None,
               origin_of_word_list: str = None):
    """
    pipeline_1 ranks a word list with two embeddings and writes the results to a runtime specified file

    :param word_emb_paths: list of path to the four wordembeddings to speed up process of ranking
    :param word_embeddings_strs: list of the 4 word_embedding-names
    :param word_list: list of words to be ranked
    :param origin_of_word_list: str where the list of words originates from
    :return: None
    """
    # initialize dict
    word_score = {}

    # Select a word_list if None is given to pipeline_1
    if word_list is None:
        origin, word_list = select_word_list()
    else:
        origin = origin_of_word_list

    for idx, embedding_str in enumerate(word_embeddings_strs, 0):
        embedding_he_she: str = embedding_str + "_heShe"
        embedding_bolukbasi: str = embedding_str + "_boluk"
        # reduce needed RAM space:
        pkl_dict = None
        gc.collect()
        # Load word embedding
        if word_emb_paths is None:
            print("Choose the", embedding_str, "word embedding .PKL you want to load")
            pkl_dict = reader_saver.load_pkl_to_dict()
        else:
            pkl_dict = reader_saver.load_pkl_to_dict(word_emb_paths[idx])
        # get vectors for cosine_distance
        female_vectors, female_vectors_boluk, male_vectors, male_vectors_boluk = get_gender_ranking_vectors(pkl_dict)
        # ranking with he-she and Glove
        print("Ranking with he-she and", embedding_str)
        ranked_words = get_bias_score_matrix(word_list, male_vectors, female_vectors, pkl_dict)
        # normalize ranked words
        ranked_words = normalize_ranked_words(ranked_words)
        print("Ranked words:", ranked_words[0:5])
        print("Dictionary bool is:", bool(word_score))
        for elem in ranked_words:
            if elem[0] not in word_score:
                word_score[elem[0]] = {}
                word_score[elem[0]]["origin"] = origin
            word_score[elem[0]][embedding_he_she] = round(elem[1], 5)
        # ranking with bolukbasi and Glove
        print("Ranking with bolukbasi and", embedding_str)
        ranked_words = get_bias_score_matrix(word_list, male_vectors_boluk, female_vectors_boluk, pkl_dict)
        ranked_words = normalize_ranked_words(ranked_words)
        print("Ranked words:", ranked_words[0:5])
        for elem in ranked_words:
            word_score[elem[0]][embedding_bolukbasi] = round(elem[1], 5)
    # delete all keys which are not present in all word_embeddings
    incomplete_ranking = []
    for key in word_score:
        if len(word_score[key]) < 9:
            incomplete_ranking.append(key)
    # append key+sub_dict to incomplete_word_scores
    # calculate sum of subkeys
    # delete entry from word_score
    incomplete_word_scores = {}
    for key in incomplete_ranking:
        print("Incomplete rankings ::::", key, ":", word_score[key])
        incomplete_word_scores[key] = word_score[key]
        del word_score[key]
        sum_all: float = 0
        for idx, sub_key in enumerate(incomplete_word_scores[key]):
            count = idx
            if sub_key != "origin":
                sum_all += incomplete_word_scores[key][sub_key]
        incomplete_word_scores[key]["sum_all"] = round((sum_all / count), 5)

    # create sum of all scores in sub-dictionary (except for "origin" which is a str)
    for key in word_score:
        sum_all: float = 0
        for idx, sub_key in enumerate(word_score[key]):
            count = idx
            if sub_key != "origin":
                sum_all += word_score[key][sub_key]
        word_score[key]["sum_all"] = round((sum_all / count), 5)

    # word_score = normalize_sum_all(word_score)

    # Save the incomplete rankings
    print("Save the incomplete rankings:")
    save_ranked_words_dict_to_file(incomplete_word_scores)
    # Save the dict to a file
    print("Save the complete rankings:")
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
    print("selects tab separated 2nd position")
    verb_sentences: list = reader_saver.load_verb_sentence_to_list_at_2nd_pos()
    print([sentence for sentence in verb_sentences[0:4]])
    print("Choose the list of occupations you want to load")
    print("selects tab separated 1st position")
    occupations: list = reader_saver.load_nested_list_to_list()
    for elem in occupations:
        elem[1] = elem[1].replace("N", "I")
    print([occupation for occupation in occupations[0:4]])
    # ID: VF01OccF01AdjF01 ->   V for verb, F for gender of verb (F, M), 01 is an incremented int,
    #                           Occ for occupation, F for gender of occupation (F, N, M), 01 is an incremented int,
    finished_sentences = {}
    for sentence_info in verb_sentences:
        sentence: str = sentence_info[0]
        sentence_verb = sentence_info[1]
        sentence_gender = sentence_info[2]
        sentence_number = sentence_info[3]
        id_base: str = "V" + sentence_gender + str(sentence_number).zfill(2)
        for idx_occ, occupation_info in enumerate(occupations):
            if type(occupation_info) is str:
                occupation = occupation_info
                occupation_gender = "OG"
                occupation_number = idx_occ
            else:
                occupation = occupation_info[0]
                occupation_gender = occupation_info[1]
                occupation_number = occupation_info[2]
            id_full: str = id_base + "Occ" + occupation_gender + str(occupation_number).zfill(2)
            sentence_plus_occupation = sentence.replace("XY", occupation)
            finished_sentences[id_full]: dict = {}
            finished_sentences[id_full]["sentence"]: str = sentence_plus_occupation
            finished_sentences[id_full]["verb"]: str = sentence_verb
            finished_sentences[id_full]["occupation"]: str = occupation
    reader_saver.write_nested_dict_to_file(finished_sentences, write_subkeys=False)

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
    print("Choose the WinoBias sentence dataset:")
    winobias_data: [list] = reader_saver.load_nested_list_to_list()
    winobias_data_plus_adj: list = []
    print(winobias_data[0:5])
    print("Choose the list of gender adjectives:")
    adjectives_data: list = reader_saver.load_nested_list_to_list()
    del_obj = adjectives_data.pop(0)
    print("Deleted object from 'adjectives_data':", del_obj)
    print("Choose the list of occupations:")
    occupations_data = reader_saver.load_nested_list_to_list()
    id_count = 1
    for winobias_sub_list in winobias_data:
        occ_splitted = winobias_sub_list[3].split(" ")
        # get gender-class of the occupation
        for occ_sub_list in occupations_data:
            if occ_sub_list[0] == occ_splitted[1]:
                occupation_gender: str = occ_sub_list[1]
        # if "The" or "the -> no manipulation of occ_splitted needed
        if occ_splitted[0] == "The" or occ_splitted[0] == "the":
            for adj_sub_list in adjectives_data:
                winobias_sub_list_plus_adj = list(winobias_sub_list)
                print("Winobias_sub_list:", winobias_sub_list)
                print("Winobias_sub_list_plus_adj:", winobias_sub_list_plus_adj)
                adjective = adj_sub_list[0]
                adj_gender = adj_sub_list[1]
                replacement = occ_splitted[0] + " " + adjective + " " + occ_splitted[1]
                winobias_sub_list_plus_adj[2] = winobias_sub_list_plus_adj[2].replace(winobias_sub_list_plus_adj[3],
                                                                                      replacement)
                winobias_sub_list_plus_adj.append(occupation_gender)
                winobias_sub_list_plus_adj.append(adjective)
                winobias_sub_list_plus_adj.append(adj_gender)
                winobias_sub_list_plus_adj.append(
                    str(id_count).zfill(5) + occ_splitted[1][0:2] + occupation_gender + adjective[0:2] + adj_gender)
                id_count += 1
                winobias_data_plus_adj.append(winobias_sub_list_plus_adj)
        else:
            occ_splitted = winobias_sub_list[3].split(" ")
            # if "a" and adj starts with vocal -> an
            for adj_sub_list in adjectives_data:
                winobias_sub_list_plus_adj = list(winobias_sub_list)
                adjective = adj_sub_list[0]
                adj_gender = adj_sub_list[1]
                if adjective.startswith("a") or adjective.startswith("e"):
                    replacement = "an" + " " + adjective + " " + occ_splitted[1]
                    winobias_sub_list_plus_adj[2] = winobias_sub_list_plus_adj[2].replace(winobias_sub_list_plus_adj[3],
                                                                                          replacement)
                    winobias_sub_list_plus_adj.append(occupation_gender)
                    winobias_sub_list_plus_adj.append(adjective)
                    winobias_sub_list_plus_adj.append(adj_gender)
                    winobias_sub_list_plus_adj.append(
                        str(id_count).zfill(5) + occ_splitted[1][0:2] + occupation_gender + adjective[0:2] + adj_gender)
                    id_count += 1
                    winobias_data_plus_adj.append(winobias_sub_list_plus_adj)

                else:
                    replacement = "a" + " " + adjective + " " + occ_splitted[1]
                    winobias_sub_list_plus_adj[2] = winobias_sub_list_plus_adj[2].replace(winobias_sub_list_plus_adj[3],
                                                                                          replacement)
                    winobias_sub_list_plus_adj.append(occupation_gender)
                    winobias_sub_list_plus_adj.append(adjective)
                    winobias_sub_list_plus_adj.append(adj_gender)
                    winobias_sub_list_plus_adj.append(
                        str(id_count).zfill(5) + occ_splitted[1][0:2] + occupation_gender + adjective[0:2] + adj_gender)
                    id_count += 1
                    winobias_data_plus_adj.append(winobias_sub_list_plus_adj)
    for i in range(20):
        print("Random sub list from winobias_data_plus_adj", i, ":")
        print(random.choice(winobias_data_plus_adj))
    reader_saver.write_nested_list_to_file(winobias_data_plus_adj)
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
