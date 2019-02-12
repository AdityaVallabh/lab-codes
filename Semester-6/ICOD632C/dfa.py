
class Node:

    def __init__(self, id):
        self.id = id
        self.transitions = {}
        self.final = False

    def set_transition(self, inp, to):
        next_node = Node(to)
        self.transitions[inp] = next_node
        return next_node

    def transition(self, inp):
        try:
            return self.transitions[inp]
        except:
            return None

    def is_final(self):
        return self.final

class DFA:

    def __init__(self, keywords):
        self.automaton = Node(0)
        i = 0
        for keyword in keywords:
            node = self.automaton
            for c in keyword:
                exists = node.transition(c)
                if exists:
                    node = exists
                else:
                    i += 1
                    node = node.set_transition(c, i)
            node.final = True

    def check(self, word):
        node = self.automaton
        for c in word:
            node = node.transition(c)
            if not node:
                return False
        return node.is_final()

def main():
    keywords = ['if','while','then','do','for','else','goto','break','malloc','return', 'ifelse']
    words = ['if', 'iffs', 'while', 'whiles', 'nope', 'ifelse', 'ifels', 'ife']

    dfa = DFA(keywords)

    for word in words:
        if dfa.check(word):
            print('{} is a keyword'.format(word))
        else:
            print('{} is not a keyword'.format(word))
        
if __name__ == '__main__':
    main()
