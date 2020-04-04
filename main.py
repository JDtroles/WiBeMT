# TODO: GloVe model (glove.840B.300d.zip)
# TODO: word2vec GoogleNews model (Bolukbasi)


import spacy
import annoy
import numpy as np
import math
from tqdm import tqdm
import pickle
import time

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

def distance(coord1, coord2):
    # note, this is VERY SLOW, don't use for actual code
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


def get_bias_score(word, male_words, female_words, word_embedding):
    if word in word_embedding:
        male_sum = 0
        for elem in male_words:
            male_sum += distance(word_embedding.get(word), word_embedding.get(elem))
        female_sum = 0
        for elem in female_words:
            female_sum += distance(word_embedding.get(word), word_embedding.get(elem))
        return male_sum - female_sum
    else:
        print(word, " is not in the dictionary.")
        return None

def save_dict_to_pkl(dict, path):
    # Store data (serialize)
    with open(path, 'wb') as handle:
        pickle.dump(dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load_pkl_to_dict(path):
    # Load data (deserialize)
    with open(path, 'rb') as handle:
        unserialized_data = pickle.load(handle)
    return unserialized_data


if __name__ == "__main__":
    # CODE: get number of lines of text file
    count = 0
    for line in open("/home/jonas/Documents/GitRepos/PretrainedWordVectors/glove.6B.300d.txt").readlines():
        count += 1

    # TODO: tutorial -> https://towardsdatascience.com/word-embeddings-with-code2vec-glove-and-spacy-5b26420bf632

    # glove.840B = 2196017
    # glove.6B = 400000
    embeddings_dict = {}
    with open("/home/jonas/Documents/GitRepos/PretrainedWordVectors/glove.840B.300d.txt", 'r', encoding="utf-8") as f:

        for line in tqdm(f.readlines(), desc="Creating dictionary: "):
            values = line.split(" ")
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            embeddings_dict[word] = vector

    pkl_path = "/home/jonas/Documents/GitRepos/PretrainedWordVectors/pkl_Test_small.pickle"

    start_time = time.time()
    save_dict_to_pkl(embeddings_dict, pkl_path)
    duration = time.time() - start_time
    print("You dumped the pickle in ", duration, " seconds!")

    start_time = time.time()
    pkl_dict = load_pkl_to_dict(pkl_path)
    duration = time.time() - start_time
    print("You loaded the pickle in ", duration, " seconds!")

    female_list = ["she", "hers", "her", "woman", "women", "mother", "female", "vulva"]
    male_list = ["he", "his", "him", "man", "men", "father", "male", "penis"]

    gender_list = ["lads", "lion", "gentleman", "fraternity", "bachelor", "niece", "bulls", "husbands", "prince",
                   "colt", "salesman", "hers", "dude", "beard", "filly", "princess", "lesbians", "councilman",
                   "actresses", "gentlemen", "stepfather", "monks", "lad", "sperm", "testosterone", "nephews",
                   "acknowledge", "acquaint", "acquiesce", "acquire", "acquit", "act", "activate", "actualize", "adapt",
                   "add", "address", "adhere", "adjoin", "adjourn", "adjudicate", "adjust", "administer",
                   "administrate", "admire", "admit", "admonish", "adopt", "adore", "adorn", "adsorb", "adulate",
                   "advance", "advertise"]

    if "penis" in embeddings_dict:
        print("Yes, 'penis' is one of the keys in the embeddings_dict dictionary")
        print(embeddings_dict.get("penis"))

    for elem in gender_list:
        print(elem)
        print(get_bias_score(elem, male_list, female_list, embeddings_dict))

    if "penis" in pkl_dict:
        print("Yes, 'penis' is one of the keys in the pkl_dict dictionary")
        print(pkl_dict.get("penis"))

    for elem in gender_list:
        print(elem)
        print(get_bias_score(elem, male_list, female_list, pkl_dict))

    print("Penis neighbours in embeddings_dict", closest(embeddings_dict, embeddings_dict.get("penis")))
    print("Penis neighbours in pkl_dict", closest(pkl_dict, pkl_dict.get("penis")))
