from collections import defaultdict
from os.path import isfile, join
from os import listdir
import random
import matrix
import pickle

CACHE = '.cache.pkl'

class Markovchain(object):
    """ Markov-chain object for fabricating text """

    def __init__(self, refresh_cache=False):
        """ Create the first order markov-chain """
        
        cache_enabled = not refresh_cache and isfile(CACHE)
        if cache_enabled:
            # utilize cached transition matrix
            self.transition = matrix.transition(frequency_matrix=None,
                                                cache=self.__read_cache())
        else:
            # generate the transition matrix anew
            self.__initalize_model();
            self.__write_cache()

    def __initalize_model(self):
        # set up the frequency matrix
        frequency = matrix.frequency()
        for f in self._data_files():
            with open(f) as fstream:
                for line in fstream:
                    frequency.add_text(line)

        # set up the transition matrix
        self.transition = matrix.transition(frequency_matrix=frequency)

    def generate(self):
        """ Return a fabricated string made with a 1st order markov chain """
        body = [matrix.delimiter.ROOT]
        while body[-1] != matrix.delimiter.EOL:
            body.append(self.__next(len(body)-1, body[-1]))

        # return all but root and eol delimiters
        return ' '.join(body[1:-1])

    def __next(self, position, word):
        """ Pick a random successor based on the probability of transition """
        transition_probability = random.random()
        total_probability = 0.0

        # loop until the probability exceeds the likelihood of transition
        for successor, probability in self.transition.matrix[position][word]:
            total_probability += probability
            if total_probability >= transition_probability:
                return successor

        # perhaps a little flaky, but should always have returned by now
        raise RuntimeError('__next failed')

    def __write_cache(self, cache_path=CACHE):
        """ Write to the cache """
        with open(cache_path, "wb") as cache:
            pickle.dump(self.transition.matrix, cache, pickle.HIGHEST_PROTOCOL)

    def __read_cache(self, cache_path=CACHE):
        """ Read from the cache """
        with open(cache_path, "rb") as cache:
            return pickle.load(cache)

    def _data_files(self, datapath='data/', exclude=['.gitignore']):
        """ Return paths of eligible files in the data subdirectory """
        files = list()
        for f in listdir(datapath):
            fpath = join(datapath, f)
            if isfile(fpath) and f not in exclude:
                files.append(fpath)
        return files
