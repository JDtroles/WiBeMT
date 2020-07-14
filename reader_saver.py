import io

from tqdm import tqdm
import pickle
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
import numpy as np
import re

INITIAL_DIR_WORDS = "/home/Jonas/Nextcloud/#CitH/Masterarbeit"
INITIAL_DIR_EMBEDDINGS = "/home/Jonas/Desktop"
INITIAL_DIR = "/home/Jonas/Desktop"


def get_file_saver_instance(file_type: str = None):
    """
    opens a asksaveasfile dialog from tkinter

    :param file_type: str ".txt" if ".txt" shall be appended to filename
    :return: file-writer-instance
    """
    root = tk.Tk()
    root.withdraw()

    if file_type == ".txt":
        # Load data (deserialize)
        file_saver = filedialog.asksaveasfile("w", parent=root, initialdir=INITIAL_DIR, defaultextension=".txt")
    else:
        file_saver = filedialog.asksaveasfile("w", parent=root, initialdir=INITIAL_DIR)

    return file_saver


def get_file_path_for_saving(file_extension: str = None) -> str:
    """
    opens a asksaveasfilename dialog from tkinter

    :param file_extension: str of file-extension which shall be appended to filename
    :return: str of Path object
    """
    root = tk.Tk()
    root.withdraw()

    if file_extension is not None:
        file_path = Path(filedialog.asksaveasfilename(parent=root, initialdir=INITIAL_DIR)).with_suffix(file_extension)
    else:
        file_path = Path(filedialog.asksaveasfilename(parent=root, initialdir=INITIAL_DIR))

    path = file_path.absolute().as_posix()
    return path


def get_file_path_for_loading(window_title) -> str:
    """
    opens a askopenfilename dialog from tkinter

    :param window_title: specifies the title of the askopenfilename-window
    :return: str of Path object
    """
    root = tk.Tk()
    root.withdraw()

    file_path = Path(filedialog.askopenfilename(parent=root, initialdir=INITIAL_DIR, title=window_title))
    path = file_path.absolute().as_posix()

    return path


def save_dict_to_pkl(dict_to_save) -> None:
    """
    saves a dict to a .pkl file

    :param dict_to_save: the dict one wants to save as a .pkl file
    :return: None
    """
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


def load_pkl_to_dict(file_path: str = None) -> dict:
    """
    loads a word_embedding in .pkl format which one selects at runtime

    :rtype dict
    :return: word_embedding: key = word, value = vector
    """
    if file_path is None:
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
    """
    loads a .txt or .vec word_embedding and writes it into a dict structure

    :return: word_embedding: key = word, value = vector
    """
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


def load_vocab_to_list_at_2nd_pos(separator: str = " ") -> list:
    """
    loads a list of words from a file;
    default line-separator: " ";
    2nd position in line is selected as list element

    :return: list of words
    """
    file_path = get_file_path_for_loading("Choose a word list file in .txt format")

    vocab_list = []
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Creating vocab list: "):
            values = line.split(separator)
            word = values[1]
            vocab_list.append(word.rstrip())
    return vocab_list


def load_verb_sentence_to_list_at_2nd_pos(separator: str = "\t") -> list:
    """
    loads a list of sentences from a file;
    default line-separator: "\t";
    2nd position in line is selected as list element

    :return: nested list of [[sentence_1, verb_1]...[sentence_n, verb_n]]
    """
    file_path = get_file_path_for_loading("Choose a word list file in .txt format")

    verb_sentences = []
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Creating vocab list: "):
            if len(line.strip()) > 0:
                line = line.strip()
                for elem in line:
                    values = line.split(separator)
                    sentence = values[1]
                    verb = values[2]
                    gender = values[3]
                    number = values[0]
                    verb_sentences.append([sentence, verb, gender, number])
    return verb_sentences


def load_vocab_to_list_at_1st_pos() -> list:
    r"""raw
    loads a list of words from a file

    line-separator: "\\\t"

    1st position in line is selected as list element

    :return: list of words
    """
    file_path = get_file_path_for_loading("Choose a word list file in .txt format")

    vocab_list = []
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Creating vocab list: "):
            if len(line.strip()) > 0:
                values = line.split("\t")
                word = values[0]
                vocab_list.append(word.rstrip())
    return vocab_list


