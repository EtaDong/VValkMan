def walrus_operator_demo1(l: list[int] | None = None):
    # l = [1, 2, 3]
    # length = len(l)
    if l is None:
        l = [1, 2, 3]
    if (length := len(l)) > 0:
        return f"list is not empty, its size: {length}"
    return "empty"


def walrus_operator_demo2():
    while (cmd := input("Enter command: ")) != "exit":
        print(f"You entered: {cmd}")


from typing import List

Num = int | float

num_list: List[Num] = [1, 2, 3, 4, 5]


def print_num_list(l: List[Num]) -> None:
    for n in l:
        print(n)


print_num_list(num_list)
