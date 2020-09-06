import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc
import matplotlib.font_manager
from pathlib import Path
from dotenv import load_dotenv
import os

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


# path extension for histograms of word lists
occupations_path: str = load_path_base + occ_concat + "ONLY_Occupations_ranked_with_ALL.txt"
adjectives_path: str = load_path_base + adj_concat + "adj_pbw_garg_ALL.txt"
verbs_path: str = load_path_base + ver_concat + "verbs_ranked_ALL.txt"

occupations = pd.read_csv(Path(occupations_path), sep=None, engine="python")
adjectives = pd.read_csv(Path(adjectives_path),  sep=None, engine="python")
verbs = pd.read_csv(Path(verbs_path),  sep=None, engine="python")
# print(occupations[["sum_all"]])

occupations_median = float(occupations[["sum_all"]].median())
adjectives_median = float(adjectives[["sum_all"]].median())
verbs_median = float(verbs[["sum_all"]].median())

occupations_std = float(occupations[["sum_all"]].std())
adjectives_std = float(adjectives[["sum_all"]].std())
verbs_std = float(verbs[["sum_all"]].std())

print("Occupations: std =", occupations_std, "; median =", occupations_median)
print("Adjectives: std =", adjectives_std, "; median =", adjectives_median)
print("Verbs: std =", verbs_std, "; median =", verbs_median)


ax = sns.distplot(adjectives[["sum_all"]], bins=100, hist=False, label="Adjectives",
                  kde_kws={"bw": .20, 'shade': True, 'cut': 0,  'gridsize': 1000})
ax = sns.distplot(verbs[["sum_all"]], bins=100, hist=False, label="Verbs",
                  kde_kws={"bw": .20, 'shade': True, 'cut': 0,  'gridsize': 1000})
ax = sns.distplot(occupations[["sum_all"]], bins=100, hist=False, label="Occupations",
                  kde_kws={"bw": .20, 'shade': True, 'cut': 0, 'gridsize': 1000})
# plt.axvline(occupations_median, linestyle='--', color='g')
# plt.axvline(adjectives_median, linestyle='--', color='b')
# plt.axvline(verbs_median, linestyle='--', color='orange')

ax.set_xlim(-1, 1)
ax.set(xlabel="Gender score", ylabel='Density')
# ax._legend.set_title("Word-List:")
ax.legend()
sns.despine(bottom=True, left=True)
ax.figure.savefig(Path(save_path + "DistPlotWords.pdf"))
plt.show()
