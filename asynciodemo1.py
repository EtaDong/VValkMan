from distutils.log import debug
import asyncio


async def coro_c():
    print("Breakpoints")


async def coro_a():
    print("I am coro_a(). Hi!")
    await asyncio.create_task(coro_c())
    # await coro_c()


async def coro_b():
    print("I am coro_b(). I sure hope no one hogs the event loop...")


# await asyncio.sleep(1)


async def base_coroutine_demo():
    task_b = asyncio.create_task(coro_b())
    num_repeats = 3
    for _ in range(num_repeats):
        await coro_a()
    #   await asyncio.create_task(coro_a())
    await task_b


class Rock:
    def __await__(self):
        value_sent_in = yield 7
        print(f"Rock.__await__ resuming with value: {value_sent_in}.")
        return value_sent_in


async def main():
    print("Beginning coroutine main().")
    rock = Rock()
    print("Awaiting rock...")
    value_from_rock = await rock
    print(f"Coroutine received value: {value_from_rock} from rock.")
    return 23


coroutine = main()
intermediate_result = coroutine.send(None)
print(f"Coroutine paused and returned intermediate value: {intermediate_result}.")

print(f"Resuming coroutine and sending in value: 42.")
try:
    coroutine.send(42)
except StopIteration as e:
    returned_value = e.value
print(f"Coroutine main() finished and provided value: {returned_value}.")


# asyncio.run(base_coroutine_demo(), debug=True)

# event_loop = asyncio.new_event_loop()
# event_loop.run_forever()
