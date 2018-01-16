import argparse
from multiprocessing import Manager
from multiprocessing.pool import Pool

from feedhandler.src.main.feedhandler import start_feed
from engine.src.main.automate import start_engine
from executor.src.main.executor_handler import start_executor
from feedhandler.src.main.scheduled_task import create_repeated_timer


def send_info_from_queues(queues):
    for queue in queues:
        print('size: {}\n inputs: {}\noutputs: {}'.format(queue.qsize(), queue.nb_in, queue.nb_out))


def monitor(queues):
    create_repeated_timer(send_info_from_queues, 1, queues).start()


def test_queue_and_thread():
    strategy_name = parse_args()
    manager = Manager()

    in_queue = manager.Queue()
    out_queue = manager.Queue()

    # monitor([in_queue, out_queue])

    pool = Pool(processes=3)

    results = [pool.apply_async(start_engine, (in_queue, out_queue, strategy_name)),
               pool.apply_async(start_feed, (in_queue,)),
               pool.apply_async(start_executor, (out_queue,))]

    try:
        for r in results:
            r.get()

    except KeyboardInterrupt:
        print("Keybord interruption in main thread")

    finally:
        print("Cleaning main thread")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--strategy", help="use this strategy")
    args = parser.parse_args()

    strategy = 'default'
    if args.strategy:
        strategy = args.strategy

    return strategy


def main():
    test_queue_and_thread()


if __name__ == '__main__':
    main()
