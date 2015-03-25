"""The main module for COMS E6111 Project 2"""
import argparse
import logging
import os
import re

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

def do_question_query(api_key, query):
    result = re.match(r'who\s+created\s+([^?]*)\??', query, re.IGNORECASE)
    assert result is not None, 'Invalid question!'
    query = result.group(1)

    logger.info('Performing question query for \"%s\"', query)
    results = []
    for kind in (True, False):
        question_api = freebase.QuestionApi(api_key, kind)
        results.extend(question_api.Query(query))
    for i,text in enumerate(sorted(results)):
        print '%d. %s' % (i+1, text)

def main():
    logging.basicConfig(level=logging.INFO)
    args = parser.parse_args()
    if args.query_type == 'infobox':
        do_infobox_query(args.api_key, args.query)
    elif args.query_type == 'question':
        do_question_query(args.api_key, args.query)

if __name__ == '__main__':
    main()
