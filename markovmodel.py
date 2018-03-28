from collections import defaultdict
from os.path import isfile, join
from os import listdir
import random

class Markovchain(object):
    """ Markov-chain object for fabricating text """

    def main(self):
        """ Generate a fake text string using a naïve 1st order markov chain """
        transition = self._transition_matrix()

        # pick the first word at random
        body = list()
        body.append(random.choice(list(transition.keys())))

        # add words until the end-of-line nominator is found, i.e. `None`
        while body[-1] != None:
            body.append(self._pick_successor(body[-1], transition))

        print(' '.join(body[:-1]))

    def _pick_successor(self, word, transition):
        """ Pick a successor based on the probability of transition """
        transition_probability = random.random()
        total_probability = 0.0

        # loop until the probability exceeds the likelihood of transition
        for successor, probability in transition[word]:
            total_probability += probability
            if total_probability >= transition_probability:
                return successor

        # perhaps a little flaky, but should always have returned by now
        raise RuntimeError('_pick_successor failed')

    def _transition_matrix(self):
        """ Return a unidirectional transition matrix of pairwise word order
            * frequency is relative to all successors of a given word
            * matrix elements are represented by tuples of (word, probability)
        """
        # the transition matrix is implemented as a dictionary of tuple-entry lists
        transition = defaultdict(list)
        for word, successors in self._frequency_matrix().items():
            total_freq = sum(map(lambda d: d[1], successors.items()))

            for successor, frequency in successors.items():
                # matrix entries consist of a word and the probability of transition
                probability = float(frequency) / float(total_freq)
                transition[word].append((successor, probability))

            # sort the successor list by probability for simpler use later
            transition[word].sort(key=lambda entry: entry[1])
        return transition

    def _frequency_matrix(self):
        """ Return a unidirectional frequency matrix of pairwise word order
            * uses all datasets found in data/
            * the `None` word denotes end-of-line
        """
        # the frequency matrix is implemented as a dictionary of dictionaries
        frequency = defaultdict(lambda: defaultdict(int))
        for f in self._data_files():
            with open(f) as fstream:
                for line in fstream:
                    words = line.split()
                    words_pairwise = zip(words, words[1:]+[None])
                    for position, (word1, word2) in enumerate(words_pairwise):
                        frequency[word1][word2] += 1
        return frequency

    def _data_files(self, datapath='data/', exclude=['.gitignore']):
        """ Return paths of eligible files in the data subdirectory """
        files = list()
        for f in listdir(datapath):
            fpath = join(datapath, f)
            if isfile(fpath) and f not in exclude:
                files.append(fpath)
        return files
