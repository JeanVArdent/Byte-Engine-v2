import sqlite3
import pandas as pd


def read_table(table: str):
    """
    Returns the entire table given the table's name.
    :param table:
    """
    with sqlite3.connect('byte_server.db') as db:
        return pd.read_sql_query(f'SELECT * FROM {table}', db)


def tournaments():
    """
    Returns Tournaments table.
    """
    return read_table('tournament')


def teams():
    """
    Returns Teams table.
    """
    return read_table('team')


def runs():
    """
    Returns Run table.
    """
    return read_table('run')


def turns():
    """
    Returns Turns table.
    """
    return read_table('turn')


def submissions():
    """
    Returns Submissions table.
    """
    return read_table('submission')


def universities():
    """
    Returns Universities table.
    """
    return read_table('university')


def team_types():
    """
    Returns Team Types table.
    """
    return read_table('team_type')


def submission_run_infos():
    """
    Returns Run table.
    """
    return read_table('submission_run_info')
