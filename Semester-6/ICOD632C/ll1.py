
# -*- coding: utf-8 -*-
from collections import defaultdict
import re
import pandas as pd
from tabulate import tabulate

def get_input():
    lines = []
    while True:
        line = raw_input()
        line = line.replace(" ","")
        if line:
            if '|' in line:
                l, r = line.split('->')
                words = r.split('|')
                for i in range(len(words)):
                    lines.append(l + '->' + words[i])
            else:
                lines.append(line)
        else:
            break
    return lines

def get_lhs_rhs():
    lhs = []
    rhs = []
    for rule in rules:
        l,r = rule.split("->")
        lhs.append(l)
        rhs.append(r)
    return lhs, rhs

def get_first(lhs, rhs, n):
    index = -1
    length = -1
    for i,l in enumerate(lhs):
        if rhs[n].startswith(l):
            if len(l) > length:
                index = i
                length = len(l)
    if index!= -1:
        non_term = lhs[index]
        i = 0
        first = []
        for i in range(len(rhs)):
            if lhs[i] == non_term:
                resu = get_first(lhs,rhs,i)
                if isinstance(resu, (list,)):
                    for j in resu:
                        first.append(j)
                else:
                    first.append(resu)
        return first

    if not rhs[n][0].isalpha():
        return rhs[n][0]
    if rhs[n][0].isalpha():
        ret = ""
        for i in rhs[n]:
            if i.isupper():
                break
            else:
                ret = ret + i
        return ret

def get_follow(lhs, rhs, first ,n, f):
    follow = []
    for i in range(len(rhs)):
        for m in re.finditer(lhs[n],rhs[i]):
            pos = m.start()
            if len(lhs[n]) == 1:
                if rhs[i][pos+1] == "'":
                    pass
                else:
                    if pos == len(rhs[i])-1:
                        resu = f[lhs[i]]
                        if isinstance(resu, (list,)):
                            for k in resu:
                                follow.append(k)
                        else:
                            follow.append(resu)
                        return follow
                    elif not rhs[i][pos+1].isupper():
                        # print("poop")
                        follow.append(rhs[i][pos+1])
                        return follow
                    else:
                        # j = pos + 1
                        for j in range(pos,len(rhs[i])):
                            if rhs[i][j+1].isupper() and rhs[i][j+2] == "'":
                                if '\xd0' not in first[rhs[i][j+1]+"'"]:

                                    resu = first[rhs[i][j+1]+"'"]
                                    if isinstance(resu, (list,)):
                                        for k in resu:
                                            follow.append(k)
                                    else:
                                        follow.append(resu)

                                    return follow
                                else:
                                    if j == len(rhs[i])-3:
                                        resu = first[rhs[i][j+1]+"'"]
                                        if isinstance(resu, (list,)):
                                            for j in resu:
                                                follow.append(j)
                                        else:
                                            follow.append(resu)

                                        if '\xd0' in resu:
                                            resu = f[lhs[i]]
                                            if isinstance(resu, (list,)):
                                                for k in resu:
                                                    follow.append(k)
                                            else:
                                                follow.append(resu)
                                            follow.remove('\xd0')
                                        return follow
                                    else:
                                        resu = first[rhs[i][j+1]+"'"]
                                        if isinstance(resu, (list,)):
                                            for k in resu:
                                                follow.append(k)
                                        else:
                                            follow.append(resu)
                                        follow.remove('\xd0')
                                        j = j + 1

                            elif rhs[i][j+1].isupper() and rhs[i][j+2] != "'":
                                if '\xd0' not in first[rhs[i][j+1]]:
                                    resu = first[rhs[i][j+1]]
                                    if isinstance(resu, (list,)):
                                        for k in resu:
                                            follow.append(k)
                                    else:
                                        follow.append(resu)

                                    return follow
                                else:

                                    if j == len(rhs[i])-2:
                                        resu = first[rhs[i][j+1]]
                                        if isinstance(resu, (list,)):
                                            for j in resu:
                                                follow.append(j)
                                        else:
                                            follow.append(resu)

                                        if '\xd0' in resu:
                                            resu = f[lhs[i]]
                                            if isinstance(resu, (list,)):
                                                for k in resu:
                                                    follow.append(k)
                                            else:
                                                follow.append(resu)
                                            follow.remove('\xd0')
                                        return follow
                                    else:
                                        resu = first[rhs[i][j+1]]
                                        if isinstance(resu, (list,)):
                                            for k in resu:
                                                follow.append(k)
                                        else:
                                            follow.append(resu)
                                        follow.remove('\xd0')
            elif len(lhs[n]) == 2:
                if pos == len(rhs[i])-2:
                    resu = f[lhs[i]]
                    if isinstance(resu, (list,)):
                        for k in resu:
                            follow.append(k)
                    else:
                        follow.append(resu)

                    return follow
                elif not rhs[i][pos+2].isupper():
                    follow.append(rhs[i][pos+2].isupper())
                    return follow
                else:
                    for j in range(pos+1,len(rhs[i])):
                        if rhs[i][j+1].isupper() and rhs[i][j+2] == "'":
                            if 'Є' not in first[rhs[i][j+1]+"'"]:
                                resu = first[rhs[i][j+1]+"'"]
                                if isinstance(resu, (list,)):
                                    for k in resu:
                                        follow.append(k)
                                else:
                                    follow.append(resu)

                                return follow
                            else:
                                if j == len(rhs[i])-3:
                                    resu = first[rhs[i][j+1]+"'"]
                                    if isinstance(resu, (list,)):
                                        for j in resu:
                                            follow.append(j)
                                    else:
                                        follow.append(resu)

                                    if '\xd0' in resu:
                                        resu = f[lhs[i]]
                                        if isinstance(resu, (list,)):
                                            for k in resu:
                                                follow.append(k)
                                        else:
                                            follow.append(resu)
                                        follow.remove('\xd0')
                                    return follow
                                else:
                                    resu = first[rhs[i][j+1]+"'"]
                                    if isinstance(resu, (list,)):
                                        for k in resu:
                                            follow.append(k)
                                    else:
                                        follow.append(resu)
                                    follow.remove('\xd0')
                                    j = j + 1

                        elif rhs[i][j+1].isupper() and rhs[i][j+2] != "'":
                            if 'Є' not in first[rhs[i][j+1]]:
                                resu = first[rhs[i][j+1]]
                                if isinstance(resu, (list,)):
                                    for k in resu:
                                        follow.append(k)
                                else:
                                    follow.append(resu)

                                return follow
                            else:
                                if j == len(rhs[i])-2:
                                    resu = first[rhs[i][j+1]]
                                    if isinstance(resu, (list,)):
                                        for j in resu:
                                            follow.append(j)
                                    else:
                                        follow.append(resu)

                                    if '\xd0' in resu:
                                        resu = f[lhs[i]]
                                        if isinstance(resu, (list,)):
                                            for k in resu:
                                                follow.append(k)
                                        else:
                                            follow.append(resu)
                                        follow.remove('\xd0')
                                    return follow
                                else:
                                    resu = first[rhs[i][j+1]]
                                    if isinstance(resu, (list,)):
                                        for k in resu:
                                            follow.append(k)
                                    else:
                                        follow.append(resu)
                                    follow.remove('\xd0')
    return follow

