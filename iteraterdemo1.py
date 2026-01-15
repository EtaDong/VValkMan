lst = [x**2 for x in range(0, 10, 2) if x != 4]
d1 = tuple(enumerate(dir(lst)))
d2 = (*enumerate(dir(lst)),)


# for index, name in d1:
#     if index < 5:  # 仅打印前5个
#         print(f"ID: {index}, Method: {name}")

def check_box(box):
    print(f"I received ONE box with {len(box)} items.")

my_tuple = (1, 2, 3)
check_box(my_tuple) # 传进去的是一个整体

# *args 就像是一双能够“接住所有散落零件”的手
def receive_items(*args):
    # args 在这里又把零件重新打包成了一个临时元组供你遍历
    print(f"I caught {len(args)} individual items.")

my_tuple = (1, 2, 3)
receive_items(*my_tuple) # 传进去的是 1, 然后是 2, 然后是 3

def super_function(*args, **kwargs): 
    print(f"Positional parts (Tuple): {args}")
    print(f"Keyword parts (Dict): {kwargs}")

super_function(1, 2, name="Alice", role="Admin")