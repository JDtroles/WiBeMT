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
deepL_adj_path = os.environ["DEEPL_ADJ"]
deepL_adj_occ_path = os.environ["DEEPL_ADJ_OCCUPATION_WEMB"]
deepL_adj_occ_percent_path = os.environ["DEEPL_ADJ_OCCUPATION_WINOB"]
deepL_verb_path = os.environ["DEEPL_VERB"]
deepL_verb_occupations_path = os.environ["DEEPL_VERB_OCCUPATION"]
google_adj_path = os.environ["GOOGLE_ADJ"]
google_adj_occ_path = os.environ["GOOGLE_ADJ_OCCUPATION_WEMB"]
google_adj_occ_percent_path = os.environ["GOOGLE_ADJ_OCCUPATION_WINOB"]
google_verb_path = os.environ["GOOGLE_VERB"]
google_verb_occupations_path = os.environ["GOOGLE_VERB_OCCUPATION"]
microsoft_adj_path = os.environ["MICROSOFT_ADJ"]
microsoft_adj_occ_path = os.environ["MICROSOFT_ADJ_OCCUPATION_WEMB"]
microsoft_adj_occ_percent_path = os.environ["MICROSOFT_ADJ_OCCUPATION_WINOB"]
microsoft_verb_path = os.environ["MICROSOFT_VERB"]
microsoft_verb_occupations_path = os.environ["MICROSOFT_VERB_OCCUPATION"]
save_path = os.environ["PLOT_SAVE_PATH"]


def barplot_plotter(title: str, word_class: str, values_deepL: list, values_microsoft: list, values_google: list,
                     save_name: str):

    mt_systems_deepL, categories_deepL, female_ratios_deepL = [], [], []
    mt_systems_microsoft, categories_microsoft, female_ratios_microsoft = [], [], []
    mt_systems_google, categories_google, female_ratios_google = [], [], []
    loop_count = 0
    for deepL, microsoft, google in zip(values_deepL, values_microsoft, values_google):
        mt_systems_deepL.append("DeepL")
        mt_systems_microsoft.append("Microsoft")
        mt_systems_google.append("Google")
        if loop_count == 0:
            categories_deepL.append("feminine-" + word_class)
            categories_microsoft.append("feminine-" + word_class)
            categories_google.append("feminine-" + word_class)
            female_ratios_deepL.append(100 * deepL[0] / (sum(deepL)))
            female_ratios_microsoft.append(100 * microsoft[0] / (sum(microsoft)))
            female_ratios_google.append(100 * google[0] / (sum(google)))
        elif len(values_deepL) == 3 and loop_count == 1:
            if word_class == "adjectives":
                categories_deepL.append("no-" + word_class)
                categories_microsoft.append("no-" + word_class)
                categories_google.append("no-" + word_class)
            else:
                categories_deepL.append("neutral-" + word_class)
                categories_microsoft.append("neutral-" + word_class)
                categories_google.append("neutral-" + word_class)
            female_ratios_deepL.append(100 * deepL[0] / (sum(deepL)))
            female_ratios_microsoft.append(100 * microsoft[0] / (sum(microsoft)))
            female_ratios_google.append(100 * google[0] / (sum(google)))
        elif len(values_deepL) == 2 and loop_count == 1:
            categories_deepL.append("masculine-" + word_class)
            categories_microsoft.append("masculine-" + word_class)
            categories_google.append("masculine-" + word_class)
            female_ratios_deepL.append(100 * deepL[0] / (sum(deepL)))
            female_ratios_microsoft.append(100 * microsoft[0] / (sum(microsoft)))
            female_ratios_google.append(100 * google[0] / (sum(google)))
        elif loop_count == 2:
            categories_deepL.append("masculine-" + word_class)
            categories_microsoft.append("masculine-" + word_class)
            categories_google.append("masculine-" + word_class)
            female_ratios_deepL.append(100 * deepL[0] / (sum(deepL)))
            female_ratios_microsoft.append(100 * microsoft[0] / (sum(microsoft)))
            female_ratios_google.append(100 * google[0] / (sum(google)))
        loop_count += 1

    mt_systems_complete = mt_systems_deepL + mt_systems_microsoft + mt_systems_google
    categories_complete = categories_deepL + categories_microsoft + categories_google
    female_ratios_complete = female_ratios_deepL + female_ratios_microsoft + female_ratios_google

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

    barplot_df = pd.DataFrame(list(zip(mt_systems_complete, categories_complete, female_ratios_complete)),
                                  columns=['MT systems', 'Word Category', "\%TFG"])

    if len(values_deepL) == 2:
        palette_colours = ["C0", "C1"]
    else:
        palette_colours = ["C0", "C2", "C1"]

    barplot = sns.barplot(y="\%TFG", x='MT systems', hue='Word Category', data=barplot_df,
                          saturation=1, alpha=1, palette=palette_colours)

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


