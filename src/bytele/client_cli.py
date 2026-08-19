import json
import typer
from dataclasses import dataclass
from typing import Annotated
from requests.models import HTTPError

from server.client.client import Client, Result
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
    utils = ClientUtils(client_app_state.use_csv)
    try:
        result = utils.get_leaderboard(all, include_alumni, id)
        if result.is_err():
            print(result)
    except HTTPError as e:
        print(f"Error: {json.loads(e.response.content)}")

# NOTE: does anyone use these? if so, is this annoying to them?
@client_app.command("stats", help="View stats for your team", no_args_is_help=True)
def client_stats(
    get_runs_for_submission: Annotated[int | None, typer.Option(help="Submission ID you want to get run IDs for")] = None,
    get_code_for_submission: Annotated[int | None, typer.Option(help="Submission ID you want to get code from")] = None,
    get_details_for_submission: Annotated[int | None, typer.Option(help="Submission ID you want to details of")] = None,
    get_submissions: Annotated[bool, typer.Option("-a", "--all-submissions", help="Get all submission ids for your team")] = False,
):
    utils = ClientUtils(client_app_state.use_csv)
    client = Client(None, utils=utils)

    if not client.verify():
        return

    if get_submissions:
        utils.get_submissions(client.vid)
        return

    if get_runs_for_submission is not None:
        temp: Result = utils.get_runs_for_submission(get_runs_for_submission, client.vid)
        if temp.is_err():
            print(temp.Err)
        return

    if get_code_for_submission is not None:
        temp: Result = utils.get_code_from_submission(get_code_for_submission, client.vid)
        if temp.is_err():
            print(temp.Err)
        return

    if get_details_for_submission is not None:
        temp: Result = utils.get_submission_run_info(get_details_for_submission, client.vid)
        if temp.is_err():
            print(temp.Err)
        return

@client_app.command("register", help="Create a new team and receive a vID")
def client_register():
    utils = ClientUtils(client_app_state.use_csv)
    Client(None, utils=utils).register()

@client_app.command("submit", help="Submit a client for grading")
def client_submit():
    utils = ClientUtils(client_app_state.use_csv)
    Client(None, utils=utils).submit()

