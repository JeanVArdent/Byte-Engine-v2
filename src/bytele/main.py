import typer
import warnings
from typing import Annotated

import game.config as config

from bytele.__about__ import __version__ as VERSION
from game.common.enums import DebugLevel
from game.engine import Engine
from game.utils.generate_game import generate_new_map
from visualizer.main import ByteVisualiser

from bytele.client_cli import client_app

DEBUG_LEVEL_HELP_MSG = ", ".join([f"{level.value} ({level.name})" for level in list(DebugLevel)])
IRRELEVANT_OPTION_MSG = "Provided {option_name} without {action}."
IRRELEVANT_FLAG_MSG = "Enabled {option_name} without {action}."
GENERATE_MSG = "generating a map"
RUN_MSG = "running a game"
VISUALIZE_MSG = "visualizing a game"


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

@app.command(help="Generate/run/visualize a game. If an option has a flag noted in brackets, the value of that option will not be used unless that flag is used.", no_args_is_help=True)
def game(
    generate: Annotated[bool, typer.Option("-g", "--generate", help="Generate a map (previously generated map will be discarded)")] = False,
    run: Annotated[bool, typer.Option("-r", "--run", help="Run a game (turn logs from previously ran games will be discarded)")] = False,
    visualize: Annotated[bool, typer.Option("-v", "--visualize", help="Visualize the most recently ran game")] = False,
    seed: Annotated[int | None, typer.Option("-s", "--seed", help="[GENERATE] Seed to use when generating a map")] = None,
    debug_level: Annotated[int | None, typer.Option("-d", "--debug-level", help=f"[RUN] {DEBUG_LEVEL_HELP_MSG}")] = None,
    quiet_mode: Annotated[bool, typer.Option("-q", "--quiet", help="[RUN] Runs your bot... quietly :) (turns per second is hidden)")] = False,
    log_dir: Annotated[str | None, typer.Option("-l", "--log-path", help="[VISUALIZE] Path to a directory containing turn logs to visualize")] = None,
    result_screen_duration: Annotated[int | None, typer.Option("--results-duration", help="[VISUALIZE] Sets the time for how long the visualizer will pause on the results screen", min=1)] = None,
    playback_speed: Annotated[float | None, typer.Option("--playback-speed", help="[VISUALIZE] Playback speed of the visualizer (turns per second)", min=1.0)] = None,
    skip_start: Annotated[bool, typer.Option("--skip-start", help="[VISUALIZE] Skips the first screen of the visualizer to make viewing the game faster")] = False,
    fullscreen: Annotated[bool, typer.Option("-f", "--fullscreen", help="[VISUALIZE] Determines whether to display the visualizer in fullscreen or not")] = False,
):
    if generate:
        if seed:
            generate_new_map(seed=seed)
        else:
            generate_new_map()
    else:
        if seed is not None:
            warnings.warn(IRRELEVANT_OPTION_MSG.format(option_name="seed", action=GENERATE_MSG))

    if run:
        if debug_level is not None:
            config.Debug.level = DebugLevel(debug_level)
        Engine(quiet_mode=quiet_mode).loop()
    else:
        if debug_level is not None:
            warnings.warn(IRRELEVANT_OPTION_MSG.format(option_name="debug level", action=RUN_MSG))
        if quiet_mode:
            warnings.warn(IRRELEVANT_FLAG_MSG.format(option_name="quiet mode", action=RUN_MSG))

    if visualize:
        ByteVisualiser(log_dir=log_dir, end_time=(result_screen_duration or 1), skip_start=skip_start, playback_speed=(playback_speed or 1.0), fullscreen=fullscreen).loop()
    else:
        if log_dir is not None:
            warnings.warn(IRRELEVANT_OPTION_MSG.format(option_name="log directory", action=VISUALIZE_MSG))
        if result_screen_duration is not None:
            warnings.warn(IRRELEVANT_OPTION_MSG.format(option_name="result screen duration", action=VISUALIZE_MSG))
        if playback_speed is not None:
            warnings.warn(IRRELEVANT_OPTION_MSG.format(option_name="playback speed", action=VISUALIZE_MSG))
        if skip_start:
            warnings.warn(IRRELEVANT_FLAG_MSG.format(option_name="skip start", action=VISUALIZE_MSG))
        if fullscreen:
            warnings.warn(IRRELEVANT_FLAG_MSG.format(option_name="fullscreen", action=VISUALIZE_MSG))

