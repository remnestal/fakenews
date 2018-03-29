from collections import defaultdict

class _defaultlist(object):
    """ List structure with default initializer

        Implementation is based on that of `collections.defaultdict`. If a non-
        existing list member is set, i.e. list[key] and key is larger than
        len(list); then the list initializes default members up unto that key.
    """

    def __init__(self, default):
        """ Initialize an empty list """
        self.default = default
        self.list = list()

    def __getitem__(self, key):
        """ Return the member with the passed index """
        diff = max((key - (len(self.list) - 1)), 0)
        if diff > 0: self.list += [self.default()] * diff
        return self.list[key]

    def __setitem__(self, key, value):
        """ Set the value of a certain list member """
        self.list[key] = value

class frequency(object):
    """ Word sequence frequency matrix

        Word frequency is calculated pairwise in ascending order, i.e. word
        number n+1 is added to the successor-frequency vector of the nth word.
        The frequency is stored as the number of occurances of that exact word
        sequence. `None` is used as an end-of-line delimiter.
    """

    def __init__(self):
        """ Initialize an empty frequency matrix """
        self.matrix = defaultdict(lambda: defaultdict(int))

    def add_text(self, text):
        """ Add each pair of words in the passed text to the matrix """
        words = text.split()
        words_pairwise = zip(words, words[1:]+[None])
        for pair in words_pairwise:
            self.add_pair(*pair)

    def add_pair(self, word, successor):
        """ Add the passed pair of words to the matrix

            The second argument is added as the successor of the first word.
            Since the frequency is unidirectional, the first argument is not
            added as the successor of the second.
        """
        self.matrix[word][successor] += 1

class transition(object):
    """ Word sequence transition matrix

        Matrix containing the transition probability of each word. For each word
        there is a list of the tuple (next-word, probability) and the words are
        sorted in ascending order. `None` is used as an end-of-line delimiter.
    """
    def __init__(self, frequencies):
        self.matrix = defaultdict(list)
        for (word, nextlist) in frequencies.matrix.items():
            frequency_sum = sum((freq for _, freq in nextlist.items()))
            for (next_word, frequency) in nextlist.items():
                # matrix entries consist of a word and the probability of transition
                probability = float(frequency) / float(frequency_sum)
                self.matrix[word].append((next_word, probability))

            # sort the next-word list by probability for simpler use later
            self.matrix[word].sort(key=lambda entry: entry[1])
