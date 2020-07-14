from reader_saver import load_nested_list_to_dict, load_nested_list_to_list, write_nested_list_to_file


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
            translation = translation_data[4]
            try:
                female_found: bool = False
                male_found: bool = False
                neutral_found: bool = False
                wrong_found: bool = False
                # find female translations
                for female_occ_trans in occupation_trans[occupation]["female"]:
                    female_occ_trans_plus_spaces = female_occ_trans + " "
                    if female_occ_trans_plus_spaces.lower() in translation.lower():
                        female_found = True
                if female_found:
                    translation_data.append("female")
                # find male translations
                for male_occ_trans in occupation_trans[occupation]["male"]:
                    male_occ_trans_plus_spaces = male_occ_trans + " "
                    if male_occ_trans_plus_spaces.lower() in translation.lower():
                        male_found = True
                if male_found:
                    translation_data.append("male")
                # find neutral translations
                for neutral_occ_trans in occupation_trans[occupation]["neutral"]:
                    neutral_occ_trans_plus_spaces = neutral_occ_trans + " "
                    if neutral_occ_trans_plus_spaces.lower() in translation.lower():
                        neutral_found = True
                if neutral_found:
                    translation_data.append("neutral")
                # find wrong translations
                for wrong_occ_trans in occupation_trans[occupation]["wrong"]:
                    wrong_occ_trans_plus_spaces = wrong_occ_trans + " "
                    if wrong_occ_trans_plus_spaces.lower() in translation.lower():
                        wrong_found = True
                if wrong_found:
                    translation_data.append("wrong")

                if not female_found and not male_found and not neutral_found and not wrong_found:
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
        n_of_len_above_six = 0
        n_of_unclassified_sentences = 0
        for translation_data in translations_data:
            occupation = translation_data[3].split(" ")[1]
            translation = translation_data[8]
            try:
                female_found: bool = False
                male_found: bool = False
                neutral_found: bool = False
                wrong_found: bool = False
                # find female translations
                for female_occ_trans in occupation_trans[occupation]["female"]:
                    female_occ_trans_plus_spaces = female_occ_trans + " "
                    female_occ_trans_plus_comma = female_occ_trans + ","
                    if female_occ_trans_plus_spaces.lower() in translation.lower() or female_occ_trans_plus_comma.lower() in translation.lower():
                        female_found = True
                if female_found:
                    translation_data.append("female")
                # find male translations
                for male_occ_trans in occupation_trans[occupation]["male"]:
                    male_occ_trans_plus_spaces = male_occ_trans + " "
                    male_occ_trans_plus_comma = male_occ_trans + ","
                    male_occ_trans_plus_s = male_occ_trans + "s "

                    if male_occ_trans_plus_spaces.lower() in translation.lower() or male_occ_trans_plus_comma.lower() in translation.lower() or male_occ_trans_plus_s.lower() in translation.lower():
                        male_found = True
                if male_found:
                    translation_data.append("male")
                # find neutral translations
                for neutral_occ_trans in occupation_trans[occupation]["neutral"]:
                    neutral_occ_trans_plus_spaces = neutral_occ_trans + " "
                    neutral_occ_trans_plus_comma = neutral_occ_trans + ","
                    if neutral_occ_trans_plus_spaces.lower() in translation.lower() or neutral_occ_trans_plus_comma.lower() in translation.lower():
                        neutral_found = True
                if neutral_found:
                    translation_data.append("neutral")
                # find wrong translations
                for wrong_occ_trans in occupation_trans[occupation]["wrong"]:
                    wrong_occ_trans_plus_spaces = wrong_occ_trans + " "
                    wrong_occ_trans_plus_comma = wrong_occ_trans + ","
                    if wrong_occ_trans_plus_spaces.lower() in translation.lower() or wrong_occ_trans_plus_comma.lower() in translation.lower():
                        wrong_found = True
                if wrong_found:
                    translation_data.append("wrong")

                if not female_found and not male_found and not neutral_found and not wrong_found:
                    n_of_unclassified_sentences += 1
                    print("NO OCCUPATION TRANSLATION FOUND:")
                    print(translation_data)
                    print("Number of unclassified sentences:", n_of_unclassified_sentences)
                if len(translation_data) > 10:
                    n_of_len_above_six += 1
                    print("MULTIPLE OCCUPATION TRANSLATIONS FOUND:")
                    print(translation_data)
                    print("NEUTRAL LIST VALUES")
                    print("BEGINNING" + str(occupation_trans[occupation]["neutral"]) + "ENDING")
                    print("WRONG LIST VALUES")
                    print("BEGINNING" + str(occupation_trans[occupation]["wrong"]) + "ENDING")
                    print("Number of lines with length above 9: ", n_of_len_above_six)
                    print("Length of translation_data:", len(translation_data))
            except KeyError:
                print("KeyError in: ", occupation)
                print("Data: ", translation_data)
    write_nested_list_to_file(translations_data)
    return
