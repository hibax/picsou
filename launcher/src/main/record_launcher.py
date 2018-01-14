from multiprocessing import Manager
from multiprocessing.pool import Pool

from engine.src.main.automate import start_recorder
from feedhandler.src.main.feedhandler import start_feed


def launch_record():
    manager = Manager()

    in_queue = manager.Queue()

    pool = Pool(processes=2)

    results = [pool.apply_async(start_recorder, (in_queue,)),
               pool.apply_async(start_feed, (in_queue,))]

    try:
        for r in results:
            r.get()

    except KeyboardInterrupt:
        print("Keybord interruption in main thread")

    finally:
        print("Cleaning main thread")


def main():
    launch_record()


if __name__ == '__main__':
    main()
