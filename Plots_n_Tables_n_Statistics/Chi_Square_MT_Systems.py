import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc
import matplotlib.font_manager
from pathlib import Path
from dotenv import load_dotenv
import os
from tqdm import tqdm
from scipy.stats import chi2_contingency
import numpy as np
from time import sleep
import statsmodels


# load paths from env:
load_dotenv()
mt_systems_adj_path = os.environ["MT_SYSTEMS_ADJ"]
mt_systems_verbs_path = os.environ["MT_SYSTEMS_VERBS"]
mt_systems_occ_adj_path = os.environ["MT_SYSTEMS_OCC_ADJ"]
mt_systems_occ_verbs_path = os.environ["MT_SYSTEMS_OCC_VERBS"]

save_path = os.environ["PLOT_SAVE_PATH"]


def barplot_plotter_mt_system(title: str, word_class: str, values_deepL: list, values_microsoft: list,
                              values_google: list, save_name: str):
    # deepl female male [15092, 15386] - google female male [12003, 17905]
    # deepl female male [15092, 15386] - microsoft female male [12734, 17219]
    # google female male [12003, 17905] - microsoft female male [12734, 17219]

    # deepl female male [13525, 16803] - google female male [10174, 16661]
    # deepl female male [13525, 16803] - microsoft female male [9929, 15348]
    # google female male [10174, 16661] - microsoft female male [9929, 15348]

    # deepl female male [1259, 1758] - google female male [976, 1965]
    # deepl female male [1259, 1758] - microsoft female male [1041, 1868]
    # google female male [976, 1965] - microsoft female male [1041, 1868]

    word_types_complete = ["female","female","female",
                           "male","male","male",
                           "none","none","none"]
    mt_systems_complete = ["DeepL", "Microsoft", "Google",
                           "DeepL", "Microsoft", "Google",
                           "DeepL", "Microsoft", "Google"]
    female_ratio_complete_0 = [(15092 / (15092 + 15386)), (12734 / (12734 + 17219)), (12003 / (12003 + 17905)),
                             (13525 / (13525 + 16803)), (9929 / (9929 + 15348)), (10174 / (10174 + 16661)),
                             (1259 / (1259 + 1758)), (1041 / (1041 + 1868)), (976 / (976 + 1965))]
    female_ratio_complete = [i * 100 for i in female_ratio_complete_0]


    plt.clf()
    # SeabornplotCode
    # Latex plotting code from Malte Büttner
    sns.set_context("paper")
    sns.set_style("whitegrid")
    sns.set_palette("colorblind")

    rc('font', **{'family': 'serif', 'serif': ['Palatino']})
    rc('text', usetex=True)

    plt.rc('font', size=12)  # controls default text sizes
    plt.rc('axes', titlesize=12)  # fontsize of the axes title
    plt.rc('axes', labelsize=12)  # fontsize of the x and y labels
    plt.rc('xtick', labelsize=12)  # fontsize of the tick labels
    plt.rc('ytick', labelsize=12)  # fontsize of the tick labels
    plt.rc('legend', fontsize=12)  # legend fontsize
    plt.rc('figure', titlesize=12)

    barplot_df = pd.DataFrame(list(zip(word_types_complete, mt_systems_complete, female_ratio_complete)),
                                  columns=['Adjectives', 'MT System', "Female-Translated Ratio (\%)"])

    if len(values_deepL) == 2:
        palette_colours = ["C0", "C1"]
    else:
        palette_colours = ["C0", "C2", "C1"]

    barplot = sns.barplot(y="Female-Translated Ratio (\%)", x='Adjectives', hue='MT System', data=barplot_df,
                          saturation=1, alpha=0.9, palette=palette_colours)

    for p in barplot.patches:
        barplot.annotate(format(p.get_height(), '.1f'),
                         (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center',
                         size=12,
                         xytext=(0, 5),
                         textcoords='offset points')

    # plt.axvline(occupations_median, linestyle='--', color='g')
    # plt.axvline(adjectives_median, linestyle='--', color='b')
    # plt.axvline(verbs_median, linestyle='--', color='orange')

    barplot.set_ylim(0, 100)
    # ax.set(xlabel="Gender score", ylabel='Density')
    # ax._legend.set_title("Word-List:")
    # barplot.legend(loc="upper left", bbox_to_anchor=(0, 1.05))
    barplot.legend()
    sns.despine(bottom=True, left=True)
    barplot.figure.savefig(Path(save_path + save_name))


def get_confusion_matrix_adjectives(nested_list_input: list):
    female_word_female_trans = 0
    female_word_male_trans = 0
    male_word_female_trans = 0
    male_word_male_trans = 0
    neutral_word_female_trans = 0
    neutral_word_male_trans = 0

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

    print("female", female_word, "- male", male_word)
    obs = np.array([female_word, male_word])
    print(chi2_contingency(obs))

    print("female", female_word, "- neutral", neutral_word)
    obs = np.array([female_word, neutral_word])
    print(chi2_contingency(obs))

    print("male", male_word,  "- neutral", neutral_word)
    obs = np.array([male_word, neutral_word])
    print(chi2_contingency(obs))

    return [female_word, neutral_word, male_word]


def get_everything_adj_mt_systems(nested_list_input: list):
    deepl_female_word_female_trans, deepl_male_word_female_trans, deepl_neutral_word_female_trans = 0, 0, 0
    deepl_female_word_male_trans, deepl_male_word_male_trans, deepl_neutral_word_male_trans = 0, 0, 0

    google_female_word_female_trans, google_male_word_female_trans, google_neutral_word_female_trans = 0, 0, 0
    google_female_word_male_trans, google_male_word_male_trans, google_neutral_word_male_trans = 0, 0, 0

    microsoft_female_word_female_trans, microsoft_male_word_female_trans, microsoft_neutral_word_female_trans = 0, 0, 0
    microsoft_female_word_male_trans, microsoft_male_word_male_trans, microsoft_neutral_word_male_trans = 0, 0, 0

    for translation in nested_list_input:
        if translation[2] != "WORD":
            if translation[0] == "DeepL":
                if translation[1] == "female":
                    deepl_female_word_female_trans += (int(translation[5]) + int(translation[6]))
                    deepl_female_word_male_trans += (int(translation[7]) + int(translation[8]))
                elif translation[1] == "male":
                    deepl_male_word_female_trans += (int(translation[5]) + int(translation[6]))
                    deepl_male_word_male_trans += (int(translation[7]) + int(translation[8]))
                elif translation[1] == "neutral":
                    deepl_neutral_word_female_trans += (int(translation[5]) + int(translation[6]))
                    deepl_neutral_word_male_trans += (int(translation[7]) + int(translation[8]))
            elif translation[0] == "Google":
                if translation[1] == "female":
                    google_female_word_female_trans += (int(translation[5]) + int(translation[6]))
                    google_female_word_male_trans += (int(translation[7]) + int(translation[8]))
                elif translation[1] == "male":
                    google_male_word_female_trans += (int(translation[5]) + int(translation[6]))
                    google_male_word_male_trans += (int(translation[7]) + int(translation[8]))
                elif translation[1] == "neutral":
                    google_neutral_word_female_trans += (int(translation[5]) + int(translation[6]))
                    google_neutral_word_male_trans += (int(translation[7]) + int(translation[8]))
            elif translation[0] == "Microsoft":
                if translation[1] == "female":
                    microsoft_female_word_female_trans += (int(translation[5]) + int(translation[6]))
                    microsoft_female_word_male_trans += (int(translation[7]) + int(translation[8]))
                elif translation[1] == "male":
                    microsoft_male_word_female_trans += (int(translation[5]) + int(translation[6]))
                    microsoft_male_word_male_trans += (int(translation[7]) + int(translation[8]))
                elif translation[1] == "neutral":
                    microsoft_neutral_word_female_trans += (int(translation[5]) + int(translation[6]))
                    microsoft_neutral_word_male_trans += (int(translation[7]) + int(translation[8]))

    deepl_female = [deepl_female_word_female_trans, deepl_female_word_male_trans]
    deepl_male = [deepl_male_word_female_trans, deepl_male_word_male_trans]
    deepl_none = [deepl_neutral_word_female_trans, deepl_neutral_word_male_trans]

    google_female = [google_female_word_female_trans, google_female_word_male_trans]
    google_male = [google_male_word_female_trans, google_male_word_male_trans]
    google_none = [google_neutral_word_female_trans, google_neutral_word_male_trans]

    microsoft_female = [microsoft_female_word_female_trans, microsoft_female_word_male_trans]
    microsoft_male = [microsoft_male_word_female_trans, microsoft_male_word_male_trans]
    microsoft_none = [microsoft_neutral_word_female_trans, microsoft_neutral_word_male_trans]

    print(50*"\#")
    print("FEMALE COMPARISONS")
    print("deepl female male", deepl_female, "- google female male", google_female)
    obs = np.array([deepl_female, google_female])
    print(chi2_contingency(obs))

    print("deepl female male", deepl_female, "- microsoft female male", microsoft_female)
    obs = np.array([deepl_female, microsoft_female])
    print(chi2_contingency(obs))

    print("google female male", google_female, "- microsoft female male", microsoft_female)
    obs = np.array([google_female, microsoft_female])
    print(chi2_contingency(obs))


    print(50*"\#")
    print("MALE COMPARISONS")
    print("deepl female male", deepl_male, "- google female male", google_male)
    obs = np.array([deepl_male, google_male])
    print(chi2_contingency(obs))

    print("deepl female male", deepl_male, "- microsoft female male", microsoft_male)
    obs = np.array([deepl_male, microsoft_male])
    print(chi2_contingency(obs))

    print("google female male", google_male, "- microsoft female male", microsoft_male)
    obs = np.array([google_male, microsoft_male])
    print(chi2_contingency(obs))


    print(50*"\#")
    print("NEUTRAL COMPARISONS")
    print("deepl female male", deepl_none, "- google female male", google_none)
    obs = np.array([deepl_none, google_none])
    print(chi2_contingency(obs))

    print("deepl female male", deepl_none, "- microsoft female male", microsoft_none)
    obs = np.array([deepl_none, microsoft_none])
    print(chi2_contingency(obs))

    print("google female male", google_none, "- microsoft female male", microsoft_none)
    obs = np.array([google_none, microsoft_none])
    print(chi2_contingency(obs))

    barplot_plotter_mt_system("None COMPARISONS", "None adjectives",
                              [deepl_female, deepl_male, deepl_none],
                              [microsoft_female, microsoft_male, microsoft_none],
                              [google_female, google_male, google_none],
                              "MT_Systems_Adj.pdf")

    return


def get_confusion_matrix_verbs(nested_list_input: list):
    female_word_female_trans = 0
    female_word_male_trans = 0
    male_word_female_trans = 0
    male_word_male_trans = 0

    for translation in nested_list_input:
        if translation[1] != "WORD":
            if translation[0] == "female":
                female_word_female_trans += (int(translation[5]))
                female_word_male_trans += (int(translation[6]))
            elif translation[0] == "male":
                male_word_female_trans += (int(translation[5]))
                male_word_male_trans += (int(translation[6]))

    female_word = [female_word_female_trans, female_word_male_trans]
    male_word = [male_word_female_trans, male_word_male_trans]

    print("female", female_word, "- male", male_word)
    obs = np.array([female_word, male_word])
    print(chi2_contingency(obs))
    return [female_word, male_word]


def get_confusion_matrix_verbs_occupations(nested_list_input: list):
    female_word_female_trans = 0
    female_word_male_trans = 0
    male_word_female_trans = 0
    male_word_male_trans = 0
    neutral_word_female_trans = 0
    neutral_word_male_trans = 0

    for translation in nested_list_input:
        if translation[1] != "WORD":
            if translation[0] == "female":
                female_word_female_trans += (int(translation[5]))
                female_word_male_trans += (int(translation[6]))
            elif translation[0] == "male":
                male_word_female_trans += (int(translation[5]))
                male_word_male_trans += (int(translation[6]))
            elif translation[0] == "neutral":
                neutral_word_female_trans += (int(translation[5]))
                neutral_word_male_trans += (int(translation[6]))

    female_word = [female_word_female_trans, female_word_male_trans]
    male_word = [male_word_female_trans, male_word_male_trans]
    neutral_word = [neutral_word_female_trans, neutral_word_male_trans]

    print("female", female_word, "- male", male_word)
    obs = np.array([female_word, male_word])
    print(chi2_contingency(obs))

    print("female", female_word, "- neutral", neutral_word)
    obs = np.array([female_word, neutral_word])
    print(chi2_contingency(obs))

    if male_word[0] + neutral_word[0] > 0:
        print("male", male_word, "- neutral", neutral_word)
        obs = np.array([male_word, neutral_word])
        print(chi2_contingency(obs))

    return [female_word, neutral_word, male_word]


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
    sleep(1)
    print("You opened: " + Path(file_path).name)
    return nested_list


mt_systems_adj = load_nested_list_to_list(Path(mt_systems_adj_path))
print("DeepL-Adjectives-Results")
get_everything_adj_mt_systems(mt_systems_adj)
