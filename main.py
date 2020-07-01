from get_ressources import get_20_handpicked_adjectives, get_20_handpicked_verbs
from pipelines import pipeline_0, pipeline_1, pipeline_2

if __name__ == "__main__":
    print("main")
    # pipeline_0()
    # pipeline_1("fastText_1M_300d_wiki_UMBC_statmt", "fastText_2M_300d_commonCrawl", get_20_handpicked_adjectives())
    # TODO: complete formatting of output file -> simplest solution = 1 tab -> no key, only value (column captions)
    pipeline_1(["fT_s", "fT_l", "GV_s", "GV_l"])
    # pipeline_2()
