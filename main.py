# TODO: GloVe model (glove.840B.300d.zip)
# TODO: word2vec GoogleNews model (Bolukbasi)


import spacy
import annoy
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import time
from tqdm import tqdm


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
#vectors = spacy.vectors.Vectors()
#vectors.from_glove("/home/jonas/Documents/GitRepos/PretrainedWordVectors/GloVe840B/")

if __name__ == "__main__":
    # CODE: get number of lines of text file
    count = 0
    for line in open("/home/jonas/Documents/GitRepos/PretrainedWordVectors/glove.6B.300d.txt").readlines():
        count += 1

    # TODO: tutorial -> https://towardsdatascience.com/word-embeddings-with-code2vec-glove-and-spacy-5b26420bf632

    # glove.840B = 2196017
    # glove.6B = 400000
    embeddings_dict = {}
    with open("/home/jonas/Documents/GitRepos/PretrainedWordVectors/glove.6B.300d.txt", 'r', encoding="utf-8") as f:


        for line in tqdm(f.readlines(), desc="finding penis.."):
            values = line.split(" ")
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            embeddings_dict[word] = vector

    if "penis" in embeddings_dict:
        print("Yes, 'penis' is one of the keys in the embeddings_dict dictionary")
        print(embeddings_dict.get("penis"))
