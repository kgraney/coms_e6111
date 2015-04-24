import argparse
import logging

import assoc_list
import data
import itertools

parser = argparse.ArgumentParser()
parser.add_argument('dataset', type=str, help='CSV file containing the data')
parser.add_argument('min_sup', type=float)
parser.add_argument('min_conf', type=float)


def main():
    logging.basicConfig(level=logging.INFO)
    args = parser.parse_args()
    item_list = data.ReadIntegratedDataset(args.dataset)
    dataset = data.Dataset(item_list)

    sum_lens = 0
    item_set = set()
    for tl in item_list:
        sum_lens += len(tl)
        for i in tl:
            item_set.add(i)

    print 'Unique items = ', len(item_set)
    print 'Average transaction length = ', sum_lens / float(len(item_list))

    print '==Frequent itemsets (min_sup=%f%%)' % (args.min_sup * 100)
    frequent_items = assoc_list.apriori(item_list, args.min_sup)
    for i in sorted(frequent_items, key=lambda x: x.freq, reverse=True):
        print(str(i))

    print ''
    print('==High-confidence association rules (min_conf=%f%%)' %
          (args.min_conf * 100))
    assoc_rules = assoc_list.assoc_rules(dataset, frequent_items, args.min_conf)
    for i in sorted(assoc_rules, key=lambda x: x.conf, reverse=True):
        print(str(i))


if __name__ == '__main__':
  main()
