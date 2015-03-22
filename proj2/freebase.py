import abc
import logging
import json
import urllib
import urllib2

logger = logging.getLogger(__name__)

def EntityToList(entity_id):
    return entity_id.split('/')[1:]

class FreebaseApi(object):
    def __init__(self, api_key):
        self.api_key = api_key

    @abc.abstractmethod
    def GetApiUrl(self, param):
        pass

    def ExecuteQuery(self, param):
        url = self.GetApiUrl(param)
        logger.info('Querying %s', url)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        return response.read()


class QueryApi(FreebaseApi):
    BASE_URL = 'https://www.googleapis.com/freebase/v1/search?'

    def GetApiUrl(self, param):
        """
        Args:
          param - the query string
        """
        url_params = {'query': param,
                      'key': self.api_key}
        return self.BASE_URL + urllib.urlencode(url_params)

    def Query(self, query):
        data = json.loads(self.ExecuteQuery(query))
        mids = []
        for result in data['result']:
            mids.append(result['mid'])
        return mids

class TopicApi(FreebaseApi):
    BASE_URL = 'https://www.googleapis.com/freebase/v1/topic'

    def GetApiUrl(self, param):
        """
        Args:
          param - the mid of an object
        """
        url_params = {'key': self.api_key}
        return (self.BASE_URL + param + '?'
                + urllib.urlencode(url_params))

    def Query(self, mid):
        data = json.loads(self.ExecuteQuery(mid))
        return data

    def GetTrie(self, mid):
        data = self.Query(mid)
        return EntityNode.ConstructTrie(dict((x[0], x[1]['values'])
                                        for x in data['property'].items()))

class EntityNode(object):
    def __init__(self, name=None, root=False):
        self.name = name
        self.children = {}
        self.value = None

    def Insert(self, entity, value):
        return self._InsertHelper(EntityToList(entity), value)

    def _InsertHelper(self, entity_list, value):
        node_name = entity_list[0]
        try:
            node = self.children[node_name]
        except (KeyError):
            node = EntityNode(node_name)
            self.children[node_name] = node

        if entity_list[1:] == []:
            node.value = value
        else:
            node._InsertHelper(entity_list[1:], value)

    def AddChild(self, entity, node):
        self.children[entity] = node

    def GetChild(self, entity):
        return self.children[entity]

    def GetOrAddChild(self, entity):
        try:
            self.children[entity]
        except (KeyError):
            self.children[entity] = EntityNode()
            return self.children[entity]

    def MatchEntityId(self, entity_id):
        lst = EntityToList(entity_id)
        return self._MatchEntityIdHelper(lst)

    def _MatchEntityIdHelper(self, entity_id_lst):
        if entity_id_lst == []:
            return self
        try:
            child = self.children[entity_id_lst[0]]
            return child._MatchEntityIdHelper(entity_id_lst[1:])
        except (KeyError):
            return None

    @classmethod
    def ConstructTrie(cls, d):
        """
        Args:
          d - a dictionary of entity name mapped to a value list
        """
        root = cls()
        for entity, value in d.items():
            root.Insert(entity, value)
        return root
