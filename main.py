# TODO: GloVe model (glove.840B.300d.zip)
# TODO: word2vec GoogleNews model (Bolukbasi)


# import spacy
# import annoy
import numpy as np
import time

import reader_saver
import plotter
# import spacy_functions
from evaluator import get_bias_score_matrix
from getter import get_plotting_word_list


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


# TODO: CREATE FUNCTION TO GET PLOTTER WORDS
# 1st: rank words by bolukbasi-lists
# 2nd: rank words by he - she
# 3rd: return list: [[he-she-value, bolukbasi-value, "word"], ...]


def pipeline() -> bool:
    # initialize dict
    word_score = dict()


    # Load word list
    start_time = time.time()
    pkl_dict = reader_saver.load_pkl_to_dict()
    duration = time.time() - start_time
    print("You loaded the pickle in ", duration, " seconds!")

    # he / she as word lists
    male_words = ["he"]
    female_words = ["she"]

    male_vectors = np.array([pkl_dict.get(male_word) for male_word in male_words])
    female_vectors = np.array([pkl_dict.get(female_word) for female_word in female_words])

    adjectives = reader_saver.load_vocab_to_list_at_2nd_pos()

    ranked_words = get_bias_score_matrix(adjectives, male_vectors, female_vectors, pkl_dict)

    reader_saver.write_list_to_file(sorted(ranked_words, key=lambda x: x[1]))

    breakpoint()


if __name__ == "__main__":
    # occupations_list_WinoBias = get_occupations("/home/jonas/Documents/GitRepos/Words/WinoBias.txt")
    # get_unique_sentences("/home/jonas/Documents/GitRepos/Words/WinoBias.txt", occupations_list_WinoBias)
    # get_occupations("/home/jonas/Documents/GitRepos/Words/Sentences_Occupations_Stanovsky.txt")

    start_time = time.time()
    pkl_dict = reader_saver.load_pkl_to_dict()
    duration = time.time() - start_time
    print("You loaded the pickle in ", duration, " seconds!")

    # he / she as word lists
    male_words = ["he"]
    female_words = ["she"]

    male_vectors = np.array([pkl_dict.get(male_word) for male_word in male_words])
    female_vectors = np.array([pkl_dict.get(female_word) for female_word in female_words])

    adjectives = reader_saver.load_vocab_to_list_at_2nd_pos()

    ranked_words = get_bias_score_matrix(adjectives, male_vectors, female_vectors, pkl_dict)

    reader_saver.write_list_to_file(sorted(ranked_words, key=lambda x: x[1]))

    breakpoint()


    adjectives = reader_saver.load_vocab_to_list_at_1st_pos()
    print(adjectives)

    start_time = time.time()
    pkl_dict = reader_saver.load_pkl_to_dict()
    duration = time.time() - start_time
    print("You loaded the pickle in ", duration, " seconds!")

    plotter.create_word_map(get_plotting_word_list(adjectives, pkl_dict))

    breakpoint()

    adj_for_sentences = reader_saver.load_vocab_to_list_at_1st_pos()

    # add_adj_to_sentences("/home/jonas/Documents/GitRepos/Words/WinoBias.txt", adj_for_sentences)

    breakpoint()

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

    adjectives = reader_saver.load_vocab_to_list_at_2nd_pos()
    results = []


    '''    run_pool(strategy=concurrent.futures.ThreadPoolExecutor,
             max_workers=4,
             comp_word_list=adjectives,
             male_list = ["he"],
             fem_list = ["she"],
             word_emb=pkl_dict,
             cosine=True)
    '''