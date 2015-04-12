from collections import defaultdict
from itertools import combinations

class Itemset(object):
    def __init__(self, items, freq):
        self.items = tuple(sorted(items))
        self.freq = freq

    def get_set(self):
        return set(self.items)

    def __repr__(self):
        return '<%s %0.2f>' % (str(self.items), self.freq)

def apriori(item_lists, min_sup):
    """
    Implementation of the Apriori algorithm for finding large item sets.

    item_lists: a list of item lists
    min_sup: a [0,1] value representing the minimum support level for frequent
        itemsets
    """
    L = {}
    # Count the large 1-itemsets (L_1)
    item_freq = defaultdict(float)
    n = len(item_lists)
    for item_list in item_lists:
        for item in item_list:
            item_freq[item] += 1.0/n
    L[1] = set(Itemset([item], item_freq[item])
               for item in item_freq if item_freq[item] >= min_sup)
    # Find the remaining large itemsets (L_2,...,L_k)
    k = 2
    while L[k-1] != set():
        Ck = apriori_gen(L[k-1], k-1)
        for i_set in (set(x) for x in item_lists):
            for c in Ck:
                if c.get_set().issubset(i_set):
                    c.freq += 1.0/n
        L[k] = set(c for c in Ck if c.freq >= min_sup)
        k += 1
    return [item for sublist in L.values() for item in sublist]

def apriori_gen(L, k):
    C = set()
    for p in L:  # Join
        for q in L:
            if (p.items[:-1] == q.items[:-1]) and (p.items[-1] < q.items[-1]):
                C.add(Itemset(p.items + (q.items[-1],), 0))
    L_set = set(x.items for x in L)
    for c in C:  # Prune
        for s in list(combinations(c.items, k)):
            if s not in L_set:
                print "Deleting ", s
        pass
    return C
