#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import sys
from dotenv import load_dotenv
from pathlib import Path

ENV_FILE = Path("/.env")


async def restart(proc_queue):
    proc = await queue.get()
    load_dotenv(dotenv_path=ENV_FILE)
    proc.send_signal(signal.SIGTERM)


async def run_command(proc_queue, *args):
    """Creates a child process from the args passed in from shell. Restarts until cancelled during shutdown."""
    while True:
        proc = await asyncio.create_subprocess_exec(*args)
        workflow = await queue.put_nowait(proc)
        await process.wait()


async def shutdown():
    """Cancel all running tasks in anticipation of exiting."""
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    [task.cancel() for task in tasks]  # pylint: disable=expression-not-assigned

    logging.info('Canceling outstanding tasks')
    await asyncio.gather(*tasks)


def main():
    """Entrypoint for the entrypoint."""
    loop = asyncio.get_event_loop()
    load_dotenv(dotenv_path=ENV_FILE)
    proc_queue = asyncio.Queue()

    # When receiving SIGHUP, we want to reload .env file and restart child process.
    loop.add_signal_handler(signal.SIGHUP, lambda: asyncio.create_task(restart(proc_queue)))

    # SIGTERM and SIGINT should cancel all tasks and exit.
    for s in {signal.SIGTERM, signal.SIGINT}:  # pylint: disable=no-member
        # logging.info(f'adding handlers for {s.name}')
        loop.add_signal_handler(s, lambda: asyncio.create_task(shutdown()))


    # run_command will continually restart the child proc until it is cancelled.
    try:
        asyncio.create_task(run_command(proc_queue, sys.argv[1:]))
        loop.run_forever()
    finally:
        print('Cleaning up')
        loop.close()
