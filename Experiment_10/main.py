from itertools import takewhile

s = "S->iEtS|iEtSeS|a"

def groupby(rules):
    d = {}
    initial = list(set([y[0] for y in rules]))

    for y in initial:
        for i in rules:
            if i.startswith(y):
                if y not in d:
                    d[y] = []
                d[y].append(i)

    return d

def prefix(x):
    return len(set(x)) == 1

starting = ""
rules = []
common = []
alphabetset = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]

s = s.replace(" ", "").replace("\n", "")

while True:
    rules = []
    common = []

    split = s.split("->")
    starting = split[0]

    for i in split[1].split("|"):
        rules.append(i)

    for k, I in groupby(rules).items():
        r = [[0] for _ in takewhile(prefix, zip(*I))]
        common.append("".join(r))

    for i in common:
        new_alphabet = alphabetset.pop()
        print(starting + "->" + i + new_alphabet)

        index = []

        for k in rules:
            if k.startswith(i):
                index.append(k)

        for j in index[-1]:
            string_to_print = j.replace("", 1)
            if string_to_print == "T":
                print("03B5", end="")
            else:
                print(string_to_print.replace(i, "", 1), end="")

        string_to_print = index[-1].replace(i, "", 1)

        if string_to_print == "|":
            print("\U03B5", "", end="")
        else:
            print(index[-1].replace(i, "", 1), end="")

        print()

    break
