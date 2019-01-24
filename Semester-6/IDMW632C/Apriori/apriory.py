import sys

to_str = lambda s: ' '.join([x for x in s])
to_set = lambda s: set(s.split())

datatable = []
freq = {}

def apriori(item_sets):
    new_sets = []
    for i in range(0, len(item_sets)):
        for j in range(i+1, len(item_sets)):
            s1 = item_sets[i].split()
            s2 = item_sets[j].split()
            if s1[:-1] != s2[:-1]:
                continue
            tmp = s1 + [s2[-1]]
            for k in range(len(tmp)):
                tmp_set = to_str(set(tmp[:k]+tmp[k+1:]))
                if tmp_set in item_sets:
                    if to_str(set(tmp)) not in new_sets:
                        new_sets.append(to_str(set(tmp)))
    return new_sets

def print_closed_freq_sets(prev, item_sets):
    for prev_set in prev:
        closed = True
        for item_set in item_sets:
            if to_set(prev_set).issubset(to_set(item_set)) and freq[prev_set] == freq[item_set]:
                closed = False
                break
        if closed:
            print('{}: {}'.format(prev_set, freq[prev_set]))

def load_data(file):
    item_sets = []
    with open(file) as f:
        for line in f.readlines():
            transaction = set(line.replace('\n','').split())
            datatable.append(transaction)
            for item in transaction:
                if item in item_sets:
                    freq[item] += 1
                else:
                    item_sets.append(item)
                    freq[item] = 1
    return item_sets

def check_min_sup(item_sets, min_sup):
    for item_set in item_sets:
        count = 0
        for transaction in datatable:
            if to_set(item_set).issubset(transaction):
                count += 1
        if count >= min_sup:
            freq[item_set] = count
    return list(filter(lambda x: x in freq, item_sets))

def main():
    item_sets = []
    min_sup = float(input('Minimum support (in %): '))
    file = sys.argv[1] if len(sys.argv) > 1 else 'dataset.dat'
    item_sets = load_data(file)
    min_sup = min_sup*len(datatable)/100.0 if min_sup >= 0 else 1
    item_sets = list(filter(lambda x: freq[x] >= min_sup, item_sets))
    print('min_sup = {}'.format(min_sup))
    # for item in item_sets:
    #     print('{}: {}'.format(item, freq[item]))
    while True:
        prev = item_sets
        item_sets = apriori(item_sets)
        if not item_sets:
            break
        item_sets = check_min_sup(item_sets, min_sup)
        print_closed_freq_sets(prev, item_sets)
        # for item_set in item_sets:
        #     print('{}: {}'.format(item_set, freq[item_set]))
    print_closed_freq_sets(prev, item_sets)

if __name__ == "__main__":
    main()
