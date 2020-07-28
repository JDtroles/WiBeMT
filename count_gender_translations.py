from reader_saver import load_nested_list_to_list, write_nested_list_to_file

from math import sqrt


def get_statistical_measures(translations):
    # {0}: true_female={1}, false_female={2}, true_male={3}, false_male={4}, neutral={5}, wrong={6}
    statistical_measures = [
        ["WORD", "ground_truth_female", "ground_truth_male","n_of_true_female", "n_of_false_female", "n_of_true_male",
         "n_of_false_male", "n_of_female", "n_of_male", "n_of_neutral", "n_of_wrong", "total", "wrong_ratio",
         "neutral_ratio", "true_female_rate", "true_male_rate", "female_predictive_value", "male_predictive_value",
         "false_female_rate", "false_male_rate", "female_male_classifications_rate", "total_accuracy", "accuracy",
         "balanced_accuracy", "f_one_score", "mathews_correlation_coefficient"]]
    for elem in translations:
        try:
            ground_truth_female = elem[7]
            ground_truth_male = elem[8]
            n_of_true_female = elem[1]
            n_of_false_female = elem[2]
            n_of_true_male = elem[3]
            n_of_false_male = elem[4]
            n_of_female = n_of_true_female + n_of_false_male
            n_of_male = n_of_true_male + n_of_false_female
            n_of_neutral = elem[5]
            n_of_wrong = elem[6]
            total = sum(elem[1:6])
            wrong_ratio = n_of_wrong / total
            neutral_ratio = n_of_neutral / total
            # TrueFemaleRate = TFemale / (TFemale + FMale)
            true_female_rate = n_of_true_female / n_of_female
            # TrueMaleRate = TMale / (TMale + FFemale)
            true_male_rate = n_of_true_male / n_of_male
            # FemalePredictiveValue = TFemale / (TFemale + FFemale)
            female_predictive_value = n_of_true_female / (n_of_true_female + n_of_false_female)
            # MalePredictiveValue = TMale / (TMale + FMale)
            male_predictive_value = n_of_true_male / (n_of_true_male + n_of_false_male)
            # FalseFemaleRate = FFemale / (FFemale + TMale)
            false_female_rate = n_of_false_female / n_of_male
            # FalseMaleRate = FMale / (FMale + TFemale)
            false_male_rate = n_of_false_male / n_of_female

            # Rate of Male/Female classifications (TFemale + FFemale + TMale + FMale) / ALL
            female_male_classifications_rate = sum(elem[1:4]) / sum(elem[1:6])

            # Total_Accuracy with true female/male divided by all cases
            total_accuracy = (n_of_true_female + n_of_true_male) / total
            # Accuracy of Female / Male classifications
            accuracy = (n_of_true_female + n_of_true_male) / (n_of_female + n_of_male)
            # Balanced Accuracy: (TFR + TMR) / 2
            balanced_accuracy = (true_female_rate + true_male_rate) / 2
            # F1 score
            f_one_score = (2 * n_of_true_female) / ((2 * n_of_true_female) + n_of_false_female + n_of_false_male)
            # Mathews Correlation Coefficient (MCC)
            mathews_correlation_coefficient = ((n_of_true_female * n_of_true_male) - (
                    n_of_false_female * n_of_false_male)) / (sqrt(
                (n_of_true_female + n_of_false_female) * (n_of_true_female + n_of_false_male) *
                (n_of_true_male + n_of_false_female) * (n_of_true_male + n_of_false_male)))

            statistical_measures.append(
                [elem[0], ground_truth_female, ground_truth_male, n_of_true_female, n_of_false_female, n_of_true_male, n_of_false_male, n_of_female, n_of_male,
                 n_of_neutral, n_of_wrong, total, wrong_ratio, neutral_ratio, true_female_rate, true_male_rate,
                 female_predictive_value, male_predictive_value, false_female_rate, false_male_rate,
                 female_male_classifications_rate, total_accuracy, accuracy, balanced_accuracy, f_one_score,
                 mathews_correlation_coefficient])
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

    # statistical_measures_occupations.sort(key=lambda x: x[1])
    statistical_measures_occupations.sort(key=lambda x: x[0])
    for elem in statistical_measures_occupations:
        print(elem)

    # statistical_measures_adjectives.sort(key=lambda x: x[1])
    statistical_measures_adjectives.sort(key=lambda x: x[0])
    for elem in statistical_measures_adjectives:
        print(elem)

    print("Write occupations with statisticmeasures to file")
    write_nested_list_to_file(statistical_measures_occupations)

    print("Write adjectives with statisticmeasures to file")
    write_nested_list_to_file(statistical_measures_adjectives)


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
        ground_truth_female = 0
        ground_truth_male = 0
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
                ground_truth = sentence[0]
                result = sentence[index_result]
                if ground_truth == "female":
                    ground_truth_female += 1
                elif ground_truth == "male":
                    ground_truth_male += 1
                if result == "neutral":
                    neutral_trans += 1
                elif result == "wrong":
                    wrong_trans += 1
                elif result == "female":
                    if ground_truth == "female":
                        true_female += 1
                    elif ground_truth == "male":
                        false_female += 1
                elif result == "male":
                    if ground_truth == "male":
                        true_male += 1
                    elif ground_truth == "female":
                        false_male += 1
        translations_gender.append([key, true_female, false_female, true_male, false_male, neutral_trans, wrong_trans,
                                    ground_truth_female, ground_truth_male])
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
