def jumping_bean():
    print("--- 第一次起跳 ---")
    received = yield "我是第一个值"

    print(f"--- 重新落地，收到外界给的: {received} ---")
    yield "我是第二个值"


# 1. 拿到蹦床（生成器对象）
bean = jumping_bean()

# 2. 第一次跳：代码跑到第一个 yield，然后弹出
val1 = next(bean)
print(f"外面拿到: {val1}")

# 3. 第二次跳：把 '苹果' 送进去，代码从第一个 yield 之后继续
val2 = bean.send("苹果")
print(f"外面拿到: {val2}")
