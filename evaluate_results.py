import string
import random

from reader_saver import load_nested_list_to_dict, load_nested_list_to_list, write_nested_list_to_file, get_file_saver_instance

from get_ressources import get_ceo_dat_akk_sentences


def special_rules_dativ_akkusativ(translation: str, case_dependent_occupations: list) -> str:
    translation = translation.translate(str.maketrans('', '', string.punctuation))
    male_articles = ["den", "dem", "des", "beim", "vom"]
    female_articles = ["der", "die"]
    for case_dependent_occupation in case_dependent_occupations:
        if " " + case_dependent_occupation.lower() + " " in translation.lower():
            words: list = translation.lower().split(" ")
            try:
                index_of_article: int = words.index(case_dependent_occupation.lower()) - 2
            except ValueError:
                print(translation)
                continue
            try:
                if index_of_article >= 0:
                    article: str = words[index_of_article].lower()
                else:
                    article: str = "article index -1"
                possible_article: str = words[index_of_article + 1].lower()
            except IndexError:
                print(10 * "Special rule index is out of range\n")
                continue
            if article in male_articles or possible_article in male_articles:
                return "male"
            elif article in female_articles or possible_article in female_articles:
                return "female"
            else:
                print(translation)
                print("article:", article)
                print("possible_article:", possible_article)
                print(10 * "NO MATCHING ARTICLE\n")
                return False
    return False


def special_rules_nominativ(translation: str, case_dependent_occupations: list) -> str:
    special_found_male = False
    special_found_female = False
    translation = translation.translate(str.maketrans("", "", string.punctuation))
    for case_dependent_occupation in case_dependent_occupations:
        if " " + case_dependent_occupation.lower() + " " in translation.lower():
            words: list = translation.lower().split(" ")
            try:
                index_of_article: int = words.index(case_dependent_occupation.lower()) - 2
            except ValueError:
                print(translation)
                continue
            try:
                if index_of_article >= 0:
                    article: str = words[index_of_article].lower()
                else:
                    article: str = "article index -1"
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
                    wrong_occ_trans_plus_in = wrong_occ_trans + "in "
                    if wrong_occ_trans_plus_spaces in translation or wrong_occ_trans_plus_in in translation:
                        wrong_found = True
                if wrong_found:
                    translation_data.append("wrong")
                if get_special_rules_list(occupation, "dativ") is not None:
                    occupation_trans_case_dependent: list = get_special_rules_list(occupation, "dativ")
                    if int(female_found) + int(male_found) + int(neutral_found) + int(wrong_found) < 1:
                        if special_rules_dativ_akkusativ(translation, occupation_trans_case_dependent) is not False:
                            special_found = True
                            translation_data.append(special_rules_dativ_akkusativ(translation, occupation_trans_case_dependent))
                if get_special_rules_list(occupation, "nominativ") is not None:
                    occupation_trans_case_dependent: list = get_special_rules_list(occupation, "nominativ")
                    if int(female_found) + int(male_found) + int(neutral_found) + int(wrong_found) < 1:
                        if special_rules_nominativ(translation, occupation_trans_case_dependent) is not False:
                            special_found = True
                            translation_data.append(special_rules_nominativ(translation, occupation_trans_case_dependent))

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
        translations_data.sort(key=lambda x: x[3])
        for translation_data in translations_data:
            occupation = translation_data[3].split(" ")[1]
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
                    if female_occ_trans_plus_spaces in translation:
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
                if get_special_rules_list(occupation, "dativ") is not None:
                    occupation_trans_case_dependent: list = get_special_rules_list(occupation, "dativ")
                    if int(female_found) + int(male_found) + int(neutral_found) + int(wrong_found) < 1:
                        if special_rules_dativ_akkusativ(translation, occupation_trans_case_dependent) is not False:
                            special_found = True
                            translation_data.append(special_rules_dativ_akkusativ(translation, occupation_trans_case_dependent))
                if get_special_rules_list(occupation, "nominativ") is not None:
                    occupation_trans_case_dependent: list = get_special_rules_list(occupation, "nominativ")
                    if int(female_found) + int(male_found) + int(neutral_found) + int(wrong_found) < 1:
                        if special_rules_nominativ(translation, occupation_trans_case_dependent) is not False:
                            special_found = True
                            translation_data.append(special_rules_nominativ(translation, occupation_trans_case_dependent))

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
    write_nested_list_to_file(translations_data)
    return


