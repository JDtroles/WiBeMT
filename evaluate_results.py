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
        for translation_data in translations_data:
            occupation = translation_data[3]
            translation = translation_data[4]
            try:
                found: bool = False
                for female_occ_trans in occupation_trans[occupation]["female"]:
                    female_occ_trans_plus_spaces = " " + female_occ_trans + " "
                    if female_occ_trans_plus_spaces in translation:
                        found = True
                        translation_data.append("female")
                if not found:
                    for male_occ_trans in occupation_trans[occupation]["male"]:
                        male_occ_trans_plus_spaces = " " + male_occ_trans + " "
                        if male_occ_trans_plus_spaces in translation:
                            found = True
                            translation_data.append("male")
                if not found:
                    print("NO OCCUPATION TRANSLATION FOUND:")
                    print(translation_data)
            except KeyError:
                print("KeyError in: ", occupation)
                print("Data: ", translation_data)
    elif data_structure == "WinoBias":
        a = 23
    write_nested_list_to_file(translations_data)
    return
