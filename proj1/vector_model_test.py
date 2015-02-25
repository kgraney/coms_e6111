import vector_model
import unittest
import math


class TestVector(unittest.TestCase):

    def test_mul(self):
        v1 = vector_model.Vector({'a': 1, 'b': 2, 'c': 0, 'd': 0.4})
        v2 = 2*v1
        v3 = vector_model.Vector({'a': 9, 'e': 5, 'c': 0, 'd': 0.4})
        p4 = v1*v3
        self.assertEqual(1, v1.get_weight('a'))
        self.assertEqual(2, v1.get_weight('b'))
        self.assertEqual(0, v1.get_weight('c'))
        self.assertEqual(0.4, v1.get_weight('d'))
        self.assertEqual(2, v2.get_weight('a'))
        self.assertEqual(4, v2.get_weight('b'))
        self.assertEqual(0, v2.get_weight('c'))
        self.assertEqual(0.8, v2.get_weight('d'))

        self.assertAlmostEqual(9.16, p4, places=8)

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

    def test_make_unit(self):
        v1 = vector_model.Vector({'a': 1, 'b': 2, 'c': 0, 'd': 0.4})
        v1_orig = v1
        self.assertNotEqual(1, v1.magnitude)
        v1.make_unit()
        self.assertEqual(1, v1.magnitude)

        # Make sure the two vectors point in the same direction
        self.assertEqual(0, math.acos((v1 * v1_orig) /
                                      (v1.magnitude * v1_orig.magnitude)))

if __name__ == '__main__':
    unittest.main(verbosity=2)