def evaluate_gender_of_translation_after_sample(data_structure: str = "verb_sentences"):
    print("Choose the list of categorized translations:")
    categorized_translations = load_nested_list_to_list()

    # print("Choose the list of occupation translations:")
    # occupation_translations_complete_list = load_nested_list_to_list()

    changed_categorizations: list = []

    for translation_data in categorized_translations:
        occupation = translation_data[3].split(" ")[1]
        translation = translation_data[8].translate(str.maketrans("", "", string.punctuation))
        if occupation == "CEO":
            new_classification = None
            if " vorstandsvorsitzende " in translation.lower() and " ceo " not in translation.lower():
                new_classification = special_rules_nominativ(translation, ["Vorstandsvorsitzende"])
            elif " vorstandsvorsitzenden " in translation.lower() and " ceo " not in translation.lower():
                new_classification = special_rules_nominativ(translation, ["Vorstandsvorsitzenden"])
            elif " geschäftsführerin " in translation.lower() and " ceo " not in translation.lower():
                new_classification = "female"
            elif " geschäftsführer " in translation.lower() and " ceo " not in translation.lower():
                new_classification = "male"
            elif translation_data[3] == "The CEO":
                new_classification = special_rules_nominativ(translation, ["CEO"])
            elif translation_data[3] == "the CEO":
                dativ_akkusativ_sentences = get_ceo_dat_akk_sentences()
                dat_akk: bool = False
                for dat_akk_sentence in dativ_akkusativ_sentences:
                    # case for dativ
                    if dat_akk_sentence.lower() in translation_data[2].lower():
                        dat_akk = True
                        new_classification = special_rules_dativ_akkusativ(translation, ["CEO"])
                # case for nominativ
                if not dat_akk:
                    new_classification = special_rules_nominativ(translation, ["CEO"])
            else:
                print("NO CEO CASE DETECTED")
                print(translation_data)
            if new_classification is not None:
                if new_classification != translation_data[9]:
                    translation_data[9] = new_classification
                    changed_categorizations.append(translation_data)
        elif occupation == "clerk":
            new_classification = None
            # print("Occupation is clerk / supervisor")
            clerk_nominativ: list = ["Angestellte"]
            clerk_dativ: list = ["Angestellten", "Büroangestellten"]

            for elem in clerk_nominativ:
                if " " + elem.lower() + " " in translation.lower():
                    new_classification = special_rules_nominativ(translation, clerk_nominativ)
                    if new_classification != translation_data[9]:
                        print(translation_data)
                        translation_data[9] = new_classification
                        changed_categorizations.append(translation_data)
            for elem in clerk_dativ:
                if " " + elem.lower() + " " in translation.lower():
                    new_classification = special_rules_dativ_akkusativ(translation, clerk_dativ)
                    if new_classification != translation_data[9]:
                        print(translation_data)
                        translation_data[9] = new_classification
                        changed_categorizations.append(translation_data)
        elif occupation == "supervisor":
            new_classification = None

            supervisor_nominativ: list = ["Vorgesetzte"]
            supervisor_dativ: list = ["Vorgesetzten"]

            for elem in supervisor_nominativ:
                if " " + elem.lower() + " " in translation.lower():
                    new_classification = special_rules_nominativ(translation, supervisor_nominativ)
                    if new_classification != translation_data[9]:
                        print(translation_data)
                        translation_data[9] = new_classification
                        changed_categorizations.append(translation_data)
            for elem in supervisor_dativ:
                if " " + elem.lower() + " " in translation.lower():
                    new_classification = special_rules_dativ_akkusativ(translation, supervisor_dativ)
                    if new_classification != translation_data[9]:
                        translation_data[9] = new_classification
                        print(translation_data)
                        changed_categorizations.append(translation_data)
    print("SAVE ALL CHANGED CATEGORIZATIONS:")
    write_nested_list_to_file(changed_categorizations)
    return


