from math import log2

class Node:

    def __init__(self, attr=None, leaf=False):
        self.attr = attr
        self.children = {}
        self.leaf = leaf

    def add_child(self, choice, node):
        self.children[choice] = node

    def print_tree(self, cols, level=0):
        if self.leaf:
            print('\t'*level + str(self.attr))
        else:
            print('\t'*level + str(cols[self.attr]) + '?')
        for child in self.children:
            print('\t'*level + str(child))
            self.children[child].print_tree(cols, level+1)
     
    def print_rules(self, cols, rule='', level=0):
        if self.leaf:
            rule = rule[:-4]
            rule += 'THEN ' + str(self.attr)
            print(rule)
        else:
            rule += 'IF ' + str(cols[self.attr]) + ' IS '
        for child in self.children:
            rule+= str(child) + ' AND '
            self.children[child].print_rules(cols, rule, level+1)
            rule = rule[:-len(str(child) + ' AND ')] 

def get_info(data):
    ps = {}
    for row in data:
        ps[row[-1]] = ps.get(row[-1], 0) + 1
    info = 0.0
    N = len(data)
    for p in ps:
        info += -(ps[p]/N) * log2(ps[p]/N)
    return info

def id3_c45(data, attrs, algo='id3'):
    info = get_info(data)
    max_gain = 0.0
    split = attrs[0]
    for attr in attrs:
        tups = {}
        for row in data:
            tups[row[attr]] = tups.get(row[attr], []) + [row]        
        info_attr = 0.0
        split_ratio = 0.0
        N = len(data)
        for ch in tups:
            info_attr += (len(tups[ch])/N) * get_info(tups[ch])
            split_ratio += -(len(tups[ch])/N) * log2(len(tups[ch])/N)
        gain = info - info_attr
        gain_ratio = gain/split_ratio
        curr = gain_ratio if algo == 'c4.5' else gain
        if max_gain <= curr:
            max_gain = curr
            split, tuples = attr, tups
    return split, tuples

id3 = lambda data, attrs: id3_c45(data, attrs, algo='id3')
c45 = lambda data, attrs: id3_c45(data, attrs, algo='c4.5')
