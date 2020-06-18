from evaluator import distance


def closest(space, coord, n=10):
    closest = []
    for key in sorted(space.keys(),
                      key=lambda x: distance(coord, space[x]))[:n]:
        closest.append(key)
    return closest




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

'''    # some fancy multithreading..
chunk_size = 5000
executor = concurrent.futures.ThreadPoolExecutor()
futures = []
for list_part in tqdm(split_list_equally(adjectives, chunk_size), desc="Get scoring of words: "):
    futures.append(executor.submit(get_bias_score_matrix, list_part, male_vectors, female_vectors, pkl_dict, True))

bias_score_dict = {}
for future in tqdm(futures, desc="working.."):
    bias_score_dict.update(future.result())

breakpoint()'''
'''
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    for list_part in tqdm(split_list_equally(adjectives, 500), desc="Get scoring of words: "):
        future = executor.submit(get_bias_score(list_part, ["he"], ["she"], pkl_dict, True))
        result = future.result()
        print(result)
'''

'''
nlp = spacy_functions.NLPWorker()
adjectives = []
verbs = []
for dict_part in tqdm(split_dict_equally(pkl_dict), desc="Tagging words: "):
    adj, ver = nlp.get_adj_verbs(dict_part)
    adjectives.append(adj)
    verbs.append(ver)
reader_saver.write_list_to_file(adjectives)
reader_saver.write_list_to_file(verbs)
'''

#    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
#        for dict_part in tqdm(split_dict_equally(pkl_dict), desc="Multithreadingtest: "):
#            future = executor.submit(nlp.get_adj_verbs(dict_part))
#            print(future)

# for item in split_dict_equally(pkl_dict):
#    print(len(item))

# for word_list in spacy_functions.get_adj_verbs(pkl_dict):
#    reader_saver.write_list_to_file(word_list)

'''
evaluated_words = evaluate_words_for_gender(list(pkl_dict.keys()), bolukbasi_male_list, bolukbasi_female_list, pkl_dict, True)
print("Get all gender Female words: ")
for word in get_min_or_max_values(evaluated_words, 20, True):
    print(word)
print("Get all gender Male words: ")
for word in get_min_or_max_values(evaluated_words, 20, False):
    print(word)
'''

# if "penis" in embeddings_dict:
#     print("Yes, 'penis' is one of the keys in the embeddings_dict dictionary")
#     print(embeddings_dict.get("penis"))
#
# for elem in gender_list:
#     print(elem)
#     print(get_bias_score(elem, male_list, female_list, embeddings_dict))

# print("Penis neighbours in embeddings_dict", closest(embeddings_dict, embeddings_dict.get("penis")))
# print("Penis neighbours in pkl_dict", closest(pkl_dict, pkl_dict.get("penis")))


# Long word lists
male_words = word_lists.get_bolukbasi_male_list()
female_words = word_lists.get_bolukbasi_female_list()

# he / she as word lists
# male_words = ["he"]
# female_words = ["she"]

male_vectors = np.array([pkl_dict.get(male_word) for male_word in male_words])
female_vectors = np.array([pkl_dict.get(female_word) for female_word in female_words])

# score1 = get_bias_score_matrix(adjectives, male_vectors, female_vectors, pkl_dict, True)
# score2 = get_bias_score(adjectives, male_words, female_words, pkl_dict, True)
# print(score1)
# print(score2)
# breakpoint()


# some single threading..
chunk_size = 3000
split = split_list_equally(adjectives, chunk_size)
bias_scores = []
for list_part in tqdm(split, desc="Get scoring of words: ", total=len(adjectives) // chunk_size):
    for result in get_bias_score_matrix(list_part, male_vectors, female_vectors, pkl_dict, True):
        bias_scores.append(result)
        # print(result)

sorted_bias_scores = sorted(bias_scores, key=lambda x: x[1])
# print("Highest Scores: ")
# print([elem for elem in sorted_bias_scores[0:1000]])
reader_saver.write_list_to_file(sorted_bias_scores[0:100])

# print("Lowest Scores: ")
# print([elem for elem in sorted_bias_scores[len(sorted_bias_scores) - 1000:]])
reader_saver.write_list_to_file(sorted_bias_scores[len(sorted_bias_scores) - 100:])


'''def run_pool(*, strategy, max_workers=4, comp_word_list=[], male_list=[], fem_list=[], word_emb={}, cosine=True):
    start = time.time()
    with strategy(max_workers=max_workers) as executor:
        result = executor.map(get_bias_score, comp_word_list, male_list, fem_list, word_emb, cosine)
        end = time.time()
    print(f'\nTime to complete using {strategy}, with {max_workers} workers: {end - start:.2f}s\n')

    print(result) # returns an iterator
    print(list(result))'''