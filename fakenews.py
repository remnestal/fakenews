from collections import defaultdict
from os.path import isfile, join
from os import listdir

def main():
    print(_transition_matrix())

def _transition_matrix():
    """ Return a unidirectional transition matrix of pairwise word order
        * frequency is relative to all successors of a given word
        * matrix elements are represented by tuples of (word, probability)
    """
    # the transition matrix is implemented as a dictionary of tuple-entry lists
    transition = defaultdict(list)
    for word, successors in _frequency_matrix().items():
        total_freq = sum(map(lambda d: d[1], successors.items()))

        for successor, frequency in successors.items():
            # matrix entries consist of a word and the probability of transition
            probability = float(frequency) / float(total_freq)
            transition[word].append((successor, probability))

        # sort the successor list by probability for simpler use later
        transition[word].sort(key=lambda entry: entry[1])
    return transition

def _frequency_matrix():
    """ Return a unidirectional frequency matrix of pairwise word order
        * uses all datasets found in data/
        * the `None` word denotes end-of-line
    """
    # the frequency matrix is implemented as a dictionary of dictionaries
    frequency = defaultdict(lambda: defaultdict(int))
    for f in _data_files():
        with open(f) as fstream:
            for line in fstream:
                words = line.split()
                for a, b in zip(words, words[1:]+[None]):
                    frequency[a][b] += 1
    return frequency

def _data_files(datapath='data/', exclude=['.gitignore']):
    """ Return paths of eligible files in the data subdirectory """
    files = list()
    for f in listdir(datapath):
        fpath = join(datapath, f)
        if isfile(fpath) and f not in exclude:
            files.append(fpath)
    return files

if __name__ == "__main__":
    main()
