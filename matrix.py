from collections import defaultdict

class frequency(object):
    """ Word sequence frequency matrix

        Word frequency is calculated pairwise in ascending order, i.e. word
        number n+1 is added to the successor-frequency vector of the nth word.
        The frequency is stored as the number of occurances of that exact word
        sequence. `None` is used as an end-of-line delimiter.
    """

    def __init__(self):
        """ Initialize an empty frequency matrix """
        self.frequency = defaultdict(lambda: defaultdict(int))

    def add_text(self, text):
        """ Add each pair of words in the passed text to the matrix """
        words = text.split()
        words_pairwise = zip(words, words[1:]+[None])
        for pair in enumerate(words_pairwise):
            self.add_pair(*pair)

    def add_pair(self, word, succesor):
        """ Add the passed pair of words to the matrix

            The second argument is added as the successor of the first word.
            Since the frequency is unidirectional, the first argument is not
            added as the successor of the second.
        """
        self.frequency[word][succesor] += 1
