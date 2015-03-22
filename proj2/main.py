"""The main module for COMS E6111 Project 2"""
import argparse
import logging
import os

import freebase
import infobox

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-api_key', type=str, help='Freebase API key')
parser.add_argument('-query', type=str, help='Query string')
parser.add_argument('-query_type', type=str, choices=['infobox', 'question'],
                    help='Type of query')

def do_infobox_query(api_key, query):
    logger.info('Performing infobox query for \"%s\"', query)
    query_api = freebase.QueryApi(api_key)
    topic_api = freebase.TopicApi(api_key)
    mids = query_api.Query(query)
    for mid in mids:
        is_match = False
        trie = topic_api.GetTrie(mid)
        mid_topics = [t['id'] for t in
                      trie.MatchEntityId('/type/object/type').value]
        for entity_id in infobox.ENTITY_MAP:
            if entity_id in mid_topics:
                is_match = True
                break
        if is_match:
            query_infobox = infobox.Infobox.ConstructFromTrie(trie)
            query_infobox.Print()
            break

def main():
    logging.basicConfig(level=logging.INFO)
    args = parser.parse_args()
    do_infobox_query(args.api_key, args.query)

if __name__ == '__main__':
    main()