def get_special_rules_list(occupation: str, case: str) -> list:
    if occupation == "clerk":
        if case == "nominativ":
            return ["Angestellte"]
        if case == "dativ":
            return ["Angestellten", "Büroangestellten"]
    elif occupation == "attendant":
        if case == "nominativ":
            return ["Bedienstete", "Anwesende"]
        if case == "dativ":
            return ["Bediensteten", "Anwesenden"]
    elif occupation == "supervisor":
        if case == "nominativ":
            return ["Vorgesetzte"]
        if case == "dativ":
            return ["Vorgesetzten"]
    elif occupation == "CEO":
        if case == "nominativ":
            return ["Vorstandsvorsitzende"]
        if case == "dativ":
            return ["Vorstandsvorsitzenden"]
    elif occupation == "paralegal":
        if case == "nominativ":
            return ["Rechtsanwaltsfachangestellte"]
        if case == "dativ":
            return ["Rechtsanwaltsfachangestellten"]
    elif occupation == "receptionist":
        if case == "nominativ":
            return None
        if case == "dativ":
            return ["Rezeptionisten"]
    return None


def get_special_rules_list_after_sample(occupation: str, case: str) -> list:
    if occupation == "clerk":
        if case == "nominativ":
            return ["Angestellte"]
        if case == "dativ":
            return ["Angestellten", "Büroangestellten"]
    elif occupation == "supervisor":
        if case == "nominativ":
            return ["Vorgesetzte"]
        if case == "dativ":
            return ["Vorgesetzten"]
    elif occupation == "CEO":
        if case == "nominativ":
            return ["Vorstandsvorsitzende", "CEO"]
        if case == "dativ":
            return ["Vorstandsvorsitzenden", "CEO"]
    elif occupation == "CTO":
        if case == "nominativ":
            return ["CTO"]
        if case == "dativ":
            return ["CTO"]
    elif occupation == "CFO":
        if case == "nominativ":
            return ["CFO"]
        if case == "dativ":
            return ["CFO"]
    return None


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
    n_of_categorized_lines: int = 1
    for translation_data in translations:
        if continue_manual_classification:
            if len(translation_data) == 10:
                append_value: str = None
            else:
                if len(translation_data) > 10:
                    del translation_data[9:]
                try:
                    append_value: str = None
                    try_to_classify: bool = True
                    while try_to_classify:
                        print("Categorization", str(n_of_categorized_lines) + "/" + str(n_of_lines_to_categorize))
                        occupation = translation_data[3].split(" ")[1]
                        print("Occupation:", occupation.upper())
                        print(translation_data[2].replace(occupation, occupation.upper()), "\n")
                        print(translation_data[8], "\n")
                        print("female = 1; male = 2, neutral = 3, wrong = 4; finish & save = 5")
                        try:
                            translation_category: int = int(input("Enter the corresponding number:"))
                            if translation_category < 1 or translation_category > 5:
                                raise ValueError
                            elif translation_category == 1:
                                # load GloVe
                                print(5 * "FEMALE ")
                                try:
                                    correct_input: str = str(input("Enter 'y' if input is correct:"))
                                    if correct_input != "y":
                                        raise ValueError
                                    append_value = "female"
                                    try_to_classify = False
                                except ValueError:
                                    print("type 'y' to confirm correct int input: Input not confirmed TRY AGAIN")
                            elif translation_category == 2:
                                # load GloVe
                                print(5 * "MALE ")
                                try:
                                    correct_input: str = str(input("Enter 'y' if input is correct:"))
                                    if correct_input != "y":
                                        raise ValueError
                                    append_value = "male"
                                    try_to_classify = False
                                except ValueError:
                                    print("type 'y' to confirm correct int input: Input not confirmed TRY AGAIN")
                            elif translation_category == 3:
                                print(5 * "NEUTRAL ")
                                try:
                                    correct_input: str = str(input("Enter 'y' if input is correct:"))
                                    if correct_input != "y":
                                        raise ValueError
                                    append_value = "neutral"
                                    try_to_classify = False
                                except ValueError:
                                    print("type 'y' to confirm correct int input: Input not confirmed TRY AGAIN")
                            elif translation_category == 4:
                                print(5 * "WRONG ")
                                try:
                                    correct_input: str = str(input("Enter 'y' if input is correct:"))
                                    if correct_input != "y":
                                        raise ValueError
                                    append_value = "wrong"
                                    try_to_classify = False
                                except ValueError:
                                    print("type 'y' to confirm correct int input: Input not confirmed TRY AGAIN")
                            elif translation_category == 5:
                                print("DO YOU REALLY WANT TO FINISH CLASSIFICATION?")
                                try:
                                    correct_input: str = str(input("Enter 'y' if input is correct:"))
                                    if correct_input != "y":
                                        raise ValueError
                                    append_value = None
                                    try_to_classify = False
                                    continue_manual_classification = False
                                except ValueError:
                                    print("type 'y' to confirm correct int input: Input not confirmed TRY AGAIN")
                        except ValueError:
                            print("Please enter an int between 1 - 5")
                        if append_value is not None:
                            n_of_categorized_lines += 1
                except TypeError:
                    print(TypeError)
                    print(translation_data)
                    file_saver.write(translation_data[0])
                    for value in translation_data[1:]:
                        file_saver.write("\t")
                        file_saver.write(str(value))
                    file_saver.write("\n")
        if append_value is not None:
            translation_data.append(append_value)
        file_saver.write(translation_data[0])
        for value in translation_data[1:]:
            file_saver.write("\t")
            file_saver.write(str(value))
        file_saver.write("\n")
    file_saver.close()
    print("FINISHED & SAVED FILE")


