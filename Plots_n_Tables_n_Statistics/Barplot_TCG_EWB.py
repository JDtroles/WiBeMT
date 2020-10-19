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

# Data:
translator = ["DeepL", "DeepL", "DeepL", "DeepL", "DeepL", "DeepL",
              "Microsoft", "Microsoft", "Microsoft", "Microsoft", "Microsoft", "Microsoft",
              "Google", "Google", "Google", "Google", "Google", "Google"]
pro_anti = ["A", "B", "C", "D", "E", "F",
            "A", "B", "C", "D", "E", "F",
            "A", "B", "C", "D", "E", "F"]
correct = [89.6, 88.8, 84.0, 93.3, 78.2, 93.7,
           76.9, 90.9, 72.5, 92.5, 64.6, 91.6,
           68.9, 87.9, 65.8, 89.3, 55.5, 88.9]

pro_anti_correct_translations = pd.DataFrame(list(zip(translator, pro_anti, correct)),
                                             columns=["MT system", "Pro/Anti", "\%TCG"])

# print(occupations[["sum_all"]])

barplot = sns.barplot(x="MT system", y="\%TCG", hue="Pro/Anti", data=pro_anti_correct_translations,
                      palette=["C0", "C9", "C3", "C1", "C4", "C6"])

for p in barplot.patches:
    barplot.annotate(format(p.get_height(), '.0f'),
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha = 'center', va = 'center',
                     size=12,
                     xytext = (0, 5),
                     textcoords = 'offset points')

# plt.axvline(occupations_median, linestyle='--', color='g')
# plt.axvline(adjectives_median, linestyle='--', color='b')
# plt.axvline(verbs_median, linestyle='--', color='orange')

barplot.set_ylim(0, 100)
# ax.set(xlabel="Gender score", ylabel='Density')
# ax._legend.set_title("Word-List:")
barplot.legend(loc="lower left")
L = barplot.legend(loc="lower left", facecolor='white', framealpha=1)
L.get_texts()[0].set_text("F adjective, F pronoun")
L.get_texts()[1].set_text("F adjective, M pronoun")
L.get_texts()[2].set_text("M adjective, F pronoun")
L.get_texts()[3].set_text("M adjective, M pronoun")
L.get_texts()[4].set_text("no adjective, F pronoun")
L.get_texts()[5].set_text("no adjective, M pronoun")
sns.despine(bottom=True, left=True)
barplot.figure.savefig(Path(save_path + "BarplotEWBTCG.pdf"))
plt.show()


