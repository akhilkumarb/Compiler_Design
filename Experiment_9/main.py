gram = {}


def add(str):
    str = str.replace(" ", "").replace("\"", "").replace("\n", "")

    x = str.split("->")
    y = x[1]
    x.pop()
    z = y.split("|")
    x.append(z)
    gram[x[0]] = x[1]


def removeDirectLR(gramA, A):
    temp = gramA[A]
    tempCr = []
    templnCr = []

    for i in temp:
        if i[0] == A:
            templnCr.append(i[1:] + [A + "'"])
        else:
            tempCr.append(i + [A + "'"])

    templnCr.append(["e"])

    gramA[A] = tempCr
    gramA[A + "'"] = templnCr

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
            return checkForIndirect(gramA, a, i[0])

    return False


def rep(gramA, A):
    temp = gramA[A]
    newTemp = []

    for i in temp:
        if checkForIndirect(gramA, A, i[0]):
            t = 0
            for k in gramA[i[0]]:
                t += k
            t += i[1:]
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

    for j in gram:
        conv[j] = "A" + str(c)
        gramA["A" + str(c)] = []

        c += 1

    for i in gram:
        for k in gram[i]:
            temp = []
            for m in k:
                if m in conv:
                    temp.append(conv[m])
                else:
                    temp.append(m)
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
            a = a.replace(conv[j], j)
        revconv[i] = a

    for i in gramA:
        l = []
        for j in gramA[i]:
            k = []
            for m in j:
                if m in revconv:
                    k.append(m.replace(m, revconv[m]))
                else:
                    k.append(m)
            l.append(k)
        op[revconv[i]] = l

    return op


n = int(input("Enter No of Production: "))

for i in range(n):
    txt = input()
    add(txt)

result = rem(gram)

for x, y in result.items():
    print(f"{x} ->", end="")
    for index, i in enumerate(y):
        print("".join(i), end="")
        if index != len(y) - 1:
            print("|", end="")
    print()
