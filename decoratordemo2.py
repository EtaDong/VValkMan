import time

def timing(func):
    # def warpper(*args, **kwargs):
    def warpper(*args, **kwargs):
        star_time = time.time()
        result =  func(*args, **kwargs)
        print(f"total time : {time.time() - star_time} ")
        return result
    return warpper

@timing
def hello():
    print("enter hello")
    

hello = timing(hello)
print(hello)
hello()

@timing
def greet(name):
    print(f"hello {name}")


greet("dong")