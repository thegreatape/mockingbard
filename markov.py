from random import random
from collections import defaultdict

class Markov:

    def __init__(self, order=3):
        self.order = order
        record = lambda: {'count': 0.0, 'next': defaultdict(record)}
        self.chains = defaultdict(record)
        self.probabilities = []

    def compute_probabilities(self, limit, chain=None):
        chain = chain or self.chains
        probabilities = []
        if limit and len(chain):
            total = sum([i['count'] for i in chain.values()])
            norm = 1/total if total > 0 else 1
            for (token, subchain) in chain.items():
                probabilities.append({ 'chance': subchain['count'] * norm,
                                       'word':   token,
                                       'next':   self.compute_probabilities(limit-1, subchain['next']) if 'next' in subchain else []
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

    def generate_stream(self, probabilities, length):
        words = []
        current_table = probabilities
        for i in xrange(length):
            # slice down to the probability table we're interested in,
            # based on the preceding words
            for word in words[-self.order:]:
                found = False
                for item in current_table:
                    if item['word'] == word and 'next' in item and len(item['next']):
                        current_table = item['next']
                        found = True
                        break
                if not found:
                    current_table = probabilities

            # roll the dice and pick a word based on the current table
            rand = random()
            chosen = current_table[-1]['word']
            for token in current_table:
                if rand < token['chance']:
                    chosen = token['word']
                    break
            words.append(chosen)
        return words

    def add(self, input):
        self.scan(self.tokenize(input))
        self.probabilities = self.compute_probabilities(self.order)

    def generate(self, length):
        return " ".join(self.generate_stream(self.probabilities, length))

if __name__ == "__main__":
    import sys
    m = Markov()
    m.add(open(sys.argv[1]).read())
    #print m.probabilities[-1]
    print m.generate(79)
