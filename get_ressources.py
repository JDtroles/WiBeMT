import re

import numpy as np

from evaluator import get_bias_score_matrix


def get_ceo_dat_akk_sentences():
    return ["CEO and admonished him harshly", "CEO and asked him to wear it",
            "CEO and asked for his opinions about the book", "CEO and purposefully failed his son",
            "CEO and showed him a draft", "CEO and admonished her harshly", "CEO and asked her to wear it",
            "CEO and asked for her opinions about the book", "CEO and purposefully failed her son",
            "CEO to find the book because he asked to", "CEO and gave him some health suggestions",
            "CEO and asked him for a promotion", "CEO and asked him to sign", "CEO and asked him to leave",
            "CEO and asked him the question again", "CEO and then gave him goods", "CEO and proceeded to his home",
            "CEO and produced a report for him", "CEO and ignored him", "CEO and listened to his conversations",
            "CEO and enjoyed his visits", "CEO and showed her a draft", "CEO and recommended her a hair gel",
            "CEO and produced a report for her", "CEO and ignored her", "CEO and listened to her conversations",
            "CEO and enjoyed her visits", "CEO to find the book because she asked to",
            "CEO and gave her some health suggestions", "CEO and asked her for a promotion",
            "CEO and asked her to sign", "CEO and asked her to leave", "CEO and asked her the question again",
            "CEO and then gave her goods", "CEO and proceeded to her home", "CEO and recommended him a hair gel"]


def get_female_list_long():
    return ["she", "hers", "her", "woman", "women", "mother", "female", "vulva"]


def get_male_list_long():
    return ["he", "his", "him", "man", "men", "father", "male", "penis"]


def get_female_list_short():
    return ["she"]


def get_male_list_short():
    return ["he"]


def get_bolukbasi_female_list():
    return ['her', 'she', 'women', 'woman', 'wife', 'mother', 'daughter', 'girls', 'girl', 'spokeswoman', 'female',
            'sister', 'herself', 'actress', 'mom', 'girlfriend', 'daughters', 'lady', 'sisters', 'mothers',
            'grandmother', 'ladies', 'queen', 'ma', 'wives', 'widow', 'bride', 'females', 'aunt', 'lesbian',
            'chairwoman', 'moms', 'maiden', 'granddaughter', 'niece', 'hers', 'filly', 'princess', 'lesbians',
            'actresses', 'maid', 'mare', 'fiancee', 'dads', 'waitress', 'maternal', 'heroine', 'nieces', 'girlfriends',
            'mistress', 'womb', 'grandma', 'maternity', 'estrogen', 'widows', 'diva', 'nuns', 'nun', 'brides',
            'housewife', 'menopause', 'motherhood', 'stepmother', 'hostess', 'fillies', 'congresswoman', 'witch',
            'sorority', 'businesswoman', 'gal', 'schoolgirl', 'goddess', 'stepdaughter', 'uterus', 'mama', 'hens',
            'hen', 'mommy', 'grandmothers', 'feminism', 'heiress', 'queens', 'witches', 'aunts', 'granddaughters',
            'convent', 'vagina', 'maids', 'gals', 'housewives', 'obstetrics', 'councilwoman', 'matriarch', 'dowry',
            'deer']


