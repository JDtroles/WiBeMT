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
import re
from string import digits
"""Translates text into the target language.

Target must be an ISO 639-1 language code.
See https://g.co/cloud/translate/v2/translate-reference#supported_languages
"""
"""
from google
translate_client = translate.Client()

if isinstance(text, six.binary_type):
    text = text.decode('utf-8')

# Text can also be a sequence of strings, in which case this method
# will return a sequence of results for each text.
result = translate_client.translate(
    text, target_language=target)

print(u'Text: {}'.format(result['input']))
print(u'Translation: {}'.format(result['translatedText']))
print(u'Detected source language: {}'.format(
    result['detectedSourceLanguage']))
    """

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


def get_occupations(path):
    occupations = set()
    with open(path, 'r', encoding="utf-8") as f:
        for line in f:
            values = line.split("\t")
            occu = values[3].replace("the ", "")
            occu = occu.replace("The ", "")
            occu = occu.replace("a ", "")
            occu = occu.replace("an ", "")
            occupations.add(re.sub(r"\s+", "", occu, flags=re.UNICODE))
    occupations_list = list(occupations)
    occupations_list.sort()
    with open("/home/jonas/Documents/GitRepos/Words/occupations_WinoMT.txt", "w") as f:
        for elem in occupations_list:
            f.write(elem)
            f.write("\n")
    print("Occupations:", len(occupations_list), "\n", occupations_list)
    return occupations_list


def get_sentences(path_sentences, occu_list):
    sentences_set = set()
    with open(path_sentences, 'r', encoding="utf-8") as f:
        for line in f:
            values = line.split("\t")
            occupation = values[3].replace("the ", "").replace("The ", "").replace("a ", "").replace("an ", "").rstrip()
            sentence = values[2].replace(occupation, "X")
            for elem in occu_list:
                sentence = sentence.replace(elem, "Y")
            # she, he = X1; her, his = X2; her, him = X3
            gender_pronoun_space = [" she ", " he ", " her ", " him ", " his "]
            for elem in gender_pronoun_space:
                sentence = sentence.replace(elem, " X1 ")
            gender_pronoun_dot = [" she.", " he.", " her.", " him.", " his."]
            for elem in gender_pronoun_dot:
                sentence = sentence.replace(elem, " X1.")
            sentences_set.add(sentence)
    sentences_list = list(sentences_set)
    sentences_list.sort()
    with open("/home/jonas/Documents/GitRepos/Words/sentences_WinoBias.txt", "w") as f:
        for elem in sentences_list:
            f.write(elem)
            f.write("\n")
    print("Unique sentences:", len(sentences_list), "\n", sentences_list)

def add_adj_to_sentences(path_sentences, adj_list):
    with open(path_sentences, "r", encoding="utf-8") as f:
        replace_list = ["The ", "the "]
        adj_sentences = []
        for line in f:
            values = line.split("\t")
            occupation = values[3].replace("The ", "").replace("the ", "")
            print(occupation)
            sentence = values[2]
            print(sentence)
            for adj in adj_list:
                replacement = adj + " " + occupation
                print(replacement)
                # TODO: FIX REPLACEMENT
                sentence_plus_adj = sentence.replace(occupation, "XYZ")
                print(sentence_plus_adj)
                adj_sentences.append(sentence_plus_adj)




