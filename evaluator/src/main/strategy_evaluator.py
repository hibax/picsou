import asyncio

from model.src.main.book.book import Book


class Player(object):
    def __init__(self, stream):
        self.stream = stream
        self.current_pos = 0

    def events(self):
        return (line for line in self.stream)


class Simulator(object):

    def on_event(self, event):
        return event

    def on_action(self, action):
        return action


class StrategyEvaluator(object):

    def __init__(self):
        self.player = Player([('on_mbl', Book()) for _ in range(5)])
        self.simulator = Simulator()
        self.in_queue = None
        self.out_queue = None

    async def pace(self, timestamp):
        await asyncio.sleep(1)

    async def replay_feed(self):
        try:
            for event in self.player.events():
                await self.replay_event(event)
                await self.handle_output()
        except KeyboardInterrupt:
            print("Keyboard interruption in evaluator")

        finally:
            print("Cleaning evaluator")

    async def replay_event(self, event):
        print('replaying:' + str(event))
        await self.pace(event)
        event = self.simulator.on_event(event)
        self.in_queue.put(event)

    async def handle_output(self):
        print('wait output')
        await asyncio.sleep(0.1)
        if self.out_queue.qsize() != 0:
            action = self.out_queue.get()
            self.simulator.on_action(action)
            print('strat action:' + str(action))

    def start_evaluator(self, in_queue, out_queue):
        loop = asyncio.get_event_loop()
        self.in_queue = in_queue
        self.out_queue = out_queue

        print('starting evaluator')

        loop.run_until_complete(self.replay_feed())
        loop.close()

