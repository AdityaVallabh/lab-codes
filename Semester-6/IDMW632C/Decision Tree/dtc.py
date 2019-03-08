from MyDecisionTree import Node, id3, c45

def generate_tree(data, attrs, method):
    flag = True
    count = {}
    for row in data:
        count[row[-1]] = count.get(row[-1], 0) + 1
    maxi = 0
    cl = None
    for c in count:
        if maxi < count[c]:
            cl = c
            maxi = count[c]
    if maxi == len(data) or not attrs:
        return Node(attr=c, leaf=True)    
    split, tups = method(data, attrs)
    node = Node(attr=split)
    for ch in tups:
        child = generate_tree(tups[ch], [x for x in attrs if x != split], method)
        node.add_child(ch, child)
    return node

def predict(test, root):
    if root.leaf:
        return root.attr
    nxt = test[root.attr]
    return predict(test, root.children[nxt])

def load_data(file):
    data = []
    with open(file) as f:
        cols = f.readline().replace('\n', '').split(',')
        for line in f.readlines():
            row = line.replace('\n', '').split(',')
            data.append(row)
    return data, cols

def main():
    data, cols = load_data('play.csv')
    attrs = range(len(data[0])-1)
    root = generate_tree(data, attrs, id3)
    # import pdb; pdb.set_trace()
    root.print_tree(cols)
    correct = 0
    for test in data:
        res = predict(test, root)
        ans = test[-1]
        if res == ans:
            correct += 1
    print('Accuracy: {}/{} = {}'.format(correct, len(data), correct/len(data)))

if __name__ == '__main__':
    main()
