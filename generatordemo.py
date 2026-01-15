def myrang(n):
    print("enter myrange")
    i = 0
    while i < n:
        value = yield i
        print(value)
        i += 1

result = myrang(5)
it = result.__iter__()
print(it.__iter__())
print(it.__next__())
print(result.send("hello world"))
