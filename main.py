from evaluate_results import evaluate_gender_of_translation, manual_evaluation
from get_ressources import get_20_handpicked_adjectives, get_20_handpicked_verbs
from pipelines import pipeline_0, pipeline_1, pipeline_2, pipeline_3
from translation_api_caller import translate_sentences_via_api


if __name__ == "__main__":
    word_embeddings_paths = ["/home/Jonas/Desktop/TidyWordVectors/fastText/fastText_1M_300d_wiki_UMBC_statmt.pickle",
                             "/home/Jonas/Desktop/TidyWordVectors/fastText/fastText_2M_300d_commonCrawl.pickle",
                             "/home/Jonas/Desktop/TidyWordVectors/GloVe/glove_400k_300d_wiki_gigaword5.pickle",
                             "/home/Jonas/Desktop/TidyWordVectors/GloVe/glove_2M_300d_commonCrawl.pickle"]
    print("main")
    # pipeline_0()
    # pipeline_1("fastText_1M_300d_wiki_UMBC_statmt", "fastText_2M_300d_commonCrawl", get_20_handpicked_adjectives())
    # pipeline_1(["fastText_small", "fastText_large", "GloVe_small", "GloVe_large"], word_embeddings_paths)
    # pipeline_2()
    # pipeline_3()
    # translate_sentences_via_api(api="Google", dataset_type="WinoBias_sentences")
    # TODO: fix verb_sentences classification
    # ['VM20OccN16', 'The investigator appoints a date for the meeting.', 'appoint', 'investigator', 'Der Untersuchungsbeauftragte setzt einen Termin für das Treffen fest.']
    # ['VM13OccF12', 'The attendant regards a colleague with favour.', 'regard', 'attendant', 'Der Anwesende betrachtet einen Kollegen mit Wohlwollen.']
    evaluate_gender_of_translation(data_structure="verb_sentences")
    # manual_evaluation()

# TODO: create latex lists/tables for appendix
