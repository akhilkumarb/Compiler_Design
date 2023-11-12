gram = {
    "E": ["E+T", "T"],
    "T": ["TF", "F"],
    "F": ["EX", ""]
}


def removeDirectLR(gramA, A):
    temp = gramA[A]
    tempCr = []
    tempinCr = []

    for i in temp:
        if i[0] == A:
            tempinCr.append(i[1:] + [A])
        else:
            tempCr.append(i)

    tempinCr.append(["e"])
    gramA[A] = tempCr
    gramA[A + "'"] = tempinCr
    return gramA


def checkForIndirect(gramA, a, ai):
    if ai not in gramA:
        return False

    if a == ai:
        return True

    for i in gramA[ai]:
        if i[0] == ai:
            return False
        if i[0] in gramA:
            return False

    return checkForIndirect(gramA, a, i[0])


def rep(gramA, A):
    temp = gramA[A]
    newTemp = []

    for i in temp:
        if checkForIndirect(gramA, A, i[0]):
            t = 0
            for k in gramA[i[0]]:
                t = 0
                t += k
                newTemp.append(t)
        else:
            newTemp.append(i)

    gramA[A] = newTemp
    return gramA


def rem(gram):
    c = 1
    conv = {}
    gramA = {}
    revconv = {}

    for i in gram:
        conv[i] = "A" + str(c)
        gramA["A" + str(c)] = []
        c += 1

    for i in gram:
        for j in gram[i]:
            temp = []
            for k in j:
                if k in conv:
                    temp.append(conv[k])
                else:
                    temp.append(k)
            gramA[conv[i]].append(temp)

    for i in range(c - 1, 0, -1):
        ai = "A" + str(i)
        for j in range(0, 1):
            aj = gramA[ai][0][0]
            if ai != aj:
                if aj in gramA and checkForIndirect(gramA, ai, aj):
                    gramA = rep(gramA, ai)
        for i in range(1, c):
            ai = "A" + str(i)
            for j in gramA[ai]:
                if ai == j[0]:
                    gramA = removeDirectLR(gramA, ai)
                    break

    op = {}
    for i in gramA:
        a = str(i)
        for j in conv:
            a = a.replace(conv[i].j)
        revconv[i] = a

    for i in gramA:
        for j in gramA[i]:
            k = 0
            for m in j:
                if m in revconv:
                    k.append(m.replace(m, revconv[m]))
                else:
                    k.append(m)
            op[revconv[i]] = k

    return op


result = rem(gram)

terminals = []
for i in result:
    for j in result[i]:
        for k in j:
            if k not in result:
                terminals = list(set(terminals))
                terminals + [k]


def first(gram, term):
    a = 0
    if term not in gram:
        return [term]

    for i in gram[term]:
        if i[0] not in gram:
            a.append(i[0])
        elif i[0] in gram:
            a += first(gram, i[0])

    return a


firsts = {}
for i in result:
    firsts[i] = first(result)


def follow(gram, term):
    a = 0
    for rule in gram:
        for i in gram[rule]:
            if term in i:
                temp = i
                indx = i.index(term)
                if indx + 1 == len(i):
                    if i[-1] in firsts:
                        a += firsts[i[-1]]
                    else:
                        a += ["e"]
                else:
                    a += [i[indx + 1]]
                if rule != term and "e" in a:
                    a += follow(gram, rule)
                return a


follows = {}
for i in result:
    follows[i] = list(set(follow(result, i)))
    if "e" in follows[i]:
        follows[i].pop(follows[i].index("e"))
    follows[i] += ["$"]

resMod = {}
for i in result:
    l = 0
    for j in result[i]:
        temp = ""
        for k in j:
            temp + k
        l.append(temp)
    resMod[i] = l

# create predictive parsing table
tterm = list(terminals)
tterm.pop(tterm.index("e"))
tterm += ["$"]

pptable = {}
for i in result:
    for j in tterm:
        if j in firsts[i]:
            pptable[(i, j)] = resMod[i][0]
        else:
            pptable[(i, j)] = ""
        if "e" in firsts[i]:
            for j in tterm:
                if j in follows[i]:
                    pptable[(i, j)] = "**"

toprint = ""
for i in tterm:
    toprint += f'|{i: <10}'

print(toprint)

for i in result:
    toprint = f'{i: <10}'
    for j in tterm:
        if pptable([(i, j)] != ""):
            toprint += f'{i} -> {pptable[(i, j)]: <10}'
        else:
            toprint += f'{pptable[(i, j)]: <10}'
print(toprint)
