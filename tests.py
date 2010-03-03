import unittest
from markov import Markov

class TestParsing(unittest.TestCase):
    def setUp(self):
        self.markov = Markov()

    def test_basic_tokenize(self):
        result = self.markov.tokenize("grraaaaa brainss monkeybutter")
        self.assertEquals(result, ["grraaaaa", "brainss", "monkeybutter"])

    def test_basic_scan(self):
        self.markov.scan(['a', 'b', 'c', 'd', 'e'])
        self.assertTrue('a' in self.markov.chains)
        self.assertTrue('b' in self.markov.chains)
        self.assertTrue('c' in self.markov.chains)

        self.assertTrue('b' in self.markov.chains['a']['next'])
        self.assertTrue('c' in self.markov.chains['a']['next']['b']['next'])
        self.assertTrue('d' in self.markov.chains['b']['next']['c']['next'])

    def test_count(self):
        m = Markov(2)
        m.scan(['a', 'b', 'b', 'b', 'c'])
        self.assertEquals(m.chains['a']['count'], 1)
        self.assertEquals(m.chains['b']['count'], 3)

        self.assertEquals(m.chains['a']['next']['b']['count'], 1)
        self.assertEquals(m.chains['b']['next']['b']['count'], 2)
        self.assertEquals(m.chains['b']['next']['c']['count'], 1)
        
if __name__ == '__main__':
    unittest.main()
