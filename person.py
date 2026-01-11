from dataclasses import dataclass


def mydecorate(func):
    def wrapper(*args, **kwargs):
        print("using my decorate")
        return func

    return wrapper


@mydecorate
@dataclass
class person:
    name: str
    age: int


if __name__ == "__main__":
    print("hello")

    student = person("hd", "32")
    print(student)

    print()
