from reader_saver import load_nested_list_to_list, write_nested_list_to_file

from math import sqrt


def get_statistical_measures_winobias(translations):
    # {0}: true_female={1}, false_female={2}, true_male={3}, false_male={4}, neutral={5}, wrong={6}
    statistical_measures = [
        ["WORD", "ground_truth_female", "ground_truth_male", "n_of_true_female", "n_of_false_female", "n_of_true_male",
         "n_of_false_male", "n_of_female", "n_of_male", "n_of_classifications", "n_of_neutral", "n_of_wrong", "total",
         "classification_ratio", "neutral_ratio", "wrong_ratio", "true_female_rate", "true_male_rate",
         "female_predictive_value", "male_predictive_value", "false_female_rate", "false_male_rate",
         "total_accuracy", "accuracy", "balanced_accuracy", "f_one_score",
         "mathews_correlation_coefficient"]
    ]
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
            n_of_classifications = sum(elem[1:5])
            n_of_neutral = elem[5]
            n_of_wrong = elem[6]
            total = sum(elem[1:7])
            classification_ratio = round(n_of_classifications / total, 4)
            wrong_ratio = round(n_of_wrong / total, 4)
            neutral_ratio = round(n_of_neutral / total, 4)
            # Total_Accuracy with true female/male divided by all cases
            total_accuracy = round((n_of_true_female + n_of_true_male) / total, 4)

            if n_of_female > 0:
                # FalseMaleRate = FMale / (FMale + TFemale)
                false_male_rate = round(n_of_false_male / n_of_female, 4)
                # TrueFemaleRate = TFemale / (TFemale + FMale)
                true_female_rate = round(n_of_true_female / n_of_female, 4)
            else:
                false_male_rate = -99
                true_female_rate = -99

            if n_of_male > 0:
                # TrueMaleRate = TMale / (TMale + FFemale)
                true_male_rate = round(n_of_true_male / n_of_male, 4)
                # FalseFemaleRate = FFemale / (FFemale + TMale)
                false_female_rate = round(n_of_false_female / n_of_male, 4)
            else:
                true_male_rate = -99
                false_female_rate = -99

            if n_of_true_female + n_of_false_female > 0:
                # FemalePredictiveValue = TFemale / (TFemale + FFemale)
                female_predictive_value = round(n_of_true_female / (n_of_true_female + n_of_false_female), 4)
            else:
                female_predictive_value = -99

            if n_of_true_male + n_of_false_male > 0:
                # MalePredictiveValue = TMale / (TMale + FMale)
                male_predictive_value = round(n_of_true_male / (n_of_true_male + n_of_false_male), 4)
            else:
                male_predictive_value = -99

            if n_of_classifications > 0:
                # Accuracy of Female / Male classifications
                accuracy = round((n_of_true_female + n_of_true_male) / n_of_classifications, 4)
            else:
                accuracy = -99

            if n_of_female > 0 and n_of_male > 0:
                # Balanced Accuracy: (TFR + TMR) / 2
                balanced_accuracy = round(((n_of_true_female / n_of_female) + (n_of_true_male / n_of_male)) / 2, 4)
            else:
                balanced_accuracy = -99

            if n_of_true_female > 0 or n_of_false_female > 0 or n_of_false_male > 0:
                # F1 score
                f_one_score = round((2 * n_of_true_female) /
                                    ((2 * n_of_true_female) + n_of_false_female + n_of_false_male), 4)
            else:
                f_one_score = -99

            # Mathews Correlation Coefficient (MCC)
            if (n_of_true_female + n_of_false_female) > 0 and n_of_true_male + n_of_false_male > 0 and (
                    n_of_true_female + n_of_false_male) > 0 and (n_of_true_male + n_of_false_female) > 0:
                mathews_correlation_coefficient = round(((n_of_true_female * n_of_true_male) - (
                        n_of_false_female * n_of_false_male)) / (sqrt(
                    (n_of_true_female + n_of_false_female) * (n_of_true_female + n_of_false_male) *
                    (n_of_true_male + n_of_false_female) * (n_of_true_male + n_of_false_male))), 4)
            else:
                mathews_correlation_coefficient = -99

            statistical_measures.append(
                [elem[0], ground_truth_female, ground_truth_male, n_of_true_female, n_of_false_female, n_of_true_male,
                 n_of_false_male, n_of_female, n_of_male,
                 n_of_classifications, n_of_neutral, n_of_wrong, total, classification_ratio, neutral_ratio,
                 wrong_ratio, true_female_rate, true_male_rate,
                 female_predictive_value, male_predictive_value, false_female_rate, false_male_rate,
                 total_accuracy, accuracy, balanced_accuracy, f_one_score,
                 mathews_correlation_coefficient])
        except ZeroDivisionError:
            print(elem[0], "DIVISION BY ZERO AT SOME POINT")
    return statistical_measures


