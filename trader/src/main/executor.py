
def start_executor(out_queue):
    while True:
        msg = out_queue.get()
        # executor code goes here

        print(str(msg))
