import matplotlib.pyplot as plt


def create_word_map(word_list: list) -> None:
    plt.ylabel("Blokubasi List Value")
    plt.xlim((-0.25, 0.25))
    plt.xlabel("He - She Value")
    plt.ylim((-0.15, 0.15))
    for elem in word_list:
        word = elem[0]
        x = elem[1]
        y = elem[2]
        plt.text(x, y, word)
    plt.show()
    return None

