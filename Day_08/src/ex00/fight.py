import asyncio
from concurrent.futures import ProcessPoolExecutor

from enum import Enum, auto
from random import choice, random

import random


class Action(Enum):
    HIGHKICK = auto()
    LOWKICK = auto()
    HIGHBLOCK = auto()
    LOWBLOCK = auto()


class Agent:

    def __aiter__(self, health=5):
        self.health = health
        self.actions = list(Action)
        return self

    async def __anext__(self):
        slp=random.uniform(0.01,0.03)
        await asyncio.sleep(slp)
        return choice(self.actions)

def print_move(agent,agent_move,neo_move: Action,agent_number: int = 0):
    print(
        f"Agent{' ' + str(agent_number) if agent_number > 0 else ''}"
        + f": {agent_move}, Neo: {neo_move}, Agent Health: {agent.health}"
    )


async def fight():
    agent = Agent()
    async for action in agent:
        neo = Action.LOWKICK if action == Action.HIGHBLOCK \
            else Action.HIGHKICK if action == Action.LOWBLOCK \
            else Action.HIGHBLOCK if action == Action.HIGHBLOCK \
            else Action.LOWBLOCK
        if neo == Action.LOWKICK or neo == Action.HIGHKICK:
            agent.health -= 1
        print_move(agent, action, neo)
        if agent.health <= 0:
            break

    print("Neo wins!")


async def fight2(agent, i):
    async for action in agent:
        neo = Action.LOWKICK if action == Action.HIGHBLOCK \
            else Action.HIGHKICK if action == Action.LOWBLOCK \
            else Action.HIGHBLOCK if action == Action.HIGHBLOCK \
            else Action.LOWBLOCK
        if neo == Action.LOWKICK or neo == Action.HIGHKICK:
            agent.health -= 1

        print_move(agent, action, neo,i+1)
        if agent.health <= 0:
            break


async def fightmany(n):
    agents = [Agent() for _ in range(n)]
    tasks = [fight2(a, i) for i, a in enumerate(agents)]
    await asyncio.gather(*tasks)
    print("Neo wins!")

asyncio.run(fightmany(3))
