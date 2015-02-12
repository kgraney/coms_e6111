import argparse
import logging
import os

import results

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('api_key', type=str, help='Bing Search API key')
parser.add_argument('precision', type=float,
        help='The target for precision@10 of the expanded query')
parser.add_argument('query', type=str, help='The initial query')

def ask_user_for_relevance(results):
    """Interactively ask the user to mark the relevant results.

    Args:
      results: a list of BingResult objects

    Side-effects:
      Modifies the result objects passed, setting is_relevant=True if the user
      marked the result as relevant.
    """
    for i,result in enumerate(results):
        hdr = 'Result #%d ' % (i+1)
        prompt_text = 'Is result #%d relevant? [y/n] ' % (i+1)
        print '\n' + hdr + '-'*(70 - len(hdr))
        print result.to_formatted_string()
        print '-'*70
        while True:
            input = raw_input(prompt_text).strip().lower()
            if input == 'y' or input == 'n':
                break
        if input == 'y':
            result.is_relevant = True


def query_expansion_loop(query_terms, target_precision):
    """Run the user-interactive loop that expands the query.

    Args:
      query_terms: an ordered list of query terms for the initial query
      target_precision: the target for precision@10 of the expanded query
    """
    logger.info('Target Precision: %f', target_precision)
    precision = 0
    while True:
        logger.info('Querying: %s', query_terms)
        # TODO(kevin): construct from query terms instead of static JSON
        #query = results.BingQuery(query_terms)
        query = results.BingQuery.build_from_json(os.path.join(os.path.dirname(
                os.path.realpath(__file__)), 'sample_data', 'sample_output.json'))
        ask_user_for_relevance(query.results)
        precision = query.compute_precision()
        logger.info('Precision: target=%f actual=%f', target_precision, precision)
        if precision == 0:
            logger.warning('Giving up because the user marked none of the '
                           'results relevant.')
            break
        elif precision >= target_precision:
            logger.info('The target precision has been obtained.')
            break

        # TODO: add one or two more words to the query

def main():
    logging.basicConfig(level=logging.INFO)
    args = parser.parse_args()
    query_expansion_loop(args.query.split(), args.precision)

if __name__ == '__main__':
    main()