def control_sample_wb(translations_to_sample_test: list = None):
    # choose file to load
    if translations_to_sample_test is not None:
        translations = translations_to_sample_test
    else:
        print("Choose translations to sample test:")
        translations = load_nested_list_to_list()
    n_of_translations = len(translations)
    one_percent_val: int = int(n_of_translations / 20)
    # create list of random indexes
    random_indexes = random.sample(range(n_of_translations), one_percent_val)
    random_translations = []
    for random_index in random_indexes:
        random_translations.append(translations[random_index])
    random_translations.sort(key=lambda x: x[3].split(" ")[1])
    # count lines with wrong length:
    n_of_lines_to_categorize: int = one_percent_val
    # choose file to save
    file_saver = get_file_saver_instance(".txt")
    n_of_categorized_lines: int = 1
    continue_manual_classification = True
    while continue_manual_classification:
        for i, random_translation in enumerate(random_translations):
            if not continue_manual_classification:
                break
            if i == len(random_translations) - 1:
                continue_manual_classification = False
            append_value = None
            try:
                try_to_classify: bool = True
                while try_to_classify:
                    print("Categorization", str(n_of_categorized_lines) + "/" + str(n_of_lines_to_categorize))
                    occupation = random_translation[3].split(" ")[1]
                    print("Occupation:", occupation.upper())
                    print(random_translation[2].replace(occupation, occupation.upper()), "\n")
                    print(random_translation[8], "\n")
                    print("Classification:", random_translation[9].upper(), "\n")
                    print("correct = 1; incorrect = 2; finish & save = 3")
                    try:
                        translation_category: int = int(input("Enter the corresponding number:"))
                        if translation_category < 1 or translation_category > 3:
                            raise ValueError
                        elif translation_category == 1:
                            print(5 * "CORRECT ")
                            try:
                                correct_input: str = str(input("Enter 'y' if input is correct:"))
                                if correct_input != "y":
                                    raise ValueError
                                append_value = "CORRECT"
                                try_to_classify = False
                            except ValueError:
                                print("type 'y' to confirm correct int input: Input not confirmed TRY AGAIN")
                        elif translation_category == 2:
                            print(5 * "INCORRECT ")
                            try:
                                correct_input: str = str(input("Enter 'y' if input is correct:"))
                                if correct_input != "y":
                                    raise ValueError
                                append_value = "INCORRECT"
                                try_to_classify = False
                            except ValueError:
                                print("type 'y' to confirm correct int input: Input not confirmed TRY AGAIN")
                        elif translation_category == 3:
                            print("DO YOU REALLY WANT TO FINISH CLASSIFICATION?")
                            try:
                                correct_input: str = str(input("Enter 'y' if input is correct:"))
                                if correct_input != "y":
                                    raise ValueError
                                append_value = None
                                try_to_classify = False
                                continue_manual_classification = False
                            except ValueError:
                                print("type 'y' to confirm correct int input: Input not confirmed TRY AGAIN")
                    except ValueError:
                        print("Please enter an int between 1 - 3")
                    if append_value is not None:
                        n_of_categorized_lines += 1
            except TypeError:
                print(TypeError)
                print(random_translation)
            if append_value is not None:
                random_translation.append(append_value)
            file_saver.write(random_translation[0])
            for value in random_translation[1:]:
                file_saver.write("\t")
                file_saver.write(str(value))
            file_saver.write("\n")
    file_saver.close()
    print("FINISHED MANUAL CLASSIFICATION")