def get_bolukbasi_male_list():
    return ['he', 'his', 'him', 'man', 'men', 'spokesman', 'himself', 'son', 'father', 'guy', 'boy', 'boys', 'brother',
            'male', 'brothers', 'dad', 'sons', 'king', 'businessman', 'grandfather', 'uncle', 'congressman', 'grandson',
            'bull', 'businessmen', 'nephew', 'fathers', 'lads', 'lion', 'gentleman', 'fraternity', 'bachelor', 'bulls',
            'prince', 'colt', 'salesman', 'dude', 'beard', 'councilman', 'gentlemen', 'stepfather', 'monks', 'lad',
            'testosterone', 'nephews', 'daddy', 'kings', 'sir', 'stud', 'lions', 'gelding', 'czar', 'countrymen',
            'penis', 'bloke', 'spokesmen', 'monastery', 'brethren', 'schoolboy', 'brotherhood', 'stepson', 'uncles',
            'monk', 'viagra', 'macho', 'statesman', 'fathered', 'blokes', 'dudes', 'strongman', 'grandsons', 'studs',
            'godfather', 'boyhood', 'baritone', 'grandpa', 'countryman', 'stallion', 'fella', 'chap', 'widower',
            'salesmen', 'beau', 'beards', 'handyman', 'horsemen', 'fatherhood', 'princes', 'colts', 'fraternities',
            'pa', 'fellas', 'councilmen', 'barbershop', 'fraternal', 'husband', 'boyfriend', 'males', 'husbands',
            'sperm', 'fiance', 'suitors', 'prostate', 'paternity', 'suitor', 'hubby', 'boyfriends', 'semen']


'''gender_list = ["lads", "lion", "gentleman", "fraternity", "bachelor", "niece", "bulls", "husbands", "prince",
               "colt", "salesman", "hers", "dude", "beard", "filly", "princess", "lesbians", "councilman",
               "actresses", "gentlemen", "stepfather", "monks", "lad", "sperm", "testosterone", "nephews",
               "acknowledge", "acquaint", "acquiesce", "acquire", "acquit", "act", "activate", "actualize", "adapt",
               "add", "address", "adhere", "adjoin", "adjourn", "adjudicate", "adjust", "administer",
               "administrate", "admire", "admit", "admonish", "adopt", "adore", "adorn", "adsorb", "adulate",
               "advance", "advertise"]'''

'''bolukbasi_amiguous = ['deer', 'ma', 'husband', 'boyfriend', 'males', 'husbands', 'sperm', 'fiance', 'suitors',
                      'prostate', 'paternity', 'suitor', 'hubby', 'boyfriends', 'semen']
'''


def get_20_handpicked_adjectives() -> list:
    handpicked_adjectives = ["brunette", "sassy", "perky", "lovely", "vivacious", "married", "mature", "alluring",
                             "bubbly", "catty", "grizzled", "wiry", "shifty", "affable", "illustrious", "suave",
                             "eminent", "jovial", "decent", "rascally"]
    return handpicked_adjectives


def get_20_handpicked_verbs() -> list:
    handpicked_verbs = ["tease", "shower", "undress", "sew", "marry", "seduce", "bake", "milk", "wed", "flirt",
                        "allure", "lick", "gossip", "accessorize", "moan", "knit", "sample", "kiss", "treat", "crochet",
                        "bath", "tackle", "swagger", "reckon", "overthrow", "draft", "preach", "gallop", "apprehend",
                        "parley", "maul", "trade", "forge", "hoist", "dent", "exalt", "brawl", "decide", "resign",
                        "commit", "succeed", "retire"]
    return handpicked_verbs


def get_occupations(path) -> list:
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


def get_unique_sentences(path_sentences, occupations_list):
    sentences_set = set()
    with open(path_sentences, 'r', encoding="utf-8") as f:
        for line in f:
            values = line.split("\t")
            occupation = values[3].replace("the ", "").replace("The ", "").replace("a ", "").replace("an ", "").rstrip()
            sentence = values[2].replace(occupation, "X")
            for elem in occupations_list:
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


def get_plotting_word_list(words: list, word_emb) -> [list]:
    male_words = get_bolukbasi_male_list()
    female_words = get_bolukbasi_female_list()

    male_vectors = np.array([word_emb.get(male_word) for male_word in male_words])
    female_vectors = np.array([word_emb.get(female_word) for female_word in female_words])

    he_vector = np.array(word_emb.get("he"))
    she_vector = np.array(word_emb.get("she"))

    words_to_plot = []

    for word in words:
        x_val = get_bias_score_matrix([word], he_vector, she_vector, word_emb)
        print(x_val)
        y_val = get_bias_score_matrix([word], male_vectors, female_vectors, word_emb)
        words_to_plot.append([word, x_val[0][1], y_val[0][1]])
    print(words_to_plot)
    return words_to_plot
