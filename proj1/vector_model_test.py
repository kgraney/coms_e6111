import vector_model
import unittest


class TestVector(unittest.TestCase):

    def test_mul(self):
        v1 = vector_model.Vector({'a': 1, 'b': 2, 'c': 0, 'd': 0.4})
        v2 = 2*v1
        v3 = vector_model.Vector({'a': 9, 'e': 5, 'c': 0, 'd': 0.4})
        v4 = v1*v3
        self.assertEqual(1, v1.get_weight('a'))
        self.assertEqual(2, v1.get_weight('b'))
        self.assertEqual(0, v1.get_weight('c'))
        self.assertEqual(0.4, v1.get_weight('d'))
        self.assertEqual(2, v2.get_weight('a'))
        self.assertEqual(4, v2.get_weight('b'))
        self.assertEqual(0, v2.get_weight('c'))
        self.assertEqual(0.8, v2.get_weight('d'))

        self.assertEqual(9, v4.get_weight('a'))
        self.assertEqual(0, v4.get_weight('b'))
        self.assertEqual(0, v4.get_weight('c'))
        self.assertAlmostEqual(0.16, v4.get_weight('d'), places=8)
        self.assertEqual(0, v4.get_weight('e'))

    def test_add(self):
        v1 = vector_model.Vector({'a': 1, 'b': 2, 'c': 0, 'd': 0.4})
        v2 = vector_model.Vector({'a': 2, 'b': 4, 'e': 0, 'f': 0.4})
        vs = v1 + v2
        self.assertEqual(3, vs.get_weight('a'))
        self.assertEqual(6, vs.get_weight('b'))
        self.assertEqual(0, vs.get_weight('c'))
        self.assertEqual(0.4, vs.get_weight('d'))
        self.assertEqual(0, vs.get_weight('e'))
        self.assertEqual(0.4, vs.get_weight('f'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
