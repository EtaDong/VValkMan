from typing import List, TypeVar, Generic


class Animal:
    pass


class Dog(Animal):
    pass


class Cat(Animal):
    pass


AnimalType = TypeVar("AnimalType", bound=Animal)


class Store(Generic[AnimalType]):
    def __init__(self, stock: List[AnimalType]) -> None:
        self.stock = stock

    def buy(self) -> AnimalType:
        return self.stock.pop()


wang = Store[Dog]([Dog(), Dog()])
li = Store[AnimalType]([Dog(), Cat()])

print(wang.buy())

# a: Animal = wang.buy()
b: Dog = wang.buy()

a2: Animal = li.buy()

c: Cat = li.buy()

##############################################################################################################


from typing import List, Generic, TypeVar


class Animal:
    pass


class Dog(Animal):
    pass


class Cat(Animal):
    pass


AnimalType = TypeVar("AnimalType", bound=Animal)
# AnimalType = TypeVar("AnimalType", bound=Animal, covariant= True)


class Store(Generic[AnimalType]):
    def __init__(self, stock: List[AnimalType]) -> None:
        self.stock = stock

    def buy(self) -> AnimalType:
        print("Sold 1 animal")
        return self.stock.pop()

    # def restore(self, a: AnimalType) -> None:
    # self.stock.append(a)


class Doctor(Generic[AnimalType]):
    def treat(self, a: AnimalType) -> None:
        print(f"treat {a}")


def treat_my_dog(d: Doctor[Dog]) -> None:
    d.treat(Dog())


# def buy_animal(recommend_store: Store[Animal]) -> Animal:
# return recommend_store.buy()

# wang = Store[Dog]([Dog(), Dog()])
# buy_animal(wang)

dog1 = Dog()
drwang = Doctor[Dog]()
treat_my_dog(drwang)


# wang.buy()
