import random
import time


def emit_gel(step):
    pressure = random.randint(50, 100)
    while True:
        sign = yield pressure
        time.sleep(0.1)
        this_step = random.randint(0, step)
        pressure += sign * this_step


def valve(gen):
    sign = 1
    next(gen)
    while True:
        pressure = gen.send(sign)
        print(f'pressure: {pressure}')
        if pressure > 80 or pressure < 20:
            sign = -sign
            print('sign changed')
            # gen.send(sign)
        if pressure > 90 or pressure < 10:
            gen.close()
            print('valve closed')
            break


if __name__ == '__main__':
    valve(emit_gel(random.randint(3, 15)))