if __name__ == "__main__":
    occupations_list_WinoBias = get_occupations("/home/jonas/Documents/GitRepos/Words/WinoBias.txt")
    get_sentences("/home/jonas/Documents/GitRepos/Words/WinoBias.txt", occupations_list_WinoBias)
    # get_occupations("/home/jonas/Documents/GitRepos/Words/Sentences_Occupations_Stanovsky.txt")

    add_adj_to_sentences("/home/jonas/Documents/GitRepos/Words/WinoBias.txt", ["sassy", "brunette", "gorgeous", "grizzled", "burly", "scruffy"])

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

    bolukbasi_male_list = ['he', 'his', 'him', 'man', 'men', 'spokesman', 'himself', 'son', 'father', 'guy', 'boy',
                           'boys', 'brother', 'male', 'brothers', 'dad', 'sons', 'king', 'businessman', 'grandfather',
                           'uncle', 'congressman', 'grandson', 'bull', 'businessmen', 'nephew', 'fathers',
                           'lads', 'lion', 'gentleman', 'fraternity', 'bachelor', 'bulls', 'prince', 'colt', 'salesman',
                           'dude', 'beard', 'councilman', 'gentlemen', 'stepfather', 'monks', 'lad', 'testosterone',
                           'nephews', 'daddy', 'kings', 'sir', 'stud', 'lions', 'gelding', 'czar', 'countrymen',
                           'penis', 'bloke', 'spokesmen', 'monastery', 'brethren', 'schoolboy', 'brotherhood',
                           'stepson', 'uncles', 'monk', 'viagra', 'macho', 'statesman', 'fathered', 'blokes', 'dudes',
                           'strongman', 'grandsons', 'studs', 'godfather', 'boyhood', 'baritone', 'grandpa',
                           'countryman', 'stallion', 'fella', 'chap', 'widower', 'salesmen', 'beau', 'beards',
                           'handyman', 'horsemen', 'fatherhood', 'princes', 'colts', 'fraternities', 'pa',
                           'fellas', 'councilmen', 'barbershop', 'fraternal', 'husband', 'boyfriend', 'males',
                           'husbands', 'sperm', 'fiance', 'suitors', 'prostate', 'paternity', 'suitor', 'hubby',
                           'boyfriends', 'semen']
    bolukbasi_female_list = ['her', 'she', 'women', 'woman', 'wife', 'mother', 'daughter', 'girls', 'girl',
                             'spokeswoman', 'female', 'sister', 'herself', 'actress', 'mom', 'girlfriend', 'daughters',
                             'lady', 'sisters', 'mothers', 'grandmother', 'ladies', 'queen', 'ma',
                             'wives', 'widow', 'bride', 'females', 'aunt', 'lesbian', 'chairwoman', 'moms', 'maiden',
                             'granddaughter', 'niece', 'hers', 'filly', 'princess', 'lesbians', 'actresses',
                             'maid', 'mare', 'fiancee', 'dads', 'waitress', 'maternal', 'heroine',
                             'nieces', 'girlfriends', 'mistress', 'womb', 'grandma', 'maternity', 'estrogen', 'widows',
                             'diva', 'nuns', 'nun', 'brides', 'housewife', 'menopause', 'motherhood',
                             'stepmother', 'hostess', 'fillies', 'congresswoman', 'witch',
                             'sorority', 'businesswoman', 'gal', 'schoolgirl', 'goddess',
                             'stepdaughter', 'uterus', 'mama', 'hens', 'hen', 'mommy', 'grandmothers',
                             'feminism', 'heiress', 'queens', 'witches', 'aunts', 'granddaughters', 'convent',
                             'vagina', 'maids', 'gals', 'housewives', 'obstetrics', 'councilwoman', 'matriarch',
                             'dowry', 'deer']

    bolukbasi_amiguous = ['deer', 'ma', 'husband', 'boyfriend', 'males', 'husbands', 'sperm', 'fiance', 'suitors',
                          'prostate', 'paternity', 'suitor', 'hubby', 'boyfriends', 'semen']

    bolukbasi_female_list, bolukbasi_male_list = sort_bolukbasi_gender_list(
        "/home/jonas/Documents/GitRepos/Words/GenderWordsBolukbasi.txt", female_list_long, male_list_long, pkl_dict)

    print("Female list:")
    for elem in bolukbasi_female_list:
        string = "'" + elem + "'"
        print(string.strip(), end=", ")

    print("\n", "Male list: ")
    for elem in bolukbasi_male_list:
        string = "'" + elem + "'"
        print(string.strip(), end=", ")

    with open("/home/jonas/Documents/GitRepos/Words/GenderWordsBolukbasi.txt", 'r', encoding="utf-8") as f:
        bolukbasi_base = []
        for line in tqdm(f.readlines(), desc="Creating vocab list: "):
            values = line.split(", ")
            for word in values:
                bolukbasi_base.append(word)

    print("\n", "Bolukbasi list: \n", evaluate_words_for_gender(bolukbasi_base, male_list, female_list, pkl_dict, True))

    evaluated_adjectives = evaluate_words_for_gender(adjectives_list, bolukbasi_male_list, bolukbasi_female_list, pkl_dict, True)
    evaluated_verbs = evaluate_words_for_gender(verbs_list, bolukbasi_male_list, bolukbasi_female_list, pkl_dict, True)
    evaluated_occupations_WinoBias = evaluate_words_for_gender(occupations_list_WinoBias, bolukbasi_male_list, bolukbasi_female_list, pkl_dict, True)
    print("Female Occupations: ")
    for word in get_min_or_max_values(evaluated_occupations_WinoBias, 20, True):
        print(word)
    print("Male Occupations: ")
    for word in get_min_or_max_values(evaluated_occupations_WinoBias, 20, False):
        print(word)
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

    # evaluated_words = evaluate_words_for_gender(list(pkl_dict.keys()), bolukbasi_male_list, bolukbasi_female_list, pkl_dict, True)
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
