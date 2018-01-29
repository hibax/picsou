import operator
import sys

from executor.src.main.interface.executor import Executor


def start_executor(out_queue):

    executor = Executor()

    try:
        while True:
            action = out_queue.get()

            # print('action: ' + str(action))
            fct = operator.methodcaller(action['type'], action)
            fct(executor)

    except KeyboardInterrupt:
        print("Keyboard interruption in Executor")
    except:
        print("Unexpected error:", sys.exc_info()[0])

    finally:
        print("Cleaning Executor")