def load_vocab_to_list() -> list:
    """
    loads a list of words from a file where each line only contains the word

    :rtype list
    :return: list of words
    """
    file_path = get_file_path_for_loading("Choose a word list file in .txt format")

    vocab_list = []
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Creating vocab list: "):
            vocab_list.append(line.rstrip())
    return vocab_list


def load_nested_vocab_to_list() -> list:
    """
    loads a list of words from a file where each line contains a list of words
    line-separator: ", ";


    :rtype list
    :return: list of words
    """
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
    """
    writes a list to a file specified at runtime

    :param list_to_save:
    :return: None
    """
    file_saver = get_file_saver_instance(".txt")
    if file_saver is None:
        print("Not Saved")
        return
    for item in list_to_save:
        file_saver.write(str(item))
        file_saver.write("\n")
    print("File saved")


def write_nested_list_to_file(list_to_save):
    """
    writes a nested list to a file specified at runtime
    each line contains the values of the sublist separated by "\t"

    :param list_to_save:
    :return: None
    """
    file_saver = get_file_saver_instance(".txt")
    if file_saver is None:
        print("Not Saved")
        return
    for item in list_to_save:
        file_saver.write(item[0])
        for value in item[1:]:
            file_saver.write("\t")
            file_saver.write(str(value))
        file_saver.write("\n")
    print("File saved")


def write_nested_dict_to_file(dict_to_save: dict, sorted_keys: list = None, write_subkeys: bool = True):
    """
    takes a nested dict and saves it to a file (specified at runtime)

    :param write_subkeys: defines if the subkeys are written or only the corresponding value
    :param dict_to_save: the nested dict one wants to be written to file
    :param sorted_keys: the sorted list of keys to define the list-order
    :return: None
    """
    file_saver = get_file_saver_instance(".txt")
    if file_saver is None:
        print("Not Saved")
        return
    # writes one line, with column headings and then only the valuey
    if sorted_keys is not None:
        # write column names
        file_saver.write("Word")
        if sorted_keys:
            for sub_key in dict_to_save[sorted_keys[0]]:
                file_saver.write("\t")
                file_saver.write(sub_key)
            file_saver.write("\n")
        for key in sorted_keys:
            file_saver.write(str(key))
            for sub_key in dict_to_save[key]:
                file_saver.write("\t")
                if write_subkeys:
                    file_saver.write(str(sub_key) + ": " + str(dict_to_save[key][sub_key]))
                else:
                    file_saver.write(str(dict_to_save[key][sub_key]))
            file_saver.write("\n")
    else:
        for key in sorted(dict_to_save):
            file_saver.write(str(key))
            for sub_key in dict_to_save[key]:
                file_saver.write("\t")
                if write_subkeys:
                    file_saver.write(str(sub_key) + ": " + str(dict_to_save[key][sub_key]))
                else:
                    file_saver.write(str(dict_to_save[key][sub_key]))
            file_saver.write("\n")
    file_saver.close()
    print("You saved the file")


def save_ranked_words_dict_to_file(word_score):
    """
    writes the given dict to a file;
    sorted by: "sum_all"

    :param word_score: dict of ranked words
    """
    write_nested_dict_to_file(word_score, sorted(word_score, key=lambda x: word_score[x]["sum_all"]),
                              write_subkeys=False)


