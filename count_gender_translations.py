from reader_saver import load_nested_list_to_list, write_nested_list_to_file


def get_statistical_measures(translations):
    statistical_measures = []
    for elem in translations:
        try:
            wrong_percentage = elem[6] / (elem[1] + elem[2] + elem[3] + elem[4] + elem[5])
            true_female_rate = elem[1] / (elem[1] + elem[4])
            true_male_rate = elem[3] / (elem[3] + elem[2])
            female_predictive_value = elem[1] / (elem[1] + elem[2])
            male_predictive_value = elem[3] / (elem[3] + elem[4])
            statistical_measures.append(
                [elem[0], wrong_percentage, true_female_rate, true_male_rate, female_predictive_value,
                 male_predictive_value])
        except ZeroDivisionError:
            print(elem[0], "DIVISION BY ZERO AT SOME POINT")
    return statistical_measures


def get_results_winobias_sentences():
    winobias_sentences = load_nested_list_to_list()

    # get all occupations
    unique_occupations = get_unique_occupations_from_winobias_sentences(winobias_sentences)

    # get all verbs
    unique_adjectives = get_unique_adjectives(winobias_sentences)

    occupation_translations = evaluate_translation_gender_winobias_sentences(unique_occupations, winobias_sentences,
                                                                             mode="occupations_winobias")
    adjective_translations = evaluate_translation_gender_winobias_sentences(unique_adjectives, winobias_sentences,
                                                                            mode="adjectives")

    statistical_measures_occupations = get_statistical_measures(occupation_translations)
    statistical_measures_adjectives = get_statistical_measures(adjective_translations)

    statistical_measures_occupations.sort(key=lambda x: x[1])
    for elem in statistical_measures_occupations:
        print(elem)
    statistical_measures_occupations.sort(key=lambda x: x[2])
    for elem in statistical_measures_occupations:
        print(elem)
    statistical_measures_occupations.sort(key=lambda x: x[3])
    for elem in statistical_measures_occupations:
        print(elem)

    statistical_measures_adjectives.sort(key=lambda x: x[1])
    for elem in statistical_measures_occupations:
        print(elem)
    statistical_measures_adjectives.sort(key=lambda x: x[2])
    for elem in statistical_measures_occupations:
        print(elem)
    statistical_measures_adjectives.sort(key=lambda x: x[3])
    for elem in statistical_measures_occupations:
        print(elem)




def get_results_verb_sentences():
    verb_sentences = load_nested_list_to_list()
    # get all occupations
    unique_occupations = get_unique_occupations_from_verb_sentences(verb_sentences)

    # get all verbs
    unique_verbs = get_unique_verbs(verb_sentences)

    occupation_translations = evaluate_translation_gender_verb_sentences(unique_occupations, verb_sentences,
                                                                         mode="occupations_verb")
    verb_translations = evaluate_translation_gender_verb_sentences(unique_verbs, verb_sentences, mode="verbs")

    occupation_translations = sort_by_female_male_ratio(occupation_translations)

    verb_translations = sort_by_female_male_ratio(verb_translations)

    occupation_translations.insert(0, ["occupation", "n_of_female_translations", "n_of_male_translations",
                                       "n_of_neutral_translations", "n_of_wrong_translations", "female_male_ratio"])
    verb_translations.insert(0, ["verb", "n_of_female_translations", "n_of_male_translations",
                                 "n_of_neutral_translations", "n_of_wrong_translations", "female_male_ratio"])

    print("Write sorted occupation_translations list to file:")
    write_nested_list_to_file(occupation_translations)

    print("Write sorted verb_translations list to file:")
    write_nested_list_to_file(verb_translations)


def sort_by_female_male_ratio(translations):
    for elem in translations:
        try:
            female_male_ratio = elem[1] / elem[2]
        except ZeroDivisionError:
            female_male_ratio = 99
        elem.append(female_male_ratio)
    translations.sort(key=lambda x: x[5])
    for elem in translations:
        print(str(elem) + "\n")
    return translations