def get_results_winobias_sentences():
    print("CHOOSE WINOBIAS TRANSLATIONS:")
    winobias_sentences = load_nested_list_to_list()

    # get all occupations
    unique_occupations = get_unique_occupations_from_winobias_sentences(winobias_sentences)

    # get all verbs
    unique_adjectives = get_unique_adjectives(winobias_sentences)

    occupation_translations = evaluate_translation_gender_winobias_sentences(unique_occupations, winobias_sentences,
                                                                             mode="occupations_winobias")
    adjective_translations = evaluate_translation_gender_winobias_sentences(unique_adjectives, winobias_sentences,
                                                                            mode="adjectives")

    statistical_measures_occupations = get_statistical_measures_winobias(occupation_translations)
    statistical_measures_adjectives = get_statistical_measures_winobias(adjective_translations)

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
    print("CHOOSE VERB TRANSLATIONS:")
    verb_sentences = load_nested_list_to_list()
    # get all occupations
    unique_occupations = get_unique_occupations_from_verb_sentences(verb_sentences)

    # get all verbs
    unique_verbs = get_unique_verbs(verb_sentences)

    occupation_translations = evaluate_translation_gender_verb_sentences(unique_occupations, verb_sentences,
                                                                         mode="occupations_verb")
    verb_translations = evaluate_translation_gender_verb_sentences(unique_verbs, verb_sentences, mode="verbs")

    statistical_measures_occupations = get_statistical_measures_verbs(occupation_translations)
    statistical_measures_verbs = get_statistical_measures_verbs(verb_translations)

    # statistical_measures_occupations.sort(key=lambda x: x[1])
    statistical_measures_occupations.sort(key=lambda x: x[0])
    for elem in statistical_measures_occupations:
        print(elem)

    # statistical_measures_adjectives.sort(key=lambda x: x[1])
    statistical_measures_verbs.sort(key=lambda x: x[0])
    for elem in statistical_measures_verbs:
        print(elem)

    print("Write occupations with statisticmeasures to file")
    write_nested_list_to_file(statistical_measures_occupations)

    print("Write adjectives with statisticmeasures to file")
    write_nested_list_to_file(statistical_measures_verbs)


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


