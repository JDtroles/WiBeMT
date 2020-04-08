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


def fasterclosest(input_vectors, query):
    ranks = np.dot(query, input_vectors.T) / np.sqrt(np.sum(input_vectors ** 2, 1))
    most_similar = []
    [most_similar.append(idx) for idx in ranks.argsort()[::-1]]
    return most_similar


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
        if word in word_embedding:
            tuples_word_rank.append([word, get_bias_score(word, male_words, female_words, word_embedding, cosine)])
    return tuples_word_rank


def get_min_or_max_values(tuples, n, min):
    tuples.sort(key=lambda tup: tup[1])
    if min:
        return tuples[:n]
    else:
        return tuples[(len(tuples) - n):]


def save_dict_to_pkl(dict, path):
    # Store data (serialize)
    with open(path, 'wb') as handle:
        pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)


def load_pkl_to_dict(path):
    # Load data (deserialize)
    with open(path, 'rb') as handle:
        unserialized_data = pickle.load(handle)
    return unserialized_data


def load_txt_to_dict(path):
    embeddings_dict = {}
    with open(path, 'r', encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Creating dictionary: "):
            values = line.split(" ")
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            embeddings_dict[word] = vector
    return embeddings_dict


def load_vocab_to_list(path):
    vocab_list = []
    with open(path, 'r', encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Creating vocab list: "):
            values = line.split(" ")
            word = values[1]
            vocab_list.append(word.rstrip())
    return vocab_list


# TODO: fix bolukbasi sorting function
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


if __name__ == "__main__":
    adjectives_list = load_vocab_to_list("/home/jonas/Documents/GitRepos/Words/Adjectives.txt")
    verbs_list = load_vocab_to_list("/home/jonas/Documents/GitRepos/Words/Verbs.txt")

    print(len(adjectives_list))
    print(adjectives_list[0:10])
    print(len(verbs_list))
    print(verbs_list[0:10])

    # TODO: tutorial -> https://towardsdatascience.com/word-embeddings-with-code2vec-glove-and-spacy-5b26420bf632

    # glove.840B = 2196017
    # glove.6B = 400000

    # embeddings_dict = load_txt_to_dict("/home/jonas/Documents/GitRepos/PretrainedWordVectors/crawl-300d-2M.vec")

    pkl_path_6B = "/home/jonas/Documents/GitRepos/PretrainedWordVectors/glove.6B.300d.pickle"
    pkl_path_840B = "/home/jonas/Documents/GitRepos/PretrainedWordVectors/glove.840B.300d.pickle"
    pkl_path_crawl = "/home/jonas/Documents/GitRepos/PretrainedWordVectors/crawl.?.300d.pickle"

    start_time = time.time()
    # save_dict_to_pkl(embeddings_dict, pkl_path_crawl)
    duration = time.time() - start_time
    print("You dumped the pickle in ", duration, " seconds!")

    start_time = time.time()
    pkl_dict = load_pkl_to_dict(pkl_path_840B)
    duration = time.time() - start_time
    print("You loaded the pickle in ", duration, " seconds!")

    female_list_long = ["she", "hers", "her", "woman", "women", "mother", "female", "vulva"]
    male_list_long = ["he", "his", "him", "man", "men", "father", "male", "penis"]
    female_list = ["she"]
    male_list = ["he"]

    gender_list = ["lads", "lion", "gentleman", "fraternity", "bachelor", "niece", "bulls", "husbands", "prince",
                   "colt", "salesman", "hers", "dude", "beard", "filly", "princess", "lesbians", "councilman",
                   "actresses", "gentlemen", "stepfather", "monks", "lad", "sperm", "testosterone", "nephews",
                   "acknowledge", "acquaint", "acquiesce", "acquire", "acquit", "act", "activate", "actualize", "adapt",
                   "add", "address", "adhere", "adjoin", "adjourn", "adjudicate", "adjust", "administer",
                   "administrate", "admire", "admit", "admonish", "adopt", "adore", "adorn", "adsorb", "adulate",
                   "advance", "advertise"]

    # bolukbasi_male_list = ['he', 'his', 'him', 'man', 'men', 'spokesman', 'himself', 'son', 'father', 'guy', 'boy',
    #                        'boys', 'brother', 'male', 'brothers', 'dad', 'sons', 'king', 'businessman', 'grandfather',
    #                        'deer', 'uncle', 'congressman', 'grandson', 'bull', 'businessmen', 'nephew', 'fathers',
    #                        'lads', 'lion', 'gentleman', 'fraternity', 'bachelor', 'bulls', 'prince', 'colt', 'salesman',
    #                        'dude', 'beard', 'councilman', 'gentlemen', 'stepfather', 'monks', 'lad', 'testosterone',
    #                        'nephews', 'daddy', 'kings', 'sir', 'stud', 'lions', 'gelding', 'czar', 'countrymen',
    #                        'penis', 'bloke', 'spokesmen', 'monastery', 'brethren', 'schoolboy', 'brotherhood',
    #                        'stepson', 'uncles', 'monk', 'viagra', 'macho', 'statesman', 'fathered', 'blokes', 'dudes',
    #                        'strongman', 'grandsons', 'studs', 'godfather', 'boyhood', 'baritone', 'grandpa',
    #                        'countryman', 'stallion', 'fella', 'chap', 'widower', 'salesmen', 'beau', 'beards',
    #                        'handyman', 'horsemen', 'fatherhood', 'princes', 'colts', 'ma', 'fraternities', 'pa',
    #                        'fellas', 'councilmen', 'barbershop', 'fraternal']
    # bolukbasi_female_list = []

    bolukbasi_female_list, bolukbasi_male_list = sort_bolukbasi_gender_list("/home/jonas/Documents/GitRepos/Words/GenderWordsBolukbasi.txt", female_list_long, male_list_long, pkl_dict)

    print("Female list:")
    for elem in bolukbasi_female_list:
        string = "'" + elem + "'"
        print(string.strip(), end=", ")

    print("Male list: ")
    for elem in bolukbasi_male_list:
        string = "'" + elem + "'"
        print(string.strip(), end=", ")

    evaluated_adjectives = evaluate_words_for_gender(adjectives_list, male_list, female_list, pkl_dict, True)
    evaluated_verbs = evaluate_words_for_gender(verbs_list, male_list, female_list, pkl_dict, True)
    evaluated_words = evaluate_words_for_gender(list(pkl_dict.keys()), male_list, female_list, pkl_dict, True)
    print("Female verbs: ")
    for word in get_min_or_max_values(evaluated_verbs, 20, True):
        print(word)
    print("Male verbs: ")
    for word in get_min_or_max_values(evaluated_verbs, 20, False):
        print(word)
    print("Female adjectives: ")
    for word in get_min_or_max_values(evaluated_adjectives, 20, True):
        print(word)
    print("Male adjectives: ")
    for word in get_min_or_max_values(evaluated_adjectives, 20, False):
        print(word)
    print("Get all gender Female words: ")
    for word in get_min_or_max_values(evaluated_words, 20, True):
        print(word)
    print("Get all gender Male words: ")
    for word in get_min_or_max_values(evaluated_words, 20, False):
        print(word)

    # if "penis" in embeddings_dict:
    #     print("Yes, 'penis' is one of the keys in the embeddings_dict dictionary")
    #     print(embeddings_dict.get("penis"))
    #
    # for elem in gender_list:
    #     print(elem)
    #     print(get_bias_score(elem, male_list, female_list, embeddings_dict))

    # print("Penis neighbours in embeddings_dict", closest(embeddings_dict, embeddings_dict.get("penis")))
    # print("Penis neighbours in pkl_dict", closest(pkl_dict, pkl_dict.get("penis")))