def select_word_list() -> [str, list]:
    """
    user selects a word-list file and its origin

    :return: origin as str; list of words
    """
    word_list = None
    # load the word list you want to rank
    print("Now choose the origin of the word list:")
    print("patternbasedwriting.com = 1")
    print("pbw & Garg = 2")
    print("Garg = 3")
    print("WinoGender + WinoBias + Garg = 4")
    while True:
        try:
            origin_int = int(input("Enter the corresponding number:"))
            if origin_int < 1 or origin_int > 4:
                raise ValueError
            elif origin_int == 1:
                origin = "pbw"
                print("You chose \"", origin, "\" as origin")
                print("Now choose the corresponding wordlist in .txt format")
                word_list = load_vocab_to_list_at_2nd_pos()
                break
            elif origin_int == 2:
                origin = "pbw_Garg"
                print("You chose \"", origin, "\" as origin")
                print("Now choose the corresponding wordlist in .txt format")
                word_list = load_vocab_to_list_at_1st_pos()
                break
            elif origin_int == 3:
                origin = "Garg"
                print("You chose \"", origin, "\" as origin")
                print("Now choose the corresponding wordlist in .txt format")
                word_list = load_vocab_to_list_at_1st_pos()
                break
            elif origin_int == 4:
                origin = "WiGe_WiBi_Garg"
                print("You chose \"", origin, "\" as origin")
                print("Now choose the corresponding wordlist in .txt format")
                word_list = load_vocab_to_list_at_1st_pos()
                break

        except ValueError:
            print("Please enter an int between 1 - 4")
    return origin, word_list


def load_dictcc_to_list_at_1st_pos(word_type: str = "verb") -> list:
    r"""raw
    loads a list of words from a file

    line-separator: "\\\t"

    1st position in line is selected as list element

    :return: list of words
    """
    file_path = get_file_path_for_loading("Choose a word list file in .txt format")

    vocab_list = []
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Creating vocab list: "):
            if len(line.strip()) > 0:
                values = line.split("\t")
                # only consider lines with at least 3 elements
                if len(values) >= 3:
                    # only consider lines with correct wordtype in 3rd position
                    if values[2] == word_type:
                        # only consider single verbs ("to verb")
                        if len(values[0].split(" ")) == 2:
                            to_word = values[0].strip("'")
                            word = to_word.split(" ")[1]
                            vocab_list.append(word.rstrip())
    return vocab_list


def load_nested_list_to_list() -> list:
    """
    loads a list of words from a file where each line contains a list of words
    element-separator: tab;


    :rtype list
    :return: list of words
    """
    file_path = get_file_path_for_loading("Choose a nested word list file in .txt format")
    occupations = []
    with open(file_path, 'r', encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Creating vocab list: "):
            if not line.strip():
                continue
            values: list = line.split("\t")
            occupations.append([value.strip() for value in values])
    print("You opened: " + Path(file_path).name)
    return occupations


def load_nested_list_to_dict() -> dict:
    file_path = get_file_path_for_loading("Choose a nested word list file in .txt format")

    occupation_translations: dict = {}

    with open(file_path, 'r', encoding="utf-8") as f:
        for line in tqdm(f.readlines(), desc="Creating vocab list: "):
            if not line.strip():
                continue
            values: list = line.split("\t")
            key = str(values[0])
            fem_translations: list = values[1].split(", ")
            fem_trans_strip = []
            for elem in fem_translations:
                elem = elem.strip(" ")
                elem = elem.strip("\n")
                fem_trans_strip.append(elem.strip(" "))

            male_translations: list = values[2].split(", ")
            male_trans_strip = []
            for elem in male_translations:
                elem = elem.strip(" ")
                elem = elem.strip("\n")
                male_trans_strip.append(elem.strip(" "))

            neutral_translations: list = values[3].split(", ")
            neutral_trans_strip = []
            for elem in neutral_translations:
                elem = elem.strip(" ")
                elem = elem.strip("\n")
                neutral_trans_strip.append(elem.strip(" "))

            wrong_translations: list = values[4].split(", ")
            wrong_trans_strip = []
            for elem in wrong_translations:
                elem = elem.strip(" ")
                elem = elem.strip("\n")
                wrong_trans_strip.append(elem.strip(" "))

            occupation_translations[key]: dict = {}
            occupation_translations[key]["female"] = fem_trans_strip
            occupation_translations[key]["male"] = male_trans_strip
            if neutral_trans_strip != ['']:
                occupation_translations[key]["neutral"] = neutral_trans_strip
            else:
                occupation_translations[key]["neutral"] = ["NoValueInList"]
            if wrong_trans_strip != ['']:
                occupation_translations[key]["wrong"] = wrong_trans_strip
            else:
                occupation_translations[key]["wrong"] = ["NoValueInList"]

    print("You opened: " + Path(file_path).name)
    return occupation_translations