def evaluate_translation_gender_verb_sentences(unique_keys, verb_sentences, mode: str = "occupations_verb"):
    if mode == "occupations_verb":
        index_key = 3
        index_result = 5
    elif mode == "verbs":
        index_key = 2
        index_result = 5
    translations_gender: list = []
    for key in unique_keys:
        female_trans = 0
        male_trans = 0
        neutral_trans = 0
        wrong_trans = 0
        for sentence in verb_sentences:
            if key == sentence[index_key]:
                if sentence[index_result] == "female":
                    female_trans += 1
                elif sentence[index_result] == "male":
                    male_trans += 1
                elif sentence[index_result] == "neutral":
                    neutral_trans += 1
                elif sentence[index_result] == "wrong":
                    wrong_trans += 1
        translations_gender.append([key, female_trans, male_trans, neutral_trans, wrong_trans])
        output = "{0}: female={1}, male={2}, neutral={3}, wrong={4}"
        print(output.format(key.upper(), female_trans, male_trans, neutral_trans, wrong_trans))
    return translations_gender


def evaluate_translation_gender_winobias_sentences(unique_keys, winobias_sentences, mode: str = "occupations_winobias"):
    if mode == "occupations_winobias":
        index_result = 9
    elif mode == "adjectives":
        index_result = 9
    translations_gender: list = []
    for key in unique_keys:
        true_female = 0
        false_female = 0
        true_male = 0
        false_male = 0
        neutral_trans = 0
        wrong_trans = 0
        for sentence in winobias_sentences:
            if mode == "occupations_winobias":
                key_sentence = sentence[3].split(" ")[1]
                if key_sentence == "construction":
                    key_sentence = "construction worker"
            elif mode == "adjectives":
                key_sentence = sentence[5]
            if key == key_sentence:
                if sentence[index_result] == "neutral":
                    neutral_trans += 1
                elif sentence[index_result] == "wrong":
                    wrong_trans += 1
                elif sentence[index_result] == "female":
                    if sentence[0] == "female":
                        true_female += 1
                    elif sentence[0] == "male":
                        false_female += 1
                elif sentence[0] == "male":
                    if sentence[0] == "male":
                        true_male += 1
                    elif sentence[0] == "female":
                        false_male += 1
        translations_gender.append([key, true_female, false_female, true_male, false_male, neutral_trans, wrong_trans])
        output = "{0}: true_female={1}, false_female={2}, true_male={3}, false_male={4}, neutral={5}, wrong={6}"
        print(output.format(key.upper(), true_female, false_female, true_male, false_male, neutral_trans, wrong_trans))
    return translations_gender


def get_unique_verbs(verb_sentences):
    unique_verbs: dict = {}
    for sentence in verb_sentences:
        verb = sentence[2]
        verb_gender = sentence[0][2]
        if verb not in unique_verbs:
            unique_verbs[verb] = verb_gender
    return unique_verbs


def get_unique_adjectives(winobias_sentences):
    unique_adjectives: dict = {}
    for sentence in winobias_sentences:
        adjective = sentence[5]
        adjective_gender = sentence[6]
        if adjective not in unique_adjectives:
            unique_adjectives[adjective] = adjective_gender
    return unique_adjectives


def get_unique_occupations_from_verb_sentences(verb_sentences):
    unique_occupations: dict = {}
    for sentence in verb_sentences:
        occupation = sentence[3]
        occupation_gender = sentence[0][7]
        if occupation not in unique_occupations:
            unique_occupations[occupation] = occupation_gender
    return unique_occupations


def get_unique_occupations_from_winobias_sentences(winobias_sentences):
    unique_occupations: dict = {}
    for sentence in winobias_sentences:
        occupation = sentence[3].split(" ")[1]
        if occupation == "construction":
            occupation = "construction worker"
        occupation_gender = sentence[4]
        if occupation not in unique_occupations:
            unique_occupations[occupation] = occupation_gender
    return unique_occupations
