import matplotlib.pyplot as plt
from adjustText import adjust_text
import seaborn as sns
from matplotlib import rc
import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv
import numpy as np

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

# plt.xlim(-1, 1)


# load paths from env:
load_dotenv()
load_path_base = os.environ["DATA_LOAD_PATH_BASE"]
occ_concat = os.environ["LOAD_OCC_CONCAT"]
save_path = os.environ["PLOT_SAVE_PATH"]



###########################
# Occupation CSV to Table #
###########################

occupations_path_with_percentage: str = load_path_base + occ_concat + "ONLY_Occupations_ranked_with_ALL_PLUS_GENDER_PERCENT.csv"

occupations = pd.read_csv(Path(occupations_path_with_percentage), sep=None, engine="python")
print(occupations)

occupations_percentage = occupations[["Word", "WB 2017", "WB 2019", "2019"]]
occupations_percentage.loc[:, "All_Percentages"] = occupations_percentage.sum(axis=1, skipna=True)
occupations_percentage = pd.concat([occupations_percentage, occupations[["sum_all"]]], axis=1)
occupations_percentage = occupations_percentage.replace(0.0, np.nan)
occupations_percentage = occupations_percentage.dropna(subset=["All_Percentages", "sum_all"])
print(occupations_percentage)
'''
plot = sns.regplot(data=occupations_percentage, x="sum_all", y="All_Percentages", fit_reg=False, marker="+", color="skyblue")

for line in range(0, occupations_percentage.shape[0]):
    plot.text(occupations_percentage.sum_all[line], occupations_percentage.All_Percentages[line] + 0.003, occupations_percentage.Word[line], horizontalalignment='center', size='small',
              color='black')

for i, point in occupations_percentage.iterrows():
    plot.text(point["sum_all"]+.02, point["All_Percentages"], str(point["Word"]), horizontalalignment='center', size='small',)

plt.show()
'''
scatterplot = sns.regplot(data=occupations_percentage, x="sum_all", y="All_Percentages", fit_reg=True, order=1, ci=95, marker="o")
# scatterplot = sns.lmplot(data=occupations_percentage, x="sum_all", y="All_Percentages")

#plt.style.use("seaborn")
#plt.figure(figsize=(12, 8))
#plt.ylabel("Percent of Females")
#plt.xlim((-1, 1))
#plt.xlabel("Gender Score")
#plt.ylim((0, 100))
#scatterplot.set_xlim(-1, 1)
scatterplot.set_ylim(0, 100)
#scatterplot = sns.regplot(data=occupations_percentage, x="sum_all", y="All_Percentages", fit_reg=True, order=1, ci=95, marker="o")

scatterplot.set(xlabel="Gender score", ylabel="Percentage of Women")
texts = []
for i, point in occupations_percentage.iterrows():
    word = str(point["Word"])
    x = point["sum_all"]
    y = point["All_Percentages"]
    # plt.plot(x, y, color='royalblue', marker='o')
    texts.append(plt.text(x, y, word, fontsize='x-small'))
adjust_text(texts, only_move={'text': 'xy'}, force_text=1, arrowprops=dict(arrowstyle="->", color='lightcoral', alpha=.5, lw=1))
# adjust_text(texts, autoalign='xy', only_move={'text': 'xy'}, arrowprops=dict(arrowstyle='->', color='red'))
sns.despine(bottom=True, left=True)
scatterplot.figure.savefig(Path(save_path + "OccGenderscorePercentage.pdf"))
plt.show()


# seaborn attempt
def create_word_map_seaborn(word_list: list) -> None:
    sns.set()
    df = pd.DataFrame(columns=["word", "he_she", "boluk"])
    for elem in word_list:
        df = df.append({"word": elem[0], "he_she": elem[1], "boluk": elem[2]}, ignore_index=True)
    plot = sns.regplot(data=df, x="he_she", y="boluk", fit_reg=False, marker="+", color="skyblue")
    plot.set(xlim=(-0.25, 0.25), ylim=(-0.15, 0.15))
    for line in range(0, df.shape[0]):
        plot.text(df.he_she[line], df.boluk[line] + 0.003, df.word[line], horizontalalignment='center', size='small', color='black')
    plt.show()
    return None