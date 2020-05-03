import spacy
import en_core_web_lg
from tqdm import tqdm

class NLPWorker():
    def __init__(self):
        self.nlp = en_core_web_lg.load()

    def get_adj_verbs(self, word_emb: dict) -> [list, list]:
        adjectives = []
        verbs = []
        for key in word_emb:
            doc = self.nlp(key)
            for token in doc:
                if token.pos == 83:
                    adjectives.append(key)
                elif token.pos == 99:
                    verbs.append(key)
        return adjectives, verbs



def get_adj_verbs(word_emb: dict) -> [list, list]:
    adjectives = []
    verbs = []
    for key in word_emb:
        doc = nlp(key)
        for token in doc:
            if token.pos == 83:
                adjectives.append(key)
            elif token.pos == 99:
                verbs.append(key)
    return adjectives, verbs
