import unittest

import assoc_list
import data

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

    dataset = data.Dataset(SAMPLE_DATA)
    assoc_rules = assoc_list.assoc_rules(dataset, cutoff_70, 0.1)
    print list(str(x) for x in assoc_rules)

class TestDataset(unittest.TestCase):
  def setUp(self):
    self.dataset = data.Dataset(SAMPLE_DATA)

  def test_GetSupport(self):
    self.assertEqual(0.75, self.dataset.GetSupport(['pen', 'diary']))
    self.assertEqual(1, self.dataset.GetSupport(['pen']))

if __name__ == '__main__':
    unittest.main(verbosity=2)
