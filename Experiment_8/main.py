inp = "((e+a).b)"  # input("")

start = 1  # denotes start of e-nfa table

end = 1  # denotes end of our table which is initially the same as start

cur = 1  # denotes the current position of our pointer

# this is an initial e-nfa table with only one state which is the start and end both
table = [["state", "epsilon", "a", "b"], [1]]


def print_table(table):
    i = table[0]
    print(f"{i[0]:<10} {i[1]:<10} {i[2]:<10} {i[3]:<10}")
    print("-" * 46)

    for i in table[1:]:
        try:
            x = " ".join([str(j) for j in i[1]])
        except:
            x = "^n"

        try:
            y = " ".join([str(j) for j in i[2]])
        except:
            y = "^prime prime prime"

        try:
            z = "".join([str(j) for j in i[3]])
        except:
            z = "^*n"

        print(f"{i[0]:<10} {x:<10} {y:<10} {z:<10}")
        ed += 1
    return ed


def or_b(cur, ed, end):
    temp = table[cur]

    try:
        table[cur] = [cur, temp[1], temp[2], temp[3].append(cur + 1)]
    except:
        table[cur] = [cur, temp[1], temp[2], [cur + 1]]


def or_a(cur, ed, end):
    temp = table[cur]

    try:
        table[cur] = [cur, temp[1], temp[2].append(cur + 1), temp[3]]
    except:
        table[cur] = [cur, temp[1], [cur + 1], temp[3]]


def and_a(cur, ed=end):
    cur += 1
    temp = table[cur]

    try:
        table[cur] = [cur, temp[1], temp[2].append(cur + 1), temp[3]]
    except:
        table[cur] = [cur, temp[1], [cur + 1], temp[3]]

    try:
        nv = table[cur + 1]
    except:
        table.append([ed + 1])

    ed += 1
    return cur, ed


def and_b(cur, ed, end):
    cur += 1
    temp = table[cur]

    try:
        table[cur] = [cur, temp[1], temp[2], temp[3].append(cur + 1)]
    except:
        table[cur] = [cur, temp[1], temp[2], [cur + 1]]

    try:
        nv = table[cur + 1]
    except:
        table.append([cur + 1])
    ed += 1
    return cur, ed


def star(cur, ed, end, table):
    table.append([ed + 1])
    table.append([ed + 2])
    ed += 2

    for i in range(cur, ed):
        temp = [table[ed - i + cur][0]] + table[ed - i + cur - 1][1:4]

        for j in [1, 2, 3]:
            try:
                temp[j] = [x + 1 for x in table[ed - i + cur - 1][0]]
            except:
                pass

        table[ed - i + cur] = temp

    table[cur] = [cur] + table[cur]

    temp = table[cur]

    try:
        table[cur] = [temp[0], temp[1] + [cur + 1, ed], temp[2], temp[3]]
    except:
        table[cur] = [temp[0], [cur + 1, ed], temp[2], temp[3]]

    temp = table[ed - 1]

    try:
        table[ed - 1] = [temp[0], temp[1] + [cur + 1, ed], temp[2], temp[3]]
    except:
        table[ed - 1] = [temp[0], [cur + 1, ed], temp[2], temp[3]]

    return ed - 1, ed


def mod_table(inp, start, cur, end, table):
    k = 0

    while k < len(inp):
        if inp[k] == "a":
            end = (cur, end)

        elif inp[k] == "b":
            end = (cur, end)

        elif inp[k] == "e":
            end = (cur, end)

        elif inp[k] == ".":
            k += 1

            if inp[k] == "a":
                # k -= 1
                cur, end = and_a(cur, end)

            elif inp[k] == "b":
                cur, end = and_b(cur, end)

            # k -= 1

        elif inp[k] == "(":
            li = ["("]
            i = k

            for j in inp[k + 1:]:
                if j == "(":
                    li.append("(")
                if j == ")":
                    try:
                        del li[-1]
                    except:
                        break

                if len(li) == 0:
                    break

                i += 1

            m = k
            k = i + 1
            cur += 1
            start, cur, end, table = mod_table(
                inp[m + 1:i], start, cur, end, table)

        elif inp[k] == "+":
            k += 1

            if inp[k] == "a":
                or_a(cur, end)  # print("in or_a")

            elif inp[k] == "b":
                or_b(cur, end)  # print("in or_b")

            else:
                print(f"ERROR at {k} Done: {inp[k+1]} Rem: {inp[k+1:]}")

        elif inp[k] == "*":
            # print("in star")
            cur, end = star(cur, end, table)

        elif inp[k] == "":
            li = ["("]

            for i in inp[k+1:]:
                if i == "(":
                    li.append("(")
                if i == ")":
                    try:
                        del li[-1]
                    except:
                        break

                if len(li) == 0:
                    break

            m = k
            k = m + 1

            try:
                if inp[k+1] == "*":
                    cur_ = cur
            except:
                pass

            # print(inp[m+1:k+1])
            start, cur, end, table = mod_table(
                inp[m+1:k+1], start, cur, end, table)

            try:
                if inp[k+1] == "*":
                    cur = cur_
            except:
                pass

        else:
            print(f"error at {k} {inp[k]}")
        k += 1
    return start, cur, end, table


start, cur, end, table = mod_table(inp, start, cur, end, table)
print(table)
