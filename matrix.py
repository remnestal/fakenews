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

class transition(object):
    """ Word sequence transition matrix

        Matrix containing the transition probability of each word. For each word
        there is a list of the tuple (next-word, probability) and the words are
        sorted in ascending order. `None` is used as an end-of-line delimiter.
    """
    def __init__(self, frequencies):
        self.transition = defaultdict(list)
        for (word, nextlist) in frequencies.frequency.items():
            frequency_sum = sum((freq for _, freq in nextlist.items()))

            for (next_word, frequency) in nextlist.items():
                # matrix entries consist of a word and the probability of transition
                probability = float(frequency) / float(total_freq)
                transition[word].append((next_word, probability))

            # sort the next-word list by probability for simpler use later
            transition[word].sort(key=lambda entry: entry[1])
