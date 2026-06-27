import json
import os
import typer
from dataclasses import dataclass
from typing import Annotated
from requests.models import HTTPError

from server.client.client import Client
from server.client.client_utils import ClientUtils


@dataclass
class ClientAppState:
    use_csv: bool = False


client_app = typer.Typer(
    context_settings={
        "help_option_names": ["-h", "--help"]
    },
    pretty_exceptions_enable=False,
    pretty_exceptions_short=False,
    no_args_is_help=True,
    help="Interact with the Byte-le Royale server"
)

client_app_state = ClientAppState()


@client_app.callback()
def client_main(
    use_csv: Annotated[bool, typer.Option("--csv", help="Output results in CSV format instead of an ASCII table")] = False,
):
    client_app_state.use_csv = use_csv


@client_app.command("leaderboard", help="Fetch a list of teams and their current standings")
def client_leaderboard(
    id: Annotated[int | None, typer.Argument(help="The leaderboard_id you want to get")] = None,
    all: Annotated[bool, typer.Option("-a", "--all", help='Gets all available leaderboards')] = False,
    include_alumni: Annotated[bool, typer.Option("--include-ineligible", help="Include teams not eligible for prizes in the leaderboard")] = False,
):
    try:
        result = ClientUtils(client_app_state.use_csv).get_leaderboard(all, include_alumni, id)
        if result.is_err():
            print(result)
    except HTTPError as e:
        print(f"Error: {json.loads(e.response.content)}")

@client_app.command("register", help="Create a new team and receive a vID")
def client_register():
    utils = ClientUtils(client_app_state.use_csv)
    Client(None, utils=utils).register()
