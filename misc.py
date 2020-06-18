from tqdm import tqdm

from evaluator import get_bias_score


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