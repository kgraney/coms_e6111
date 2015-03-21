import unittest
import logging

import freebase


API_KEY = 'AIzaSyDLJVRvXRTOyZoM4cS2w_LqHK3bxkYtbkE'

class TestQueryApi(unittest.TestCase):
    def setUp(self):
        self.query_api = freebase.QueryApi(API_KEY)
        self.topic_api = freebase.TopicApi(API_KEY)

    def test_something(self):
        mids = self.query_api.Query('Bill Gates')
        for mid in mids:
            print(self.topic_api.GetTrie(mid))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    unittest.main(verbosity=2)
