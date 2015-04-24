from collections import defaultdict
import copy
import csv
import gzip
import logging

logger = logging.getLogger(__name__)

def ParseFile(filename):
    integrated_dataset = []
    row_labels = None
    logger.info('Reading file %s', filename)
    with gzip.open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            transaction = []
            if row_labels is None: 
                row_labels = row
            else:
                for i, value in enumerate(row):
                    if i == 12:
                        continue
                    if value == 'Y':
                        transaction.append(row_labels[i])
                    if i == 9:   # Suspected crime
                        transaction.append(value)
                    if i == 79:  # Gender
                        transaction.append(value)
                    #elif value == 'N':
                    #    transaction.append('not_' + row_labels[i])
                integrated_dataset.append(transaction)
    logger.info('Finished constructing integrated dataset from %s', filename)
    return integrated_dataset


class Dataset(object):
    def __init__(self, integrated_dataset):
        self.data = integrated_dataset
        self.support = defaultdict(set)

        for trans_id, trans_lst in enumerate(self.data):
            for item in trans_lst:
                self.support[item].add(trans_id)

    def GetSupport(self, itemset):
        support_set = copy.copy(self.support[itemset[0]])
        for item in itemset[1:]:
            support_set &= self.support[item]
        return len(support_set)/float(len(self.data))

