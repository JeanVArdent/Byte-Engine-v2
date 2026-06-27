from dataclasses import dataclass
import json
import sys
import argparse
from typing import Annotated
import typer

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
def main(version: Annotated[bool | None, typer.Option("--version", is_eager=True, callback=version_callback)] = None):
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

# @app.command(help="Register a new team")
# def register(
#     team_name: Annotated[str, typer.Option(help="Your desired team name", prompt=True)],
#     team_type: Annotated[e_TeamType, typer.Option(help="Your team type", prompt=True)],
#     university: Annotated[e_University, typer.Option(help="Your university", prompt=True)],
# ):
#     Client(argparse.ArgumentParser()).register(team_name, team_type, university)

def old_main():
    # Setup Primary Parser
    par = argparse.ArgumentParser()

    # Create Subparsers
    spar = par.add_subparsers(title="Commands", dest="command")

    # Generate Subparser
    gen_subpar = spar.add_parser('generate', aliases=['g'], help='Generates a new random game map')

    gen_subpar.add_argument('-seed', '-s', action='store', type=int, nargs='?', dest='seed',
                            help='Allows you to pass a seed into the generate function.')

    # Run Subparser and optionals
    run_subpar = spar.add_parser('run', aliases=['r'],
                                 help='Runs your bot against the last generated map! "r -h" shows more options')

    run_subpar.add_argument('-debug', '-d', action='store', type=int, nargs='?', const=-1,
                            default=None, dest='debug', help='Allows for debugging when running your code')

    run_subpar.add_argument('-quiet', '-q', action='store_true', default=False,
                            dest='q_bool', help='Runs your AI... quietly :) (the runs per second won\'t be displayed)')

    # Visualizer Subparser and optionals
    vis_subpar = spar.add_parser('visualize', aliases=['v'],
                                 help='Runs the visualizer! "v -h" shows more options')

    # might not be needed
    vis_subpar.add_argument('-log', action='store', type=str, nargs='?',
                            const=-1, default=None, dest="logpath", help="Specify a log path")

    # get user input for parameters for using the ByteVisualizer
    vis_subpar.add_argument('-end_time', action='store', default=-1, type=int, nargs='?', dest='end_time',
                            help='Sets the time for how long the visualizer will pause on the results screen')

    vis_subpar.add_argument('-skip_start', action='store_true', default=False, dest='skip_start',
                            help='Skips the first screen of the visualizer to make viewing the game faster')

    vis_subpar.add_argument('-playback_speed', action='store', default=1.0, type=float, nargs='?',
                            dest='playback_speed', help='Adjusts the playback speed of the visualizer')

    vis_subpar.add_argument('-fullscreen', action='store_true', default=False,
                            dest='fullscreen', help='Determines whether to display the visualizer in fullscreen or not')

    all_subpar = spar.add_parser('gen,run,vis', aliases=['grv'],
                                 help='Generate, Run, Visualize! "grv -h" shows more options')

    gr_subpar = spar.add_parser('gen,run', aliases=['gr'], help='Generates and runs the game without '
                                                                'visualization. Can be helpful for testing!')

    # Version Subparser
    update_subpar = spar.add_parser('version', aliases=['ver'], help='Prints the current version of the '
                                                                     'launcher')

    # Client Parser
    client_parser = spar.add_parser('client', aliases=['s', 'c'], help='Run the client for the Byte-le Royale '
                                                                       'server')

    client_parser.add_argument('-csv',
                               help='Use csv output instead of the ascii table output (if applicable)',
                               default=False, action='store_true')

    # subparser group
    client_sub_group = client_parser.add_subparsers(title='client_subparsers', dest='subparse')

    leaderboard_subpar = client_sub_group.add_parser('leaderboard', aliases=['l'],
                                                     help='Commands relating to the leaderboard')

    leaderboard_subpar.add_argument('-all', help='Gets all available leaderboards',
                                    default=False, action='store_true')

    leaderboard_subpar.add_argument('-include_alumni', help='Include alumni in the leaderboard',
                                    default=False, action='store_true')

    leaderboard_subpar.add_argument('-id', action='store', type=int, dest='id',
                                    help='pass the leaderboard_id you want to get')

    # Stats subgroup

    # ALL OF THESE NEED TO BE TESTED
    stats = client_sub_group.add_parser('stats', aliases=['s'], help='View stats for your team')

    stats.add_argument('-runs_for_submission', action='store', type=int,
                       default=-1, dest='runs_for_submission',
                        help='Pass the submission_id you want to get run ids for')

    stats.add_argument('-get_submissions', action='store_true', default=False,
                       dest='get_submissions', help='Get all submission ids for your team')

    stats.add_argument('-get_code_for_submission', action='store', type=int, default=-1,
                       dest='get_code_for_submission', help='Get the code file for a given submission')

    stats.add_argument('-get_details_for_submission', action='store', type=int, default=-1,
                       dest='get_submission_run_info', help='Get the details for a given submission')

    client_parser.add_argument('-register', action='store_true', default=False, dest='register',
                        help='Create a new team and return a vID')

    client_parser.add_argument('-submit', action='store_true', default=False,
                               dest='submit', help='Submit a client for grading')

    # Parse Command .,mnb vc
    par_args = par.parse_args()

    # Main Action variable
    action = par_args.command

    # Generate game options
    if action in ['generate', 'g']:
        # a random seed is already generated in the method by default
        generate(par_args.seed) if par_args.seed else generate()

    # Run game options
    elif action in ['run', 'r']:
        # Additional args
        quiet = False

        if par_args.debug is not None:
            if par_args.debug >= 0:
                game.config.Debug.level = par_args.debug
            else:
                print('Valid debug input not found, using default value')

        if par_args.q_bool:
            quiet = True

        engine = Engine(quiet)
        engine.loop()

    # Run the visualizer
    elif action in ['visualize', 'v']:
        visualiser = ByteVisualiser(end_time=par_args.end_time, skip_start=par_args.skip_start,
                                    playback_speed=par_args.playback_speed, fullscreen=par_args.fullscreen,
                                    log_dir=par_args.logpath)
        visualiser.loop()

    elif action in ['gen,run', 'gr']:
        generate()
        engine = Engine(False)
        engine.loop()

    elif action in ['gen,run,vis', 'grv']:
        generate()
        engine = Engine(False)
        engine.loop()
        visualiser = ByteVisualiser()
        visualiser.loop()

    elif action in ['version', 'ver']:
        print(VERSION, end="")

    # Boot up the server client
    elif action in ['client', 'c']:
        cl = Client(par_args)

    # Print help if no arguments are passed
    if len(sys.argv) == 1:
        print("\nLooks like you didn't tell the launcher what to do!"
              + "\nHere's the basic commands in case you've forgotten.\n")
        par.print_help()

if __name__ == '__main__':
    old_main()
