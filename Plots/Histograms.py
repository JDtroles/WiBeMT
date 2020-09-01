import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rc
from pathlib import Path
from dotenv import load_dotenv
import os

# load paths from env:
load_dotenv()
load_path_base = os.environ["DATA_LOAD_PATH_BASE"]
occ_concat = os.environ["LOAD_OCC_CONCAT"]
adj_concat = os.environ["LOAD_ADJ_CONCAT"]
ver_concat = os.environ["LOAD_VER_CONCAT"]

save_path = "PLOT_SAVE_PATH"

# Latex plotting code from Malte Büttner
sns.set_context("paper")
sns.set_style("whitegrid")
sns.set_palette("colorblind")

rc('font', **{'family': 'serif', 'serif': ['Palatino'], 'size': 11})
rc('text', usetex=True)

# path extension for histograms of word lists
occupations_path: str = load_path_base + occ_concat + "ONLY_Occupations_ranked_with_ALL.txt"
adjectives_path: str = load_path_base + adj_concat + "adj_pbw_garg_ALL.txt"
verbs_path: str = load_path_base + ver_concat + "verbs_ranked_ALL.txt"

occupations = pd.read_csv(Path(occupations_path), sep=None, engine="python")
print(occupations["sum_all"])

ax = sns.distplot(occupations["sum_all"], hist=True, kde=True, bins=10)
sns.despine(bottom = True, left = True)
plt.show()

