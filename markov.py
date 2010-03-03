from collections import defaultdict

class Markov:

    def __init__(self, order=3):
        self.order = order
        thingy = lambda: {'count': 0, 'next': defaultdict(thingy)}
        self.chains = defaultdict(thingy)

    def scan(self, tokens):
        for i in xrange(0, len(tokens) - self.order +1 ):
            window = tokens[i:i+self.order]
            current = self.chains
            for token in window:
                current[token]['count'] += 1
                current = current[token]['next']

    def tokenize(self, string):
        return string.split()

    
if __name__ == "__main__":
    markov = Markov()
