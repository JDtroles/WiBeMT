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
translator = ["Google (WinoMT)", "Google (WinoMT)", "Google", "Google", "Microsoft", "Microsoft", "DeepL", "DeepL"]
pro_anti = ["Pro-Stereotypical", "Anti-Stereotypical", "Pro-Stereotypical", "Anti-Stereotypical", "Pro-Stereotypical",
            "Anti-Stereotypical", "Pro-Stereotypical", "Anti-Stereotypical"]
correct = [69, 57, 82, 52, 79, 65, 94, 70]

pro_anti_correct_translations = pd.DataFrame(list(zip(translator, pro_anti, correct)),
                                             columns=["Translation System", "Pro/Anti", "Correct Gender (\%)"])

# print(occupations[["sum_all"]])

barplot = sns.barplot(x="Translation System", y="Correct Gender (\%)", hue="Pro/Anti", data=pro_anti_correct_translations)

for p in barplot.patches:
    barplot.annotate(format(p.get_height(), '.0f'),
                     (p.get_x() + p.get_width() / 2., p.get_height()),
                     ha = 'center', va = 'center',
                     size=15,
                     xytext = (0, 5),
                     textcoords = 'offset points')

# plt.axvline(occupations_median, linestyle='--', color='g')
# plt.axvline(adjectives_median, linestyle='--', color='b')
# plt.axvline(verbs_median, linestyle='--', color='orange')

barplot.set_ylim(0, 100)
# ax.set(xlabel="Gender score", ylabel='Density')
# ax._legend.set_title("Word-List:")
barplot.legend(loc="upper left", bbox_to_anchor=(0, 1.05))
sns.despine(bottom=True, left=True)
barplot.figure.savefig(Path(save_path + "ProAntiCorrectTranslations.pdf"))
plt.show()


