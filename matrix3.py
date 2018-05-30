from collections import defaultdict, Iterable


class _3d_matrix(object):
    """ Basic implementation for a 3-dimensional lazily evaluated matrix

        The matrix has no fixed size and is dynamically allocated using
        collections.defaultdict to achieve JIT construction of missing
        elements. This means that, for example, element A[1][2][3] can be
        assigned a value even if neither element A[1][2] or element A[1] has
        been defined before, since both will be instantiated on the fly.
    """

    def __init__(self, matrix_type):
        """ Initialize an empty matrix """
        # assert that the passed type is actually derived from the type-class
        if isinstance(matrix_type, type):
            # This is necessary evil to achieve lazy evaluation
            self.__matrix = defaultdict(
                lambda: defaultdict(
                    lambda: defaultdict(matrix_type)))
            self._initial_state_distrib = defaultdict(matrix_type)
        else:
            raise ValueError('`matrix_type` must be an instance of `type`')

    def __getitem__(self, key):
        """ Return the row that corresponds to the passed index """
        return self.__matrix[key]

    def __setitem__(self, key, value):
        """ Set the row content corresponding to the passed row index """
        self.__matrix[key] = value

    def items(self):
        """ Return a list of the matrix's {position, words} tuple pairs """
        return iter(self.__matrix.items())

    def _make_serializable(self):
        """ Convert matrix to regular dictionaries that are serializable """
        def to_dict(obj):
            if isinstance(obj, defaultdict):
                return {k: to_dict(v) for k, v in obj.items()}
            else:
                return obj
        # overwrite existing matrix structure
        self.__matrix = to_dict(self.__matrix)
        self._initial_state_distrib = to_dict(self._initial_state_distrib)


class Frequency(_3d_matrix):
    """ Frequency matrix for expressing frequency of pairwise word sequences

        A[x]        all words at position x in the sequence
        A[x][y]     all words following word y, at position x+1
        A[x][y][z]  how many times the sequence {x, z} has occured at {x, x+1}
    """

    def __init__(self, order):
        """ Initialize an empty frequency matrix

            The `order` parameter determines the order of the markov chain; n=2
            means that words are associated in pairs of 2, n=3 means that words
            are grouped in sets of 3 etc.
        """
        super(Frequency, self).__init__(int)
        self.order = order

    def add_sequence(self, sequence):
        """ Register the passed sequence of words in the matrix """

        if not isinstance(sequence, Iterable):
            raise ValueError('The passed sequence must be iterable.')

        # add None as an EOL-delimiter
        sequence.append(None)

        # register the initial state
        initial_state = tuple(sequence[:self.order-1])
        self._initial_state_distrib[initial_state] += 1

        # register the occurance of each state and transition
        for position, ngram in enumerate(self.__ngram(sequence)):
            state, transit = ngram[:-1], ngram[-1]
            self[position][state][transit] += 1

    def __ngram(self, sequence):
        """ Return a list of ngrams from the passed sequence """
        # copy the sequence n-times with incrementing offset for each copy
        sequence_offset = [sequence[index:] for index in range(self.order)]
        # zip the n sequences together to form the ngrams
        ngram_seq = zip(*sequence_offset)
        return list(ngram_seq)


class Transition(_3d_matrix):
    """ Transition probability matrix for pairwise comparison in sequence

        Example:
            A[x][y][z]: probability for word z to follow word y, when word y
                        has position x in the sequence.
    """

    def __init__(self, frequency_matrix):
        """ Initialize a transition matrix from the passed frequency matrix """
        super(Transition, self).__init__(float)

        # build matrix and make it serializable
        self.__set_initial_distrib(frequency_matrix)
        self.__build_transition_matrix(frequency_matrix)
        self._make_serializable()

    def __set_initial_distrib(self, frequencies):
        """ Sets initial state transition distribution

            Converts the initial state distribution of the passed frequency
            matrix to an initial state transition probability distribution.
        """
        num_observations = sum(frequencies._initial_state_distrib.values())
        self._initial_state_distrib = dict()

        for state, freq in frequencies._initial_state_distrib.items():
            probability = float(freq)/float(num_observations)
            self._initial_state_distrib[state] = probability

    def __build_transition_matrix(self, frequencies):
        """ Generate the state transition probability matrix

            Convert the valeus stored in the passed frequency matrix into state
            transition probabilities for each word and position pair.
        """
        for position, words in frequencies.items():
            for word1, successors in words.items():
                # translate frequency to probability for each word pair
                total_occurances = sum(successors.values())
                for word2, occurances in successors.items():
                    probability = float(occurances)/float(total_occurances)
                    self[position][word1][word2] = probability
