import string

from reader_saver import load_nested_list_to_dict, load_nested_list_to_list, write_nested_list_to_file, get_file_saver_instance


def special_rules_dativ_akkusativ(translation: str) -> str:
    case_dependent_occupations: list = ["Angestellten", "Büroangestellten", "Bediensteten", "Vorgesetzten",
                                        "Anwesenden", "Vorstandsvorsitzenden", "Beratenden"]
    for case_dependent_occupation in case_dependent_occupations:
        if " " + case_dependent_occupation in translation:
            words: list = translation.split(" ")
            for index, word in enumerate(words):
                words[index] = word.strip(",")
            try:
                index_of_article: int = words.index(case_dependent_occupation) - 2
            except ValueError:
                print(translation)
                continue
            try:
                article: str = words[index_of_article].lower()
                possible_article: str = words[index_of_article + 1].lower()
            except IndexError:
                print(10 * "Special rule index is out of range\n")
                continue
            if article == "den" or article == "dem" or article == "des" or article == "beim" or article == "vom" or\
                    possible_article == "den" or possible_article == "dem" or possible_article == "des" or \
                    possible_article == "beim" or possible_article == "vom":
                return "male"
            elif article == "der" or possible_article == "der":
                return "female"
            else:
                print(translation)
                print("article:", article)
                print("possible_article:", possible_article)
                print(10 * "NO MATCHING ARTICLE\n")
                return False
    return False


# TODO: check "Vorgesetzte"
def special_rules_nominativ(translation: str) -> str:
    special_found_male = False
    special_found_female = False
    case_dependent_occupations: list = ["Angestellte", "Bedienstete", "Vorgesetzte", "Anwesende",
                                        "Vorstandsvorsitzende"]
    for case_dependent_occupation in case_dependent_occupations:
        if " " + case_dependent_occupation + " " in translation:
            words: list = translation.split(" ")
            for index, word in enumerate(words):
                words[index] = word.strip(",")
            try:
                index_of_article: int = words.index(case_dependent_occupation) - 2
            except ValueError:
                print(translation)
                continue
            try:
                article: str = words[index_of_article].lower()
                possible_article: str = words[index_of_article + 1].lower()
            except IndexError:
                print(10 * "Special rule index is out of range\n")
                continue
            if article == "der" or possible_article == "der":
                special_found_male = True
            elif article == "die" or possible_article == "die":
                special_found_female = True
    if special_found_male:
        return "male"
    elif special_found_female:
        return "female"
    else:
        return False


