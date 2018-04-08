from collections import defaultdict
from os.path import isfile, join
from os import listdir
import random
import matrix

class Markovchain(object):
    """ Markov-chain object for fabricating text """

    def __init__(self):
        """ Create the first order markov-chain """

        # set up the frequency matrix
        frequency = matrix.frequency()
        for f in self._data_files():
            with open(f) as fstream:
                for line in fstream:
                    frequency.add_text(line)

        # set up the transition matrix
        self.transition = matrix.transition(frequency)

    def generate(self):
        """ Return a fabricated string made with a 1st order markov chain """

        body = list()
        body.append(self.__next(0, None)) # first word

        # add words until the end-of-line nominator is found, i.e. `None`
        while body[-1] != None:
            body.append(self.__next(len(body), body[-1]))

        return ' '.join(body[:-1])

    def __next(self, position, word):
        """ Pick a successor based on the probability of transition """
        transition_probability = random.random()
        total_probability = 0.0

        # loop until the probability exceeds the likelihood of transition
        for successor, probability in self.transition.matrix[position][word]:
            total_probability += probability
            if total_probability >= transition_probability:
                return successor

        # perhaps a little flaky, but should always have returned by now
        raise RuntimeError('__next failed')

    def _data_files(self, datapath='data/', exclude=['.gitignore']):
        """ Return paths of eligible files in the data subdirectory """
        files = list()
        for f in listdir(datapath):
            fpath = join(datapath, f)
            if isfile(fpath) and f not in exclude:
                files.append(fpath)
        return files
