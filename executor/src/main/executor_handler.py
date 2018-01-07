from executor.src.main.interface.executor import Executor


def start_executor(out_queue):

    executor = Executor()

    try:
        while True:
            msg, action = out_queue.get()

            executor.execute(action)

            # print(str(msg))

    except KeyboardInterrupt:
        print("Keyboard interruption in Executor")

    finally:
        print("Cleaning Executor")

