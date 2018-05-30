from os.path import isfile, join
from os import listdir
import random
import matrix3
import pickle

_CACHE = '.cache.pkl'


class MarkovChain(object):
    """ Markov-chain object for fabricating text """

    def __init__(self, refresh_cache=False, order=2):
        """ Create the first order markov-chain """
        self.order = order
        assert self.order >= 2, 'order 2 or higher is required'

        cache_enabled = not refresh_cache and isfile(_CACHE)
        if cache_enabled:
            # utilize cached transition matrix
            self.transition = self.__read_cache()
        else:
            # generate the transition matrix anew
            self.__initalize_model()
            self.__write_cache()

    def __initalize_model(self):
        """ Create a probibalistic transition model from available data """
        # set up the frequency matrix
        frequency = matrix3.Frequency(self.order)
        for f in self._data_files():
            with open(f) as fstream:
                for line in fstream:
                    # naïve input filtering
                    seq = line.replace('"', '') \
                              .replace('”', '') \
                              .strip() \
                              .split()
                    frequency.add_sequence(seq)

        # set up the transition matrix
        self.transition = matrix3.Transition(frequency_matrix=frequency)

    def generate(self):
        """ Return a fabricated string made with a 1st order markov chain """
        body = list(tuple(self.__first_word()))

        # look for new words until the EOL delimiter None is found
        while body[-1] is not None:
            past_states = tuple(body[-self.order+1:])
            next_state = self.__next(len(body)-(len(past_states)), past_states)
            body.append(next_state)

        # return all but root and eol delimiters
        return ' '.join(body[:-1])

    def __first_word(self):
        """ Pick the first word based on the initial state distribution """
        initial_probability = random.random()
        accumulated_prob = 0.0

        for state, prob in self.transition._initial_state_distrib.items():
            accumulated_prob += prob
            if accumulated_prob >= initial_probability:
                return state

        # perhaps a little flaky, but should always have returned by now
        raise RuntimeError('__first_word failed')

    def __next(self, position, word):
        """ Pick a random successor based on the probability of transition """
        transition_probability = random.random()
        total_probability = 0.0
        # loop until the probability exceeds the likelihood of transition
        for successor, probability in self.transition[position][word].items():
            total_probability += probability
            if total_probability >= transition_probability:
                return successor

        # perhaps a little flaky, but should always have returned by now
        raise RuntimeError('__next failed')

    def __write_cache(self, cache_path=_CACHE):
        """ Write transition matrix to the cache """
        with open(cache_path, "wb") as cache:
            pickle.dump(self.transition, cache, pickle.HIGHEST_PROTOCOL)

    def __read_cache(self, cache_path=_CACHE):
        """ Read transition matrix from the cache """
        with open(cache_path, "rb") as cache:
            loaded_cache = pickle.load(cache)
            # return if the cache actually contains a transition matrix
            if isinstance(loaded_cache, matrix3.transition):
                return loaded_cache
            else:
                raise TypeError('Cache was corrupted.')

    def _data_files(self, datapath='data/', exclude=['.gitignore']):
        """ Return paths of eligible files in the data subdirectory """
        files = list()
        for f in listdir(datapath):
            fpath = join(datapath, f)
            if isfile(fpath) and f not in exclude:
                files.append(fpath)
        return files
