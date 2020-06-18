def add_adj_to_sentences(path_sentences, adj_list):
    # TODO: add try except block to read function
    '''
    try:
    with open('/etc/hosts') as f:
        print(f.readlines())
        # Do something with the file
    except FileNotFoundError:
        print("File not accessible")
    '''
    with open(path_sentences, "r", encoding="utf-8") as f:
        adj_sentences: list = []
        n_of_letters: int = 0
        for line in f:
            line = line.strip("\n")
            values = line.split("\t")
            occupation = values[3].replace("The ", "").replace("the ", "")
            sentence = values[2]
            for adj in adj_list:
                replacement = adj + " " + occupation
                sentence_plus_adj = sentence.replace(occupation, replacement)
                n_of_letters += len(sentence_plus_adj)
                adj_sentences.append(sentence_plus_adj)
    with open("/home/jonas/Documents/GitRepos/Words/sentences_WinoBias_with_ADJECTIVES_PRESENTATION.txt", "w") as f:
        for elem in adj_sentences:
            f.write(elem)
            f.write("\n")
    print("Zeichen:", n_of_letters)