def barplot_plotter_mt_system(title: str, word_class: str, values_deepL: list, values_microsoft: list,
                              values_google: list, save_name: str):

    mt_systems_deepL, categories_deepL, female_ratios_deepL = [], [], []
    mt_systems_microsoft, categories_microsoft, female_ratios_microsoft = [], [], []
    mt_systems_google, categories_google, female_ratios_google = [], [], []
    loop_count = 0
    for deepL, microsoft, google in zip(values_deepL, values_microsoft, values_google):
        mt_systems_deepL.append("DeepL")
        mt_systems_microsoft.append("Microsoft")
        mt_systems_google.append("Google")
        if loop_count == 0:
            categories_deepL.append("female-" + word_class)
            categories_microsoft.append("female-" + word_class)
            categories_google.append("female-" + word_class)
            female_ratios_deepL.append(100 * deepL[0] / (sum(deepL)))
            female_ratios_microsoft.append(100 * microsoft[0] / (sum(microsoft)))
            female_ratios_google.append(100 * google[0] / (sum(google)))
        elif len(values_deepL) == 3 and loop_count == 1:
            categories_deepL.append("neutral-" + word_class)
            categories_microsoft.append("neutral-" + word_class)
            categories_google.append("neutral-" + word_class)
            female_ratios_deepL.append(100 * deepL[0] / (sum(deepL)))
            female_ratios_microsoft.append(100 * microsoft[0] / (sum(microsoft)))
            female_ratios_google.append(100 * google[0] / (sum(google)))
        elif len(values_deepL) == 2 and loop_count == 1:
            categories_deepL.append("male-" + word_class)
            categories_microsoft.append("male-" + word_class)
            categories_google.append("male-" + word_class)
            female_ratios_deepL.append(100 * deepL[0] / (sum(deepL)))
            female_ratios_microsoft.append(100 * microsoft[0] / (sum(microsoft)))
            female_ratios_google.append(100 * google[0] / (sum(google)))
        elif loop_count == 2:
            categories_deepL.append("male-" + word_class)
            categories_microsoft.append("male-" + word_class)
            categories_google.append("male-" + word_class)
            female_ratios_deepL.append(100 * deepL[0] / (sum(deepL)))
            female_ratios_microsoft.append(100 * microsoft[0] / (sum(microsoft)))
            female_ratios_google.append(100 * google[0] / (sum(google)))
        loop_count += 1

    mt_systems_complete = mt_systems_deepL + mt_systems_microsoft + mt_systems_google
    categories_complete = categories_deepL + categories_microsoft + categories_google
    female_ratios_complete = female_ratios_deepL + female_ratios_microsoft + female_ratios_google

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

    barplot_df = pd.DataFrame(list(zip(mt_systems_complete, categories_complete, female_ratios_complete)),
                                  columns=['MT Systems', 'Word Category', "Female-Translated Ratio (\%)"])

    if len(values_deepL) == 2:
        palette_colours = ["C0", "C1"]
    else:
        palette_colours = ["C0", "C2", "C1"]

    barplot = sns.barplot(y="Female-Translated Ratio (\%)", x='MT Systems', hue='Word Category', data=barplot_df,
                          saturation=1, alpha=1, palette=palette_colours)

    for p in barplot.patches:
        barplot.annotate(format(p.get_height(), '.0f'),
                         (p.get_x() + p.get_width() / 2., p.get_height()),
                         ha='center', va='center',
                         size=15,
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


def get_confusion_matrix_adjectives_percent(nested_list_input: list):
    female_word_female_trans = 0
    female_word_male_trans = 0
    male_word_female_trans = 0
    male_word_male_trans = 0

    for translation in nested_list_input:
        if translation[1] != "WORD":
            if translation[0] == "female":
                female_word_female_trans += (int(translation[4]) + int(translation[5]))
                female_word_male_trans += (int(translation[6]) + int(translation[7]))
            elif translation[0] == "male":
                male_word_female_trans += (int(translation[4]) + int(translation[5]))
                male_word_male_trans += (int(translation[6]) + int(translation[7]))

    female_word = [female_word_female_trans, female_word_male_trans]
    male_word = [male_word_female_trans, male_word_male_trans]

    print("female", female_word, "- male", male_word)
    obs = np.array([female_word, male_word])
    print(chi2_contingency(obs))
    return [female_word, male_word]


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


deepL_adj = load_nested_list_to_list(Path(deepL_adj_path))
print("DeepL-Adjectives-Results")
deepL_adj_values = get_confusion_matrix_adjectives(deepL_adj)

print(50 * "\\#")
google_adj = load_nested_list_to_list(Path(google_adj_path))
print("Google-Adjectives-Results")
google_adj_values = get_confusion_matrix_adjectives(google_adj)

print(50 * "\\#")
microsoft_adj = load_nested_list_to_list(Path(microsoft_adj_path))
print("Microsoft-Adjectives-Results")
microsoft_adj_values = get_confusion_matrix_adjectives(microsoft_adj)

barplot_plotter("None", "adjectives", deepL_adj_values, microsoft_adj_values, google_adj_values,
                "FemaleRatioAdjectives.pdf")

################################################################################################

print(50 * "\\#")
deepL_adj_occ = load_nested_list_to_list(Path(deepL_adj_occ_path))
print("DeepL-Adjectives-Occupations-Results")
deepL_adj_occ_values = get_confusion_matrix_adjectives(deepL_adj_occ)

print(50 * "\\#")
google_adj_occ = load_nested_list_to_list(Path(google_adj_occ_path))
print("Google-Adjectives-Occupations-Results")
google_adj_occ_values = get_confusion_matrix_adjectives(google_adj_occ)

print(50 * "\\#")
microsoft_adj_occ = load_nested_list_to_list(Path(microsoft_adj_occ_path))
print("Microsoft-Adjectives-Occupations-Results")
microsoft_adj_occ_values = get_confusion_matrix_adjectives(microsoft_adj_occ)

barplot_plotter("None", "occupations", deepL_adj_occ_values, microsoft_adj_occ_values, google_adj_occ_values,
                "FemaleRatioAdjectiveOccupations.pdf")


################################################################################################

print(50 * "\\#")
deepL_adj_occ_percent = load_nested_list_to_list(Path(deepL_adj_occ_percent_path))
print("DeepL-Adjectives-Occupations-Percent-Results")
deepL_adj_occ_percent_values = get_confusion_matrix_adjectives_percent(deepL_adj_occ_percent)

print(50 * "\\#")
google_adj_occ_percent = load_nested_list_to_list(Path(google_adj_occ_percent_path))
print("Google-Adjectives-Occupations-Percent-Results")
google_adj_occ_percent_values = get_confusion_matrix_adjectives_percent(google_adj_occ_percent)

print(50 * "\\#")
microsoft_adj_occ_percent = load_nested_list_to_list(Path(microsoft_adj_occ_percent_path))
print("Microsoft-Adjectives-Occupations-Percent-Results")
microsoft_adj_occ_percent_values = get_confusion_matrix_adjectives_percent(microsoft_adj_occ_percent)

barplot_plotter("None", "occupations", deepL_adj_occ_percent_values, microsoft_adj_occ_percent_values,
                google_adj_occ_percent_values, "FemaleRatioAdjectiveOccupationsPercent.pdf")


################################################################################################

print(50 * "\\#")
deepL_verb = load_nested_list_to_list(Path(deepL_verb_path))
print("DeepL-Verb-Results")
deepL_verb_values = get_confusion_matrix_verbs(deepL_verb)

print(50 * "\\#")
google_verb = load_nested_list_to_list(Path(google_verb_path))
print("Google-Verbs-Results")
google_verb_values = get_confusion_matrix_verbs(google_verb)

print(50 * "\\#")
microsoft_verb = load_nested_list_to_list(Path(microsoft_verb_path))
print("Microsoft-Verbs-Results")
microsoft_verb_values = get_confusion_matrix_verbs(microsoft_verb)

barplot_plotter("None", "verbs", deepL_verb_values, microsoft_verb_values,
                google_verb_values, "FemaleRatioVerbs.pdf")

################################################################################################

print(50 * "\\#")
deepL_verb_occupations = load_nested_list_to_list(Path(deepL_verb_occupations_path))
print("DeepL-Verb-Results-OCCUPATIONS")
deepL_verb_occupations_values = get_confusion_matrix_verbs_occupations(deepL_verb_occupations)

print(50 * "\\#")
google_verb_occupations = load_nested_list_to_list(Path(google_verb_occupations_path))
print("Google-Verbs-Results-OCCUPATIONS")
google_verb_occupations_values = get_confusion_matrix_verbs_occupations(google_verb_occupations)

print(50 * "\\#")
microsoft_verb_occupations = load_nested_list_to_list(Path(microsoft_verb_occupations_path))
print("Microsoft-Verbs-Results-OCCUPATIONS")
microsoft_verb_occupations_values = get_confusion_matrix_verbs_occupations(microsoft_verb_occupations)

barplot_plotter("None", "occupations", deepL_verb_occupations_values, microsoft_verb_occupations_values,
                google_verb_occupations_values, "FemaleRatioVerbsOccupations.pdf")
