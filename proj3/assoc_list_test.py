import unittest

import assoc_list

SAMPLE_DATA = [
    ['pen', 'ink', 'diary', 'soap'],
    ['pen', 'ink', 'diary'],
    ['pen', 'diary'],
    ['pen', 'ink', 'soap']]

class TestApriori(unittest.TestCase):

    def test_sample_data(self):
        cutoff_0 = assoc_list.apriori(SAMPLE_DATA, 0)
        self.assertEqual(2**4 - 1, len(cutoff_0))
        cutoff_70 = assoc_list.apriori(SAMPLE_DATA, 0.7)

if __name__ == '__main__':
    unittest.main(verbosity=2)
