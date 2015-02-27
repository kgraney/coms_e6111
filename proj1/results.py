"""Classes that handle interaction with Bing."""
import heapq
import json
import logging
import textwrap
import urllib2

import bing
import parsing
import vector_model

logger = logging.getLogger(__name__)

class BingQuery(object):
    """Represents a Bing query."""

    def __init__(self, query_terms=()):
        self.query_terms = list(query_terms)

        # A list of ordered BingResult objects representing the result documents for
        # this query.
        self.results = []

        # Our best estimate so far of a vector representing the direction of
        # relevance for the query.
        self.relevance_vector = vector_model.UnitVector()

    def execute(self, api_key):
        """Execute the query on Bing."""
        bing_resp = bing.execute_query(' '.join(self.query_terms), api_key)
        data = json.loads(bing_resp)
        for result in data['d']['results']:
            self.results.append(BingResult.build_from_json(result))

    def compute_precision(self):
        """Compute the precision of this query.

        Must be run after results are populated (e.g. from a call to execute()).

        Returns:
          A float containing the precision of the query.
        """
        return float(sum(x.is_relevant for x in self.results))/len(self.results)

    def get_query_vector(self):
        return vector_model.UnitVector.build_from_iterable(self.query_terms)

    def next_query(self):
        """
        Assumptions:
          - there is at least one relevant result

        Returns:
          a BingQuery object
        """
        query_vector = self.get_query_vector()
        avg_relevant_result = vector_model.UnitVector()
        for result in self.results:
            if result.is_relevant:
              avg_relevant_result += result.get_vector()
            else:
              avg_relevant_result -= result.get_vector()

        for term in query_vector.terms:
            avg_relevant_result.zero_coordinate(term)

        relevance_vector = self.relevance_vector + avg_relevant_result
        new_query_lst = sorted(
                heapq.nlargest(2, relevance_vector.term_weights.iteritems(),
                               key=lambda x: x[1]) +
                query_vector.term_weights.items(),
                key=lambda x: x[1],
                reverse=True)

        new_query = type(self)(x[0] for x in new_query_lst)
        new_query.relevance_vector = relevance_vector
        return new_query

    @classmethod
    def build_from_json(cls, fname):
        """Construct an instance of the class using query results from a JSON file.

        Args:
          fname: the name of a JSON file with the Bing results to use for testing.
        Returns:
          An instance of BingQuery with results initialized.
        """
        obj = cls()
        with open(fname) as f:
            data = json.load(f)
            for result in data['d']['results']:
                obj.results.append(BingResult.build_from_json(result))
        return obj


class BingResult(object):
    """Represents an individual Bing search result."""

    def __init__(self, title, description, url):
        self.title = title
        self.description = description
        self.url = url

        # Was this result marked as relevant by the user?
        self.is_relevant = False

    def get_page_contents(self):
        """Get the contents of the result HTML webpage.

        Returns:
            A string with the text contents of the URL in the result.
        """
        request = urllib2.Request(self.url)
        try:
            response = urllib2.urlopen(request)
            return parsing.extract_page_text(response.read())
        except Exception as e:
            logger.info('Ignoring page contents for %s: %s', self.url, str(e))
            return ''

    def to_formatted_string(self):
        return '%s\n%s\n\n%s' % (self.title, self.url,
                                 textwrap.fill(self.description))

    def get_vector(self):
        target_page_vec = vector_model.Vector.build_from_text(
            self.get_page_contents())
        description_vec = vector_model.Vector.build_from_text(
            self.description)

        # Weight the description vector higher than the actual page (we assume
        # Bing provides high-quality descriptions).
        vec = 2*description_vec + target_page_vec
        return vector_model.UnitVector(vec.term_weights)

    @classmethod
    def build_from_json(cls, json_obj):
        """Constructs an object of this type from a single Bing result.

        Args:
          json_obj: A JSON structure representing an item in the 'results' list
            from a 'Bing' response, i.e. nested lists and dictionaries.

        Returns:
          A BingResult object.
        """
        return cls(title=json_obj['Title'],
                   description=json_obj['Description'],
                   url=json_obj['Url'])
