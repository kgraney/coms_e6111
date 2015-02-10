"""Classes that handle interaction with Bing."""
import json
import urllib2

import parsing


class BingQuery(object):
    """Represents a Bing query."""

    def __init__(self):
        # A list of ordered BingResult objects representing the result documents for
        # this query.
        self.results = []

    def execute(self):
        """Execute the query on Bing."""
        pass

    def compute_precision(self):
        """Compute the precision of this query.

        Must be run after execute()

        Returns:
          A float containing the precision of the query.
        """
        pass


class BingResult(object):
    """Represents an individual Bing search result."""

    def __init__(self, title, description, url):
        self.title = title
        self.description = description
        self.url = url

    def get_page_contents(self):
        """Get the contents of the result HTML webpage.

        Returns:
            A string with the text contents of the URL in the result.
        """
        request = urllib2.Request(self.url)
        response = urllib2.urlopen(request)
        return parsing.extract_page_text(response.read())

    @classmethod
    def build_from_json(cls, json_str):
        """Constructs an object of this type from a single Bing result.

        Args:
          json_str: A JSON string representing an item in the 'results' list from a
            'Bing' response.

        Returns:
          A BingResult object.
        """
        json_obj = json.loads(json_str)
        return cls(title=json_obj['Title'],
                   description=json_obj['Description'],
                   url=json_obj['Url'])
