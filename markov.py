from random import random
from collections import defaultdict

class Markov:

    def __init__(self, order=3):
        self.order = order
        record = lambda: {'count': 0.0, 'next': defaultdict(record)}
        self.chains = defaultdict(record)
        self.probabilities = []
        self.tokens = []

    def compute_probabilities(self, limit, chain=None):
        chain = chain or self.chains
        probabilities = []
        highest = 0.0
        if limit and len(chain):
            total = sum([i['count'] for i in chain.values()])
            norm = 1/total if total > 0 else 1
            for (token, subchain) in chain.items():
                chance = subchain['count'] * norm
                highest = max(highest, chance)
                probabilities.append({ 'chance': chance,
                                       'word':   token,
                                       'next':   self.compute_probabilities(limit-1, subchain['next']) if 'next' in subchain else []
                                       })
            probabilities.sort(lambda a,b: cmp(a['chance'], b['chance']))
            # normalize to highest chance 
            for prob in probabilities:
                prob['chance'] *= 1.0/highest
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
            if len(current_table) == 0:
                continue
            chosen = current_table[-1]['word']
            for token in current_table:
                if rand < token['chance']:
                    chosen = token['word']
                    break
            words.append(chosen)
        return words

    def add(self, input):
        self.tokens.extend(self.tokenize(input))

    def compute(self):
        self.scan(self.tokens)
        self.probabilities = self.compute_probabilities(self.order)

    def generate(self, length):
        return " ".join(self.generate_stream(self.probabilities, length))

if __name__ == "__main__":
    import sys
    m = Markov()
    m.add(open(sys.argv[1]).read())
    m.add(open(sys.argv[2]).read())
    m.compute()
    print m.generate(79)
