import argparse

import assoc_list
import data

parser = argparse.ArgumentParser()
parser.add_argument('dataset', type=str, help='CSV file containing the data')
parser.add_argument('min_sup', type=float)
parser.add_argument('min_conf', type=float)

def main():
    args = parser.parse_args()
    item_list = data.ParseFile(args.dataset)
    frequent_items = assoc_list.apriori(item_list, args.min_sup)
    for i in sorted(frequent_items, key=lambda x: x.freq, reverse=True):
        print(str(i))

if __name__ == '__main__':
  main()
