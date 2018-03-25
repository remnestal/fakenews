from collections import defaultdict
from os.path import isfile, join
from os import listdir

def main():
    print(_frequency_matrix())

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
