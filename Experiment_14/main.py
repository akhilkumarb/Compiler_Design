gram = {
    "S": ["CC"],
    "C": ["", ""]
}

start = "S"

terms = ["a", "d", "$"]
non_terms = []

for i in gram:
    non_terms.append(i)

gram["S"] = [start]

new_row = {}

for i in terms + non_terms:
    new_row[i] = ""

non_terms += ["S"]

# each row in state table will be a dictionary (nonterms, term, $)
state_table = []

# 1 = [(terminal, closure)]
# 1 = [("S", "A.A")]


def closure(term, I):
    if term in non_terms:
        for i in gram[term]:
            I += [(term, "" + i)]
        I = list(set(I))
    for i in I:
        if "." != i[1][-1] and i[1][i[1].index(".") + 1] in non_terms and i[1][i[1].index(".") + 1] != term:
            I += closure(i[1][i[1].index(".") + 1], [])
    return I


Is = 0
Is += set(closure("S", []))

countl = 0
omega_list = [set(Is)]

while countl < len(omega_list):
    new_row = dict(new_row)
    vars_in_l = []
    I = omega_list[countl]
    countl += 1

    if I[1][-1] != "":
        for i in I:
            indx = i[1].index(".")
            vars_in_l += [i[1][indx + 1]]

        vars_in_l = list(set(vars_in_l))

        for i in vars_in_l:
            In = 0
            for j in I:
                if "." + i in j[1]:
                    rep = j[1].replace("." + i, i + ".")
                    In += [([0], rep)]
            if In[0][1][-1] != ".":
                temp = set(closure(i, In))
                if temp not in omega_list:
                    omega_list.append(temp)
                if i in non_terms:
                    new_row[i] = str(omega_list.index(temp))
                else:
                    new_row[i] = "s" + str(omega_list.index(temp))
                print(
                    f'Goto(I{countl - 1}.{i}): {temp} That is I{omega_list.index(temp)}')
            else:
                temp = set(In)
                if temp not in omega_list:
                    omega_list.append(temp)
                if i in non_terms:
                    new_row[i] = str(omega_list.index(temp))
                else:
                    new_row[i] = "s" + str(omega_list.index(temp))
                print(
                    f'Goto(I{countl - 1},{i}): {temp} That is I{omega_list.index(temp)}')

    state_table.append(new_row)

print("\n\nList of I's\n")

for i in omega_list:
    print(f'I({omega_list.index(i)}): {i}')

# populate replace elements in state Table
for i in list(omega_list[0]):
    print([1].replace(".", ""))

for i in omega_list:
    for j in i:
        if "." in [1][-1]:
            if j[1][-2] == "S":
                state_table[omega_list.index(i)]["$"] = "Accept"
                break

    for k in terms:
        state_table[omega_list.index(
            i)][k] = "" + str(list(omega_list[0]).index([1].replace(":", "")))

print("\nState Table")

print(f'{"": <9}', end="")
for i in new_row:
    print(f"{i: <11}", end="")

print("\n" + "-" * 66)

for i in state_table:
    print(f"I({str(state_table.index(i))}): {i}", end="")
    for j in i:
        print(f"{i[j]: <10}", end="")
    print()