def evaluate_gender_of_translation(data_structure: str = "verb_sentences"):
    """

    :param data_structure: "verb_sentences" or "WinoBias"
    :type data_structure: str
    """
    print("Choose the occupation for evaluation: ")
    occupation_trans: dict = load_nested_list_to_dict()

    print("Choose the", data_structure, "you want to load:")
    translations_data = load_nested_list_to_list()

    if data_structure == "verb_sentences":
        n_of_len_above_six = 0
        for translation_data in translations_data:
            occupation = translation_data[3]
            translation = translation_data[4].translate(str.maketrans('', '', string.punctuation))
            translation = translation + " "

            try:
                female_found: bool = False
                male_found: bool = False
                neutral_found: bool = False
                wrong_found: bool = False
                special_found: bool = False
                # find female translations
                for female_occ_trans in occupation_trans[occupation]["female"]:
                    female_occ_trans_plus_spaces = female_occ_trans + " "
                    if female_occ_trans_plus_spaces in translation:
                        female_found = True
                if female_found:
                    translation_data.append("female")
                # find male translations
                for male_occ_trans in occupation_trans[occupation]["male"]:
                    male_occ_trans_plus_spaces = male_occ_trans + " "
                    if male_occ_trans_plus_spaces in translation:
                        male_found = True
                if male_found:
                    translation_data.append("male")
                # find neutral translations
                for neutral_occ_trans in occupation_trans[occupation]["neutral"]:
                    neutral_occ_trans_plus_spaces = neutral_occ_trans + " "
                    if neutral_occ_trans_plus_spaces in translation:
                        neutral_found = True
                if neutral_found:
                    translation_data.append("neutral")
                # find wrong translations
                for wrong_occ_trans in occupation_trans[occupation]["wrong"]:
                    wrong_occ_trans_plus_spaces = wrong_occ_trans + " "
                    if wrong_occ_trans_plus_spaces in translation:
                        wrong_found = True
                if wrong_found:
                    translation_data.append("wrong")
                if special_rules_dativ_akkusativ(translation) is not False:
                    special_found = True
                    translation_data.append(special_rules_dativ_akkusativ(translation))

                if not female_found and not male_found and not neutral_found and not wrong_found and not special_found:
                    print("NO OCCUPATION TRANSLATION FOUND:")
                    print(translation_data)
                if len(translation_data) > 6:
                    n_of_len_above_six += 1
                    print("MULTIPLE OCCUPATION TRANSLATIONS FOUND:")
                    print(translation_data)
                    print("NEUTRAL LIST VALUES")
                    print("BEGINNING" + str(occupation_trans[occupation]["neutral"]) + "ENDING")
                    print("WRONG LIST VALUES")
                    print("BEGINNING" + str(occupation_trans[occupation]["wrong"]) + "ENDING")
                    print("Number of lines with length above 6: ", n_of_len_above_six)
                    print("Length of translation_data:", len(translation_data))
            except KeyError:
                print("KeyError in: ", occupation)
                print("Data: ", translation_data)
    elif data_structure == "WinoBias":
        n_of_unclassified_sentences = 0
        n_of_construction_sentences = 0
        translations_data.sort(key=lambda x: x[3])
        for translation_data in translations_data:
            occupation = translation_data[3].split(" ")[1]
            if occupation == "construction":
                n_of_construction_sentences += 1
                continue
            translation = translation_data[8].translate(str.maketrans('', '', string.punctuation))
            translation = translation + " "

            try:
                female_found: bool = False
                male_found: bool = False
                neutral_found: bool = False
                wrong_found: bool = False
                special_found: bool = False
                # find female translations
                for female_occ_trans in occupation_trans[occupation]["female"]:
                    female_occ_trans_plus_spaces = " " + female_occ_trans + " "
                    female_occ_trans_plus_comma = " " + female_occ_trans + ","
                    if female_occ_trans_plus_spaces in translation or female_occ_trans_plus_comma in translation:
                        female_found = True
                if female_found:
                    translation_data.append("female")
                # find male translations
                for male_occ_trans in occupation_trans[occupation]["male"]:
                    male_occ_trans_plus_spaces = " " + male_occ_trans + " "
                    male_occ_trans_plus_s = " " + male_occ_trans + "s "

                    if male_occ_trans_plus_spaces in translation or male_occ_trans_plus_s in translation:
                        male_found = True
                if male_found:
                    translation_data.append("male")
                # find neutral translations
                for neutral_occ_trans in occupation_trans[occupation]["neutral"]:
                    neutral_occ_trans_plus_spaces = " " + neutral_occ_trans + " "
                    neutral_occ_trans_plus_s = " " + neutral_occ_trans + "s "
                    if neutral_occ_trans_plus_spaces in translation or neutral_occ_trans_plus_s in translation:
                        neutral_found = True
                if neutral_found:
                    translation_data.append("neutral")
                # find wrong translations
                for wrong_occ_trans in occupation_trans[occupation]["wrong"]:
                    wrong_occ_trans_plus_spaces = " " + wrong_occ_trans + " "
                    wrong_occ_trans_plus_in = " " + wrong_occ_trans + "in "
                    wrong_occ_trans_plus_s = " " + wrong_occ_trans + "s "
                    if wrong_occ_trans_plus_spaces in translation or wrong_occ_trans_plus_s in translation or \
                            wrong_occ_trans_plus_in in translation or \
                            " Debonair" in translation or " Suave" in translation:
                        wrong_found = True
                if wrong_found:
                    translation_data.append("wrong")
                if int(female_found) + int(male_found) + int(neutral_found) + int(wrong_found) < 1:
                    if special_rules_dativ_akkusativ(translation) is not False:
                        special_found = True
                        translation_data.append(special_rules_dativ_akkusativ(translation))
                    if special_rules_nominativ(translation) is not False:
                        special_found = True
                        translation_data.append(special_rules_nominativ(translation))

                if not female_found and not male_found and not neutral_found and not wrong_found and not special_found:
                    n_of_unclassified_sentences += 1
                    print("NO OCCUPATION TRANSLATION FOUND:")
                    print(translation_data)
                    print(translation)
                    print("Number of unclassified sentences:", n_of_unclassified_sentences)
            except KeyError:
                print("KeyError in: ", occupation)
                print("Data: ", translation_data)
    n_of_len_above_six = 0
    for elem in translations_data:
        if len(elem) > 10:
            n_of_len_above_six += 1
            print("MULTIPLE OCCUPATION TRANSLATIONS FOUND:")
            print(elem)
            # TODO: add printout of occupation lists
            print("Number of lines with length above 9: ", n_of_len_above_six)
            print("Length of translation_data:", len(elem))
    print("Number of construction worker sentences:", n_of_construction_sentences)
    write_nested_list_to_file(translations_data)
    return


