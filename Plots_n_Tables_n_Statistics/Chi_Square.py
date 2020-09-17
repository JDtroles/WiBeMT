import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc
import matplotlib.font_manager
from pathlib import Path
from dotenv import load_dotenv
import os
from tqdm import tqdm
from scipy.stats import chisquare
import numpy as np


from statistics import mean


# load paths from env:
load_dotenv()
deepL_adj_path = os.environ["DEEPL_ADJ"]
deepL_verb_path = os.environ["DEEPL_VERB"]
google_adj_path = os.environ["GOOGLE_ADJ"]
google_verb_path = os.environ["GOOGLE_VERB"]
microsoft_adj_path = os.environ["MICROSOFT_ADJ"]
microsoft_verb_path = os.environ["MICROSOFT_VERB"]
save_path = os.environ["PLOT_SAVE_PATH"]

# TODO: add str_list and loop to generate all tests / plots at once


def get_confusion_matrix(nested_list_input: list) -> tuple:
    female_word_female_trans = 0
    female_word_male_trans = 0
    male_word_female_trans = 0
    male_word_male_trans = 0
    neutral_word_female_trans = 0
    neutral_word_male_trans = 0

    # TODO: add option to change between adj / verb
    # positions of adj
    for translation in nested_list_input:
        if translation[1] != "WORD":
            if translation[0] == "female":
                female_word_female_trans += (int(translation[4]) + int(translation[5]))
                female_word_male_trans += (int(translation[6]) + int(translation[7]))
            elif translation[0] == "male":
                male_word_female_trans += (int(translation[4]) + int(translation[5]))
                male_word_male_trans += (int(translation[6]) + int(translation[7]))
            elif translation[0] == "neutral":
                neutral_word_female_trans += (int(translation[4]) + int(translation[5]))
                neutral_word_male_trans += (int(translation[6]) + int(translation[7]))

    female_word = [female_word_female_trans, female_word_male_trans]
    male_word = [male_word_female_trans, male_word_male_trans]
    neutral_word = [neutral_word_female_trans, neutral_word_male_trans]

    print("Test Chi")
    print(chisquare([60, 40], [40, 60]))

    print("female - male")
    print(chisquare(female_word, male_word))

    print("female - neutral")
    print(chisquare(female_word, neutral_word))

    print("male - neutral")
    print(chisquare(male_word, neutral_word))

    return

def load_nested_list_to_list(file_path) -> list:
    """
    loads a list of words from a file where each line contains a list of words
    element-separator: tab;



    :rtype list
    :return: list of words
    """
    nested_list = []
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Creating vocab list: "):
            if not line.strip():
                continue
            values: list = line.split("\t")
            nested_list.append([value.strip() for value in values])
    print("You opened: " + Path(file_path).name)
    return nested_list


deepL_adj = load_nested_list_to_list(Path(deepL_adj_path))

print(get_confusion_matrix(deepL_adj))
