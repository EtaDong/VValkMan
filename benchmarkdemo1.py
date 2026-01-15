import timeit

# 准备一个列表
data = list(range(1000))

# 测试 tuple()
time_func = timeit.timeit("tuple(data)", globals={"data": data}, number=1000000)

# 测试 (*data,)
time_unpack = timeit.timeit("(*data,)", globals={"data": data}, number=1000000)

print(f"tuple()  耗时: {time_func:.4f}s")
print(f"(*data,) 耗时: {time_unpack:.4f}s")