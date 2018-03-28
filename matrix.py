
class frequency(object):
    """ Unidirectional matrix of ascending pairwise word frequency
        * uses all datasets found in data/
        * the `None` word denotes end-of-line
    """

    def __init__(self):
        """ Initialize an empty frequency matrix """
        self.frequency = defaultdict(lambda: defaultdict(int))
