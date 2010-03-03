from random import random
from collections import defaultdict

class Markov:

    def __init__(self, order=3):
        self.order = order
        record = lambda: {'count': 0.0, 'next': defaultdict(record)}
        self.chains = defaultdict(record)
        self.probabilities = []

    def compute_probabilities(self, chain=None):
        chain = chain or self.chains
        probabilities = []
        if len(chain):
            total = sum([i['count'] for i in chain.values()])
            norm = 1/total if total > 0 else 1
            for (token, subchain) in chain.items():
                probabilities.append({ 'chance': subchain['count'] * norm,
                                       'word':   token,
                                       'next':   self.compute_probabilities(chain['next']) if 'next' in chain else {}
                                       })
            probabilities.sort(lambda a,b: cmp(a['chance'], b['chance']))
        return probabilities
    
    def scan(self, tokens):
        for i in xrange(0, len(tokens) - self.order +1 ):
            window = tokens[i:i+self.order]
            current = self.chains
            for token in window:
                current[token]['count'] += 1
                current = current[token]['next']

    def tokenize(self, string):
        return string.split()

    def generate(self, probabilities, length):
        results = []
        for i in xrange(length):
            rand = random()
            for token in probabilities:
                # TODO: finish when not half-asleep :-)
                pass


if __name__ == "__main__":
    markov = Markov()
