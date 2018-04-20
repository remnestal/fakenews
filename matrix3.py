from collections import defaultdict

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
        """ Return the member with the passed index """
        return self.__matrix[key]

    def __setitem__(self, key, value):
        """ Set the value of a certain dictionary member """
        self.__matrix[key] = value

class frequency(_3d_matrix):
    """ Frequency matrix for expressing frequency of pairwise word sequences """

    def __init__(self):
        """ Initialize an empty frequency matrix """
        super(frequency, self).__init__(int)
