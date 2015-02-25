import parsing
import math


class Vector(object):
    """Represents a vector of weighted terms in the Vector model.

    Because these vectors are very sparse, internally this class represents the
    vector as a dictionary mapping terms to their weights.
    """

    def __init__(self, term_weights=None):
        """
        Args:
          term_weights: a dictionary mapping terms in the vector to their
            weights
        """
        if term_weights == None:
            term_weights = {}
        self.term_weights = term_weights

    def get_weight(self, term):
        return self.term_weights.get(term, 0)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __mul__(self, other):
        """Multiplication of a vector by a scalar or another vector.

        Args:
          other: a scalar value to scale the vector weights by or a vector to
              take the dot product with
        Returns:
          a new Vector in the case of scalar multiplication or a scalar in the
          case of multiplication with another vector
        """
        if type(self) == type(other):  # Vector * vector
            dotproduct_sum = 0
            for term, weight in self.term_weights.items():
                dotproduct_sum += weight * other.get_weight(term)
            return dotproduct_sum
        else:  # Scalar * vector
            new_terms = {}
            for term in self.term_weights:
                new_terms[term] = other * self.term_weights[term]
            return type(self)(new_terms)

    def __div__(self, other):
        """Division of a vector by a scalar.

        Args:
          other: a scalar value to divide the vector weights by
        """
        new_terms = {}
        for term in self.term_weights:
            new_terms[term] = self.term_weights[term] / other
        return type(self)(new_terms)

    def __add__(self, other):
        new_terms = {}
        for term, weight in (self.term_weights.items() +
                             other.term_weights.items()):
            new_terms[term] = new_terms.get(term, 0) + weight
        return type(self)(new_terms)

    def __sub__(self, other):
        return self + -1*other

    def __str__(self):
        return str(self.term_weights)

    @property
    def magnitude(self):
        return math.sqrt(sum(x**2 for x in self.term_weights.values()))

    def make_unit(self):
        magnitude = self.magnitude
        for key in self.term_weights:
            self.term_weights[key] /= magnitude

    @classmethod
    def build_from_text(cls, text):
        return cls.build_from_iterable(parsing.tokenize_text(text))

    @classmethod
    def build_from_iterable(cls, iterable):
        terms = {}
        for x in iterable:
            terms[x] = terms.get(x, 0) + 1
        return cls(terms)


class UnitVector(Vector):
    def __init__(self, *args, **kwargs):
        super(UnitVector, self).__init__(*args, **kwargs)
        self.make_unit()