def get_statistical_measures_verbs(translations):
    statistical_measures = [
        ["WORD", "ground_truth_female", "ground_truth_male", "ground_truth_neutral", "result_female", "result_male",
         "result_neutral", "result_wrong", "total_result", "total_control", "n_of_classifications", "female_ratio",
         "female_total_ratio", "male_ratio", "male_total_ratio", "neutral_total_ratio", "wrong_total_ratio"]
    ]

    # input format:
    # [0 key, 1 result_female, 2 result_male, 3 result_neutral, 4 result_wrong, 5 ground_truth_female,
    #   6 ground_truth_male, 7 ground_truth_neutral]

    for elem in translations:
        try:
            ground_truth_female = elem[5]
            ground_truth_male = elem[6]
            ground_truth_neutral = elem[7]
            result_female = elem[1]
            result_male = elem[2]
            result_neutral = elem[3]
            result_wrong = elem[4]
            total_result = sum(elem[1:5])
            total_control = sum(elem[5:8])
            n_of_classifications = sum(elem[1:3])

            if total_result > 0:
                female_total_ratio = round(result_female / total_result, 4)
                male_total_ratio = round(result_male / total_result, 4)
                neutral_total_ratio = round(result_neutral / total_result, 4)
                wrong_total_ratio = round(result_wrong / total_result, 4)
            else:
                female_total_ratio = -99
                male_total_ratio = -99
                neutral_total_ratio = -99
                wrong_total_ratio = -99

            if n_of_classifications > 0:
                female_ratio = round(result_female / n_of_classifications, 4)
                male_ratio = round(result_male / n_of_classifications, 4)
            else:
                female_ratio = -99
                male_ratio = -99
        except ZeroDivisionError:
            print(elem[0], "DIVISION BY ZERO AT SOME POINT")

        statistical_measures.append(
            [elem[0], ground_truth_female, ground_truth_male, ground_truth_neutral, result_female, result_male,
             result_neutral, result_wrong, total_result, total_control, n_of_classifications, female_ratio,
             female_total_ratio, male_ratio, male_total_ratio, neutral_total_ratio, wrong_total_ratio])

    return statistical_measures


def evaluate_translation_gender_verb_sentences(unique_keys, verb_sentences, mode: str = "occupations_verb"):
    if mode == "occupations_verb":
        index_key = 3
        index_result = 5
    elif mode == "verbs":
        index_key = 2
        index_result = 5
    translations_gender: list = []
    for key in unique_keys:
        ground_truth_female = 0
        ground_truth_male = 0
        ground_truth_neutral = 0
        result_female = 0
        result_male = 0
        result_neutral = 0
        result_wrong = 0
        for sentence in verb_sentences:
            if mode == "occupations_verb":
                key_sentence = sentence[index_key]
            elif mode == "verbs":
                key_sentence = sentence[index_key]
            if key == key_sentence:
                ground_truth = sentence[0][1]
                result = sentence[index_result]
                if ground_truth == "F":
                    ground_truth_female += 1
                elif ground_truth == "M":
                    ground_truth_male += 1
                elif ground_truth == "N":
                    ground_truth_neutral += 1
                if result == "neutral":
                    result_neutral += 1
                elif result == "wrong":
                    result_wrong += 1
                elif result == "female":
                    result_female += 1
                elif result == "male":
                    result_male += 1

        translations_gender.append(
            [key, result_female, result_male, result_neutral, result_wrong, ground_truth_female, ground_truth_male,
             ground_truth_neutral])
        output = "{0}: result_female={1}, result_male={2}, result_neutral={3}, result_wrong={4}, " \
                 "ground_truth_female={5}, ground_truth_male={6}, ground_truth_neutral={7}"
        print(output.format(key.upper(), result_female, result_male, result_neutral, result_wrong, ground_truth_female,
                            ground_truth_male, ground_truth_neutral))
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


def get_wb_overall_stats(winobias_sentences, source: str):
    index_result: int = 9

    ground_truth_female = 0
    ground_truth_male = 0
    true_female = 0
    false_female = 0
    true_male = 0
    false_male = 0
    neutral_trans = 0
    wrong_trans = 0

    translations_gender: list = []

    for sentence in winobias_sentences:
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
    translations_gender.append([source, true_female, false_female, true_male, false_male, neutral_trans, wrong_trans,
                                ground_truth_female, ground_truth_male])
    output = "{0}: true_female={1}, false_female={2}, true_male={3}, false_male={4}, neutral={5}, wrong={6}"
    print(output.format(source.upper(), true_female, false_female, true_male, false_male, neutral_trans, wrong_trans))
    return translations_gender


def get_unique_verbs(verb_sentences):
    unique_verbs: dict = {}
    for sentence in verb_sentences:
        verb = sentence[2]
        verb_gender = sentence[0][1]
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
