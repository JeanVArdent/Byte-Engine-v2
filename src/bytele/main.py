import json
import sys
import argparse
import typer
from typing import Annotated
from dataclasses import dataclass

import game.config as config

from bytele.__about__ import __version__ as VERSION
from game.common.enums import DebugLevel
from game.engine import Engine
from game.utils.generate_game import generate_new_map
from server.client.client import Client
from visualizer.main import ByteVisualiser

from bytele.client_cli import client_app

DEBUG_LEVEL_HELP_MSG = ", ".join([f"{level.value} ({level.name})" for level in list(DebugLevel)])


app = typer.Typer(
    context_settings={
        "help_option_names": ["-h", "--help"]
    },
    pretty_exceptions_enable=False,
    pretty_exceptions_short=False,
    no_args_is_help=True,
)
app.add_typer(client_app, name="client")

def version_callback(value: bool):
    if value:
        print(f"Byte-le {VERSION}")
        raise typer.Exit()

@app.callback()
def main(version: Annotated[bool | None, typer.Option("--version", help="Print the package version and exit.", is_eager=True, callback=version_callback)] = None):
    pass

@app.command(help="Generate/run/visualize a game", no_args_is_help=True)
def game(
    generate: Annotated[bool, typer.Option("-g", "--generate", help="Generate a map (previously generated map will be discarded)")] = False,
    run: Annotated[bool, typer.Option("-r", "--run", help="Run a game (turn logs from previously ran games will be discarded)")] = False,
    visualize: Annotated[bool, typer.Option("-v", "--visualize", help="Visualize the most recently ran game")] = False,
    seed: Annotated[int | None, typer.Option("-s", "--seed", help="Seed to use when generating a map")] = None,
    debug_level: Annotated[int, typer.Option("-d", "--debug-level", help=f"{DEBUG_LEVEL_HELP_MSG}")] = 1,
    quiet_mode: Annotated[bool, typer.Option("-q", "--quiet", help="Runs your bot... quietly :) (turns per second is hidden)")] = False,
    log_dir: Annotated[str | None, typer.Option("-l", "--log-path", help="Path to a directory containing turn logs to visualize")] = None,
    result_screen_duration: Annotated[int, typer.Option("--results-duration", help="Sets the time for how long the visualizer will pause on the results screen", min=1)] = 1,
    skip_start: Annotated[bool, typer.Option("--skip-start", help="Skips the first screen of the visualizer to make viewing the game faster")] = False,
    playback_speed: Annotated[float, typer.Option("--playback-speed", help="Playback speed of the visualizer (turns per second)", min=0.1)] = 1.0,
    fullscreen: Annotated[bool, typer.Option("-f", "--fullscreen", help="Determines whether to display the visualizer in fullscreen or not")] = False,
):
    if generate:
        if seed:
            generate_new_map(seed=seed)
        else:
            generate_new_map()

    if run:
        config.Debug.level = DebugLevel(debug_level)
        Engine(quiet_mode=quiet_mode).loop()

    if visualize:
        ByteVisualiser(log_dir=log_dir, end_time=result_screen_duration, skip_start=skip_start, playback_speed=playback_speed, fullscreen=fullscreen).loop()

