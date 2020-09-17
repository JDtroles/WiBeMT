import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc
import matplotlib.font_manager
from pathlib import Path
from dotenv import load_dotenv
import os
import reader_saver
from statistics import mean

# load paths from env:
load_dotenv()
load_path_base = os.environ["DATA_LOAD_PATH_BASE"]
occ_concat = os.environ["LOAD_OCC_CONCAT"]
adj_concat = os.environ["LOAD_ADJ_CONCAT"]
ver_concat = os.environ["LOAD_VER_CONCAT"]

save_path = os.environ["PLOT_SAVE_PATH"]

# Latex plotting code from Malte Büttner
sns.set_context("paper")
sns.set_style("whitegrid")
sns.set_palette("colorblind")

rc('font', **{'family': 'serif', 'serif': ['Palatino']})
rc('text', usetex=True)

plt.rc('font', size=12)          # controls default text sizes
plt.rc('axes', titlesize=12)     # fontsize of the axes title
plt.rc('axes', labelsize=12)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=12)    # fontsize of the tick labels
plt.rc('ytick', labelsize=12)    # fontsize of the tick labels
plt.rc('legend', fontsize=12)    # legend fontsize
plt.rc('figure', titlesize=12)

# Data:
DeepL_Adj = reader_saver.load_nested_list_to_list()
adjectives_class = ["none", "none", "male", "male", "female", "female"]
female_or_male = ["female", "male", "female", "male", "female", "male"]
female_accuracy_adj_female = []
female_accuracy_adj_male = []
female_accuracy_adj_neutral = []
male_accuracy_adj_female = []
male_accuracy_adj_male = []
male_accuracy_adj_neutral = []

for elem in DeepL_Adj:
    if elem[1] != "WORD":
        if int(elem[10]) > 0:
            if elem[0] == "neutral":
                female_accuracy_adj_neutral.append((int(elem[4]) + int(elem[5])) / int(elem[10]))
            elif elem[0] == "female":
                female_accuracy_adj_female.append((int(elem[4]) + int(elem[5])) / int(elem[10]))
            elif elem[0] == "male":
                female_accuracy_adj_male.append((int(elem[4]) + int(elem[5])) / int(elem[10]))
        if int(elem[10]) > 0:
            if elem[0] == "neutral":
                male_accuracy_adj_neutral.append((int(elem[6]) + int(elem[7])) / int(elem[10]))
            elif elem[0] == "female":
                male_accuracy_adj_female.append((int(elem[6]) + int(elem[7])) / int(elem[10]))
            elif elem[0] == "male":
                male_accuracy_adj_male.append((int(elem[6]) + int(elem[7])) / int(elem[10]))

accuracy = [mean(female_accuracy_adj_neutral), mean(male_accuracy_adj_neutral),
            mean(female_accuracy_adj_male), mean(male_accuracy_adj_male),
            mean(female_accuracy_adj_female), mean(male_accuracy_adj_female)]

DeepL_Adj_df = pd.DataFrame(list(zip(adjectives_class, female_or_male, accuracy)),
               columns =['Adjectives', 'female or male', "Gender of Translations (\%)"])
# DeepL_Adj_df = DeepL_Adj_df.sort_values(["female or male", "Gender of Translations (\%)"], axis=0)
# print(occupations[["sum_all"]])

barplot = sns.barplot(y="Gender of Translations (\%)", x='Adjectives', hue='female or male', data=DeepL_Adj_df)
'''
for p in barplot.patches:
    barplot.annotate(format(p.get_height(), '.0f'),
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha = 'center', va = 'center',
                     size=15,
                     xytext = (0, 5),
                     textcoords = 'offset points')
'''
# plt.axvline(occupations_median, linestyle='--', color='g')
# plt.axvline(adjectives_median, linestyle='--', color='b')
# plt.axvline(verbs_median, linestyle='--', color='orange')

# barplot.set_ylim(0, 100)
# ax.set(xlabel="Gender score", ylabel='Density')
# ax._legend.set_title("Word-List:")
# barplot.legend(loc="upper left", bbox_to_anchor=(0, 1.05))
barplot.legend()
sns.despine(bottom=True, left=True)
barplot.figure.savefig(Path(save_path + "DeepLAdjAccuracy.pdf"))
plt.show()