def manual_evaluation():
    # choose file to load
    translations = load_nested_list_to_list()
    # count lines with wrong length:
    n_of_lines_to_categorize: int = 0
    for translation_data in translations:
        if len(translation_data) != 10:
            n_of_lines_to_categorize += 1
    # choose file to save
    file_saver = get_file_saver_instance(".txt")
    continue_manual_classification: bool = True
    for translation_data in translations:
        if continue_manual_classification:
            if len(translation_data) == 9:
                for elem in translation_data:
                    file_saver.write(elem)
                    file_saver.write("\t")
                file_saver.write("\n")
            else:
                try:
                    print("Occupation:", translation_data[3])
                    print(translation_data[2])
                    print(translation_data[8])
                    print("male = 1; female = 2, neutral = 3, wrong = 4; finish & save = 5")
                    append_value: str = "WRONG \t WRONG"
                    while True:
                        # TODO: add check step to each "if" to verify if input was intended
                        try:
                            embedding_type_int = int(input("Enter the corresponding number:"))
                            if embedding_type_int < 1 or embedding_type_int > 5:
                                raise ValueError
                            elif embedding_type_int == 1:
                                # load GloVe
                                print("You chose FEMALE")
                                append_value = "female"
                                break
                            elif embedding_type_int == 2:
                                # load GloVe
                                print("You chose MALE")
                                append_value = "male"
                                break
                            elif embedding_type_int == 3:
                                # load GloVe
                                print("You chose NEUTRAL")
                                append_value = "neutral"
                                break
                            elif embedding_type_int == 4:
                                # load GloVe
                                print("You chose WRONG")
                                append_value = "wrong"
                                break
                            elif embedding_type_int == 5:
                                # TODO: add check step
                                continue_manual_classification = False
                        except ValueError:
                            print("Please enter an int between 1 - 5")
                except TypeError:
                    print(TypeError)
                    print(translation_data)
                    for elem in translation_data:
                        file_saver.write(elem)
                        file_saver.write("\t")
                    file_saver.write("\n")
                # TODO: add saving to file

        file_saver.close()

    # seperate line
    # check len of line
    # if len of line wrong:
        # print counter: current_n_of_line / total_n_of_lines
        # print occ
        # print sentence
        # print translation
        # let choose class of translation:
            # wrong, neutral, female, male
        # pop elements behind position X
        # append manual chosen classification
        # write line to file during runtime