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


def get_file_saver_instance(file_type: str = None) -> Path:
    root = tk.Tk()
    root.withdraw()

    if file_type == ".txt":
        # Load data (deserialize)
        file_saver = filedialog.asksaveasfile("w", parent=root, initialdir=INITIAL_DIR, defaultextension=".txt")
    else:
        file_saver = filedialog.asksaveasfile("w", parent=root, initialdir=INITIAL_DIR)

    return file_saver


def get_file_path_for_saving(file_extension: str = None) -> Path:
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
    # Load data
    try:
        with open(file_path, 'rb') as handle:
            unserialized_data = pickle.load(handle)
        return unserialized_data
    except OSError:
        print('cannot load: ', file_path)


def load_txt_to_dict() -> dict:
    file_path = get_file_path_for_loading("Choose a word embedding file in .txt format")
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
