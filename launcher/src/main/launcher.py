from multiprocessing import Manager
from multiprocessing.pool import Pool

from feedhandler.src.main.feedhandler import start_feed
from engine.src.main.automate import start_engine
from trader.src.main.executor import start_executor
from feedhandler.src.main.scheduled_task import create_repeated_timer


def send_info_from_queues(queues):
    for queue in queues:
        print('size: {}\n inputs: {}\noutputs: {}'.format(queue.qsize(), queue.nb_in, queue.nb_out))


def monitor(queues):
    create_repeated_timer(send_info_from_queues, 1, queues).start()


def test_queue_and_thread():
    manager = Manager()

    in_queue = manager.Queue()
    out_queue = manager.Queue()

    # monitor([in_queue, out_queue])

    pool = Pool(processes=3)
    results = [pool.apply_async(start_engine, (in_queue, out_queue)),
               pool.apply_async(start_feed, (in_queue,)),
               pool.apply_async(start_executor, (out_queue,))]

    for r in results:
        r.get()


def main():
    test_queue_and_thread()


if __name__ == '__main__':
    main()
