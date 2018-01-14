from multiprocessing import Manager
from multiprocessing.pool import Pool

from engine.src.main.automate import start_engine
from evaluator.src.main.strategy_evaluator import StrategyEvaluator
from model.src.main.book.book import Book


def launch_evaluation():
    manager = Manager()
    strategy_eval = StrategyEvaluator([('on_mbl', Book()) for _ in range(5)])

    in_queue = manager.Queue()
    out_queue = manager.Queue()

    pool = Pool(processes=2)
    results = [pool.apply_async(start_engine, (in_queue, out_queue)),
               pool.apply_async(strategy_eval.start_evaluator, (in_queue, out_queue))]

    for r in results:
        r.get()


def main():
    launch_evaluation()


if __name__ == '__main__':
    main()
