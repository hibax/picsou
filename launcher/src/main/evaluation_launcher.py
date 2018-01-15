from multiprocessing import Manager
from multiprocessing.pool import Pool
import argparse
from pathlib import Path

from engine.src.main.automate import start_engine
from evaluator.src.main.strategy_evaluator import StrategyEvaluator


def launch_evaluation():
    record_path, strategy_name = parse_args()

    manager = Manager()
    strategy_eval = StrategyEvaluator(record_path)

    in_queue = manager.Queue()
    out_queue = manager.Queue()

    pool = Pool(processes=2)
    results = [pool.apply_async(strategy_eval.start_evaluator, (in_queue, out_queue)),
               pool.apply_async(start_engine, (in_queue, out_queue, strategy_name))]

    for r in results:
        r.get()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("record", help="evaluate by replaying this recorded file")
    parser.add_argument("-s", "--strategy", help="evaluate this strategy")
    args = parser.parse_args()

    record_file = Path(args.record)
    if record_file.is_file():
        record_file = record_file.resolve()
    else:
        raise FileNotFoundError('Cannot find a record file for "' + args.record + '"')

    strategy = 'default'
    if args.strategy:
        strategy = args.strategy

    return record_file, strategy


def main():
    launch_evaluation()


if __name__ == '__main__':
    main()
