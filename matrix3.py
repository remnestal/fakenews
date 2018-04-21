from collections import defaultdict, Iterable
from textutils import delimiter

class _3d_matrix(object):
    """ Basic implementation for a 3-dimensional lazily evaluated matrix

        The matrix has no fixed size and is dynamically allocated using
        collections.defaultdict to achieve JIT construction of missing elements.
        This means that, for example, element A[1][2][3] can be assigned a value
        even if neither element A[1][2] or element A[1] has been defined before,
        since both will be instantiated on the fly.
    """

    def __init__(self, matrix_type):
        """ Initialize an empty matrix """
        # assert that the passed type is actually derived from the type-class
        if isinstance(matrix_type, type):
            # This is necessary evil to achieve lazy evaluation
            self.__matrix = defaultdict(lambda: defaultdict(lambda: defaultdict(matrix_type)))
        else:
             raise ValueError('`matrix_type` must be an instance of class `type`')

    def __getitem__(self, key):
        """ Return the row that corresponds to the passed index """
        return self.__matrix[key]

    def __setitem__(self, key, value):
        """ Set the row content corresponding to the passed row index """
        self.__matrix[key] = value

    def items(self):
        """ Return a list of the matrix's {position, words} tuple pairs """
        return iter(self.__matrix.items())

class frequency(_3d_matrix):
    """ Frequency matrix for expressing frequency of pairwise word sequences

        A[x]        all words at position x in the sequence
        A[x][y]     all words following word y, at position x+1
        A[x][y][z]  how many times the sequence {x, z} has occured at {x, x+1}
    """

    def __init__(self):
        """ Initialize an empty frequency matrix """
        super(frequency, self).__init__(int)

    def add_sequence(self, sequence):
        """ Register the passed sequence of words in the matrix """

        if not isinstance(sequence, Iterable):
            raise ValueError('The passed sequence must be iterable.')

        # add start/end- of text delimiters and group all tokens pairwise
        sequence.insert(0, delimiter.ROOT)
        sequence.append(delimiter.EOL)
        pairwise = zip(sequence[:-1], sequence[1:])

        # record that the sequence {word1, word2} occured at position
        for position, (word1, word2) in enumerate(pairwise):
            self[position][word1][word2] += 1

class transition(_3d_matrix):
    """ Transition probability matrix for pairwise comparison in sequence

        Example:
            A[x][y][z]: probability for word z to follow word y, when word y has
                        position x in the sequence.
    """

    def __init__(self):
        """ Initialize an empty transition matrix """
        super(transition, self).__init__(float)

    def convert(frequency_matrix):
        """ Returns a transition matrix based on the passed frequency matrix """
        matrix = transition()
        for position, words in frequency_matrix.items():
            # translate frequency to probability for each word pair
            for word1, successors in words.items():
                total_occurances = sum(successors.values())
                for word2, occurances in successors.items():
                    probability = float(occurances)/float(total_occurances)
                    matrix[position][word1][word2] = probability

        return matrix