if __name__=='__main__':
    rules = get_input()
    lhs, rhs = get_lhs_rhs()
    first = defaultdict(list)
    for i,l in enumerate(lhs):
        resu = get_first(lhs,rhs,i)
        if isinstance(resu, (list,)):
            for j in resu:
                first[l].append(j)
        else:
            first[l].append(resu)

    first = dict(first)
    print("First Set:")

    for key,val in first.items():
        if "\xd0" in val:
            val[val.index("\xd0")] = u'\u03B5'
            print key, "=>", val
            val[val.index(u'\u03B5')] = "\xd0"
        else: print key, "=>", val

    follow = defaultdict(list)
    follow[lhs[0]].append('$')
    for i,l in enumerate(lhs):
        resu = get_follow(lhs, rhs, first, i, follow)
        if isinstance(resu, (list,)):
            for j in resu:
                if j not in follow[l]:
                    follow[l].append(j)
        else:
            if j not in follow[l]:
                follow[l].append(resu)
    print ""
    print "Follow Set:"

    for key,val in follow.items():
        print key, "=>", val
    terminals = []
    for i in rhs:
        for j in i:
            if not j.isupper() and not j =="'":
                if j.islower():
                    s = ""
                    for k in i:
                        if k.isupper():
                            break
                        s = s + k
                    if s not in terminals:
                        terminals.append(s)
                else:
                    if j not in terminals:
                        terminals.append(j)

    non_terminals = []
    for i in lhs:
        if i not in non_terminals:
            non_terminals.append(i)
    terminals.append('$')
    terminals.remove('\x84')
    terminals.remove('\xd0')
    df = pd.DataFrame(data = " ",index = non_terminals,columns=terminals)
    print ""
    print "LL-1 Parsing Table:"

    for i,key in enumerate(non_terminals):

        for val in first[key]:
            if val != "\xd0":
                rule = ""
                for n, item in enumerate(lhs):
                    if key in item and '\xd0' not in rhs[n]:
                        if rhs[n].startswith(val):
                            rule = lhs[n]+" -> "+ rhs[n]
                            break
                        else:
                            if rhs[n][0].isupper():
                                rule = lhs[n]+" -> "+ rhs[n]
                                break
                df.at[key, val] = rule
            else:
                for item in follow[key]:
                    df.at[key, item] = key+" -> " + u'\u03B5'
    headers  = terminals
    print(tabulate(df, headers, tablefmt='psql'))


# input
# E -> TE'
# E' -> +TE' | Є
# T -> FT'
# T' -> *FT' | Є
# F -> (E) | id