def control_sample_verbs():
    # choose file to load
    translations = load_nested_list_to_list()
    n_of_translations = len(translations)
    one_percent_val: int = int(n_of_translations / 20)
    # create list of random indexes
    random_indexes = random.sample(range(n_of_translations), one_percent_val)
    random_translations = []
    for random_index in random_indexes:
        random_translations.append(translations[random_index])
    random_translations.sort(key=lambda x: x[3])
    # count lines with wrong length:
    n_of_lines_to_categorize: int = one_percent_val
    # choose file to save
    file_saver = get_file_saver_instance(".txt")
    n_of_categorized_lines: int = 1
    continue_manual_classification = True
    while continue_manual_classification:
        for i, random_translation in enumerate(random_translations):
            if not continue_manual_classification:
                break
            if i == len(random_translations) - 1:
                continue_manual_classification = False
            append_value = None
            try:
                try_to_classify: bool = True
                while try_to_classify:
                    print("Categorization", str(n_of_categorized_lines) + "/" + str(n_of_lines_to_categorize))
                    occupation = random_translation[3]
                    print("Occupation:", occupation.upper())
                    print(random_translation[1].replace(occupation, occupation.upper()), "\n")
                    print(random_translation[4], "\n")
                    print("Classification:", random_translation[5].upper(), "\n")
                    print("correct = 1; incorrect = 2; finish & save = 3")
                    try:
                        translation_category: int = int(input("Enter the corresponding number:"))
                        if translation_category < 1 or translation_category > 3:
                            raise ValueError
                        elif translation_category == 1:
                            print(5 * "CORRECT ")
                            try:
                                correct_input: str = str(input("Enter 'y' if input is correct:"))
                                if correct_input != "y":
                                    raise ValueError
                                append_value = "CORRECT"
                                try_to_classify = False
                            except ValueError:
                                print("type 'y' to confirm correct int input: Input not confirmed TRY AGAIN")
                        elif translation_category == 2:
                            print(5 * "INCORRECT ")
                            try:
                                correct_input: str = str(input("Enter 'y' if input is correct:"))
                                if correct_input != "y":
                                    raise ValueError
                                append_value = "INCORRECT"
                                try_to_classify = False
                            except ValueError:
                                print("type 'y' to confirm correct int input: Input not confirmed TRY AGAIN")
                        elif translation_category == 3:
                            print("DO YOU REALLY WANT TO FINISH CLASSIFICATION?")
                            try:
                                correct_input: str = str(input("Enter 'y' if input is correct:"))
                                if correct_input != "y":
                                    raise ValueError
                                append_value = None
                                try_to_classify = False
                                continue_manual_classification = False
                            except ValueError:
                                print("type 'y' to confirm correct int input: Input not confirmed TRY AGAIN")
                    except ValueError:
                        print("Please enter an int between 1 - 3")
                    if append_value is not None:
                        n_of_categorized_lines += 1
            except TypeError:
                print(TypeError)
                print(random_translation)
            if append_value is not None:
                random_translation.append(append_value)
            file_saver.write(random_translation[0])
            for value in random_translation[1:]:
                file_saver.write("\t")
                file_saver.write(str(value))
            file_saver.write("\n")
    file_saver.close()
    print("FINISHED MANUAL CLASSIFICATION")



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