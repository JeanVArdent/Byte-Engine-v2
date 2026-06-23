import os
from pathlib import Path
import game.config as gc
import json


def logs_to_dict(log_dir: str | None) -> dict:
    """
    Takes the given log directory and puts them into a dictionary.
    Defaults to the logs directory specified in the game config file if none specified.
    :param log_dir: The path to the log directory as a str or None
    :return: dict of the turn logs using their turn as a key. ex. 0001
    """
    temp: dict = {}
    for file in Path(gc.LOGS_DIR if log_dir is None else log_dir).glob('*.json'):
        with open(file, 'r') as f:
            temp[file.stem] = json.load(f)
    return temp
