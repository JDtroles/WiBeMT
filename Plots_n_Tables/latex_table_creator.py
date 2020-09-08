import pandas as pd
import os
from pathlib import Path
from dotenv import load_dotenv
import numpy as np

# load paths from env:
load_dotenv()
load_path_base = os.environ["DATA_LOAD_PATH_BASE"]
occ_concat = os.environ["LOAD_OCC_CONCAT"]


###########################
# Occupation CSV to Table #
###########################

occupations_path_with_percentage: str = load_path_base + occ_concat + "ONLY_Occupations_ranked_with_ALL_PLUS_GENDER_PERCENT.csv"

occupations = pd.read_csv(Path(occupations_path_with_percentage), sep=None, engine="python")

occupations_percentage = occupations[["Word", "WB 2017", "WB 2019", "2019"]]
occupations_percentage.loc[:, "All Percentages"] = occupations_percentage.sum(axis=1, skipna=True)
occupations_percentage = occupations_percentage.replace(0, np.nan)
print(occupations_percentage)
occupations_percentage = occupations_percentage.sort_values(by=["All Percentages", "Word"], axis="index", ascending=True, na_position="last")
print(occupations_percentage)
new_occ_1 = occupations_percentage.iloc[0:25, [0, 4]]
new_occ_1 = new_occ_1.rename(columns={"Word": "Word1", "All Percentages": "AllPerc1"})
# print(new_occ_1)
new_occ_2 = occupations_percentage.iloc[25:50, [0, 4]]
new_occ_2 = new_occ_2.rename(columns={"Word": "Word2", "All Percentages": "AllPerc2"})
# print(new_occ_2)
new_occ_3 = occupations_percentage.iloc[50:75, [0, 4]]
new_occ_3 = new_occ_3.rename(columns={"Word": "Word3", "All Percentages": "AllPerc3"})
# print(new_occ_3)
new_occ_4 = occupations_percentage.iloc[75:, [0, 4]]
new_occ_4 = new_occ_4.rename(columns={"Word": "Word4", "All Percentages": "AllPerc4"})
# print(new_occ_4)

new_occ = [new_occ_1.reset_index(drop=True), new_occ_2.reset_index(drop=True), new_occ_3.reset_index(drop=True), new_occ_4.reset_index(drop=True)]
new_occ = pd.concat(new_occ, axis=1)
new_occ[["AllPerc1", "AllPerc2", "AllPerc3", "AllPerc4"]] = new_occ[["AllPerc1", "AllPerc2", "AllPerc3", "AllPerc4"]].apply(pd.to_numeric, downcast="signed")
print(new_occ.to_latex(index=False, na_rep=''))
