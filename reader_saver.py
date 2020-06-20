import io

from tqdm import tqdm
import pickle
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import numpy as np
import re


INITIAL_DIR_WORDS = "/home/jonas/Nextcloud/#CitH/Masterarbeit/Words"
INITIAL_DIR_EMBEDDINGS = "/home/jonas/Schreibtisch/GitRepos/PretrainedWordVectors"
INITIAL_DIR = "/home/jonas/Schreibtisch/GitRepos"


def get_file_saver_instance(file_type: str = None):
    root = tk.Tk()
    root.withdraw()

    if file_type == ".txt":
        # Load data (deserialize)
        file_saver = filedialog.asksaveasfile("w", parent=root, initialdir=INITIAL_DIR, defaultextension=".txt")
    else:
        file_saver = filedialog.asksaveasfile("w", parent=root, initialdir=INITIAL_DIR)

    return file_saver


def get_file_path_for_saving(file_extension: str = None) -> str:
    root = tk.Tk()
    root.withdraw()

    if file_extension is not None:
        file_path = Path(filedialog.asksaveasfilename(parent=root, initialdir=INITIAL_DIR)).with_suffix(file_extension)
    else:
        file_path = Path(filedialog.asksaveasfilename(parent=root, initialdir=INITIAL_DIR))

    path = file_path.absolute().as_posix()
    return path


def get_file_path_for_loading(window_title) -> str:
    root = tk.Tk()
    root.withdraw()

    file_path = Path(filedialog.askopenfilename(parent=root, initialdir=INITIAL_DIR, title=window_title))
    path = file_path.absolute().as_posix()

    return path


def save_dict_to_pkl(dict_to_save) -> None:
    file_path = get_file_path_for_saving(".pickle")

    # Store data

    if file_path is None:
        print("Did not save:", file_path)
        return
    try:
        with open(file_path, 'wb') as handle:
            pickle.dump(dict_to_save, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print("Saved file to", file_path)
        return
    except OSError:
        print('cannot save: ', file_path)


def load_pkl_to_dict() -> dict:
    file_path = get_file_path_for_loading("Choose a word embedding file in .pickle format")
    print("You selected the file: ", str(file_path))
    # Load data
    try:
        with open(file_path, 'rb') as handle:
            unserialized_data = pickle.load(handle)
        return unserialized_data
    except OSError:
        print('cannot load: ', file_path)


def load_txt_to_dict() -> dict:
    print("Load GloVe .txt file to load")
    file_path = get_file_path_for_loading("Choose a word embedding file in .txt format")
    print("You selected the file: ", str(file_path))
    embeddings_dict = {}
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Creating dictionary: "):
            values = line.split(" ")
            word = values[0]
            vector = np.asarray(values[1:], "float32")
            embeddings_dict[word] = vector
    return embeddings_dict


def load_vocab_to_list_at_2nd_pos() -> list:
    file_path = get_file_path_for_loading("Choose a word list file in .txt format")

    vocab_list = []
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Creating vocab list: "):
            values = line.split(" ")
            word = values[1]
            vocab_list.append(word.rstrip())
    return vocab_list


def load_vocab_to_list_at_1st_pos() -> list:
    file_path = get_file_path_for_loading("Choose a word list file in .txt format")

    vocab_list = []
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Creating vocab list: "):
            if line:
                values = line.split("\t")
                word = values[0]
                vocab_list.append(word.rstrip())
    return vocab_list


def load_vocab_to_list() -> list:
    file_path = get_file_path_for_loading("Choose a word list file in .txt format")

    vocab_list = []
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Creating vocab list: "):
            vocab_list.append(line.rstrip())
    return vocab_list


def load_nested_vocab_to_list() -> list:
    file_path = get_file_path_for_loading("Choose a nested word list file in .txt format")

    vocab_list = []
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Creating vocab list: "):
            line = line.replace("[", "")
            line = line.replace("]", "")
            values = line.split(", ")
            for value in values:
                word = value.strip("'")
                vocab_list.append(word.rstrip())
    return vocab_list


def write_list_to_file(list_to_save):
    file_saver = get_file_saver_instance(".txt")
    if file_saver is None:
        print("Not Saved")
        return
    for item in list_to_save:
        file_saver.write(str(item))
        file_saver.write("\n")
    print("File saved")


def write_nested_list_to_file(list_to_save):
    file_saver = get_file_saver_instance(".txt")
    if file_saver is None:
        print("Not Saved")
        return
    for item in list_to_save:
        for i, value in enumerate(item):
            file_saver.write(str(value))
            if i+1 < len(item):
                file_saver.write("\t")
        file_saver.write("\n")
    print("File saved")


def write_nested_dict_to_file(dict_to_save: dict, sorted_keys: list):
    file_saver = get_file_saver_instance(".txt")
    if file_saver is None:
        print("Not Saved")
        return
    for key in sorted_keys:
        file_saver.write(str(key))
        for sub_key in dict_to_save[key]:
            file_saver.write("\t")
            file_saver.write(str(sub_key) + ": " + str(dict_to_save[key][sub_key]))
        file_saver.write("\n")
    file_saver.close()
    print("You saved the file")


def save_ranked_words_dict_to_file(word_score):
    for key in word_score:
        print(key, ":")
        for sub_key in word_score[key]:
            print(sub_key, "->", word_score[key][sub_key])
    reader_saver.write_nested_dict_to_file(word_score, sorted(word_score, key=lambda x: word_score[x]["sum_all"]))


def select_word_list():
    word_list = None
    # load the word list you want to rank
    print("Now choose the origin of the word list:")
    print("patternbasedwriting.com = 1")
    print("Oxford Dictionary = 2")
    print("Glove = 3")
    print("fastText = 4")
    while True:
        try:
            origin_int = int(input("Enter the corresponding number:"))
            if origin_int < 1 or origin_int > 4:
                raise ValueError
            elif origin_int == 1:
                origin = "patternbasedwriting.com"
                print("You chose \"patternbasedwriting.com\" as origin")
                print("Now choose the corresponding wordlist in .txt format")
                word_list = reader_saver.load_vocab_to_list_at_2nd_pos()
                break
            elif origin_int == 2:
                origin = "Oxford Dictionary"
                print("You chose \"Oxford Dictionary\" as origin")
                # print("Now choose the corresponding wordlist in .txt format")
                print("No Oxford list available yet")
                break
            elif origin_int == 3:
                origin = "Glove"
                print("You chose \"Glove\" as origin")
                print("Now choose the corresponding wordlist in .txt format")
                word_list = reader_saver.load_nested_vocab_to_list()
                break
            elif origin_int == 4:
                origin = "fastText"
                print("You chose \"fastText\" as origin")
                print("Now choose the corresponding wordlist in .txt format")
                word_list = reader_saver.load_nested_vocab_to_list()
                break

        except ValueError:
            print("Please enter an int between 1 - 4")
    return origin, word_list