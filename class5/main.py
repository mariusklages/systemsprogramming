import time
from multiprocessing import Process, Value

def do_something(x, name=''):
    while True:
        with x.get_lock():
            x.value += 1
            print("hello", name, x.value)
        time.sleep(1) # not necessarily needed


if __name__ == "__main__":
    x = Value('i', 0)
    Process(target=do_something, args=(x, 'first')).start()
    Process(target=do_something, args=(x, 'second')).start()
