import parsing

class Vector(object):
    """Represents a vector of weighted terms in the Vector model.

    Because these vectors are very space, internally this class represents the
    vector as a dictionary mapping terms to their weights.
    """

    def __init__(self, term_weights):
        """
        Args:
          term_weights: a dictionary mapping terms in the vector to their
            weights
        """
        self.term_weights = term_weights

    def get_weight(self, term):
        return self.term_weights[term]

    def __rmul__(self, other):
        """Multiplication of a vector by a scalar.

        Intentionally only supports __rmul__ to keep the code idiomatic, i.e.
        2*vec is valid, but vec*2 is invalid.

        Args:
          other: a scalar value to scale the vector weights by
        """
        new_terms = {}
        for term in self.term_weights:
            new_terms[term] = other * self.term_weights[term]
        return type(self)(new_terms)

    def __add__(self, other):
        new_terms = {}
        for term, weight in (self.term_weights.items() +
                             other.term_weights.items()):
            new_terms[term] = new_terms.get(term, 0) + weight
        return type(self)(new_terms)

    def __str__(self):
        return str(self.term_weights)

    @classmethod
    def build_from_text(cls, text):
        terms = {}
        for x in parsing.tokenize_text(text):
            terms[x] = terms.get(x, 0) + 1
        return cls(terms)
