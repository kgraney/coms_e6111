from collections import defaultdict
import itertools


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return itertools.chain.from_iterable(itertools.combinations(s, r)
                                         for r in range(len(s)+1))

class Itemset(object):
    def __init__(self, items, freq):
        self.items = tuple(sorted(items))
        self.freq = freq

    def get_set(self):
        return set(self.items)

    def __repr__(self):
        return '<%s %0.4f>' % (str(self.items), self.freq)

    def __str__(self):
        return '%s, %f' % (self.list_str(), self.freq)

    def list_str(self):
        return '[%s]' % ','.join(self.items)

class AssociationRule(object):
    def __init__(self, dataset, lhs, rhs):
        self.dataset = dataset
        self.lhs = lhs
        self.rhs = rhs
        self._ComputeConfidence()

    def _ComputeConfidence(self):
        self.conf = (self.dataset.GetSupport(self.lhs + self.rhs) /
                     self.dataset.GetSupport(self.lhs))

    def __str__(self):
        return '[%s] => [%s] (Conf: %f%%, Supp: %f%%)' % (','.join(self.lhs),
                ','.join(self.rhs), 100*self.conf, 0)

    def __eq__(self, other):
        return (set(self.lhs) == set(other.lhs) and
                set(self.rhs ) == set(other.rhs))

    def __hash__(self):
        return hash(tuple(sorted(self.lhs) + ['|'] + sorted(self.rhs)))

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
    C_pruned = set()
    for c in C:  # Prune
        for s in list(itertools.combinations(c.items, k)):
            if s in L_set:
                C_pruned.add(c)
    return C_pruned

def assoc_rules(dataset, frequent_items, min_conf):
    seen_subsets = set()
    rules = set()
    for item in frequent_items:
        for subset in powerset(item.items):
            if len(subset) <= 1 or subset in seen_subsets:
                continue
            seen_subsets.add(subset)
            for i, rhs in enumerate(subset):
                lhs = subset[0:i] + subset[i+1:]
                rule = AssociationRule(dataset, lhs, (rhs,))
                if rule.conf >= min_conf:
                    rules.add(rule)
    return rules
