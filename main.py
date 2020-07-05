from get_ressources import get_20_handpicked_adjectives, get_20_handpicked_verbs
from pipelines import pipeline_0, pipeline_1, pipeline_2, pipeline_3

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
    pipeline_3()

    # TODO: create new verb sentences (with adjectives)
    # TODO: create adjective sentences
    # TODO: create latex lists/tables for appendix
    # TODO: translate sentences
    # TODO: check adjectives list