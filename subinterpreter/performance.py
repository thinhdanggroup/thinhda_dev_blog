import test.support
import threading
import time
import _xxsubinterpreters as subinterpreters
from textwrap import dedent


def thread_function(interpreter_id: int = 0):
    subinterpreters.run_string(interpreter_id, dedent("""
total = 0
for i in range(10 ** 7):
    total += i
"""))


def thread_function_normal():
    total = 0
    for i in range(10 ** 7):
        total += i


def run_in_threads(total: int = 10):
    sub_interpreters = []
    list_thread = []
    for i in range(total):
        sub_interpreters.append(subinterpreters.create())
        t = threading.Thread(target=thread_function, args=(sub_interpreters[i],))
        list_thread.append(t)

    start = time.time()
    for i in range(total):
        list_thread[i].start()
        list_thread.append(list_thread[i])

    for t in list_thread:
        t.join()

    print(f"Test subinterpreter has total execution time {time.time() - start}")
    for i in range(total):
        subinterpreters.destroy(sub_interpreters[i])


def run_in_threads_no_sub(total: int = 10):
    list_thread = []
    for i in range(total):
        t = threading.Thread(target=thread_function_normal, args=(i,))
        list_thread.append(t)

    start = time.time()
    for i in range(total):
        list_thread[i].start()
        list_thread.append(list_thread[i])

    for t in list_thread:
        t.join()
    print(f"Test no_subinterpreter has total execution time {time.time() - start}")


def main():
    run_in_threads()
    run_in_threads_no_sub()


if __name__ == '__main__':
    main()
