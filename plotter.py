import matplotlib.pyplot as plt
from adjustText import adjust_text
import seaborn as sns
import pandas as pd


# adjust_text solution with matplotlib
def create_word_map(word_list: list) -> None:
    plt.style.use("seaborn")
    plt.figure(figsize=(12,8))
    plt.ylabel("Blokubasi List Value")
    plt.xlim((-0.25, 0.25))
    plt.xlabel("He - She Value")
    plt.ylim((-0.15, 0.15))
    texts = []
    for elem in word_list:
        word = elem[0]
        x = elem[1]
        y = elem[2]
        plt.plot(x, y, color='royalblue', marker='o')
        texts.append(plt.text(x, y, word, fontsize='large'))
    adjust_text(texts, only_move={'text': 'xy'}, force_text=1, arrowprops=dict(arrowstyle="->", color='lightcoral',alpha=.5, lw=1))
    #adjust_text(texts, autoalign='xy', only_move={'text': 'xy'}, arrowprops=dict(arrowstyle='->', color='red'))
    plt.show()
    return None


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
