
def start_executor(out_queue):

    try:
        while True:
            msg, action = out_queue.get()
            # executor code goes here
            print(str(msg))

    except KeyboardInterrupt:
        print("Keyboard interruption in Executor")

    finally:
        print("Cleaning Executor")

