class Config:
    """
    Config
    ------
        The Server Config class is responsible for setting up the runners for the server.
    -----
    Number Of Games Against Same Team
    +++++++++++++++++++++++++++++++++
        The Number Of Games Against Same Team is an int representing how many runs should be repeated. It is worth
        noting that this should be 1 if the development team has ensured that randomness is seeded, ensuring that
        two games with the same seed play out the same way. Competitor randomness is their own liability and not
        the development team's responsibility.
    -----
    Sleep Time Between Runs
    +++++++++++++++++++++++
        The Sleep Time Between Runs is an int representing the number of seconds between each run of the client runner.
        Each time the client runner is run, it will generate an entire tournament. The run time of the client runner is
        not factored into this time.
    -----
    End DateTime
    ++++++++++++
        The End DateTime is an ISO formatted string representing the end of the competition. This will need to be
        changed for every competition. Ex. 'YYYY-mm-dd HH:MM', like '2030-01-01 00:00'
    -----
    Sleep Time Between Vis
    ++++++++++++++++++++++
        The Sleep Time Between Vis is an int representing the number of seconds between each run of the visualizer.
        Each time the visualizer is run, it will visualize the best runs for each team of the tournament. The run time
        of the visualizer is not factored into this time. If the visualizer isn't running on the server, increase this
        parameter as a potential solution.
    -----
    """
    __NUMBER_OF_GAMES_AGAINST_SAME_TEAM: int = 1
    __SLEEP_TIME_SECONDS_BETWEEN_RUNS: int = 150
    __END_DATETIME: str = "2030-01-01 00:00"  # Adjust this for every competition!!!!!
    __SLEEP_TIME_SECONDS_BETWEEN_VIS: int = 10

    @property
    def NUMBER_OF_GAMES_AGAINST_SAME_TEAM(self) -> int:
        """
        The Number Of Games Against Same Team is an int representing how many runs should be repeated. It is worth
        noting that this should be 1 if the development team has ensured that randomness is seeded, ensuring that
        two games with the same seed play out the same way. Competitor randomness is their own liability and not
        the development team's responsibility.
        :return: int
        """
        return self.__NUMBER_OF_GAMES_AGAINST_SAME_TEAM

    @property
    def SLEEP_TIME_SECONDS_BETWEEN_RUNS(self) -> int:
        """
        The Sleep Time Between Runs is an int representing the number of seconds between each run of the client runner.
        Each time the client runner is run, it will generate an entire tournament. The run time of the client runner is
        not factored into this time.
        :return: int
        """
        return self.__SLEEP_TIME_SECONDS_BETWEEN_RUNS

    @property
    def END_DATETIME(self) -> str:
        """
        The End DateTime is an ISO formatted string representing the end of the competition. This will need to be
        changed for every competition.
        :return: str
        """
        return self.__END_DATETIME

    @property
    def SLEEP_TIME_SECONDS_BETWEEN_VIS(self) -> int:
        """
        The Sleep Time Between Vis is an int representing the number of seconds between each run of the visualizer.
        Each time the visualizer is run, it will visualize the best runs for each team of the tournament. The run time
        of the visualizer is not factored into this time. If the visualizer isn't running on the server, increase this
        parameter as a potential solution.
        :return: int
        """
        return self.__SLEEP_TIME_SECONDS_BETWEEN_VIS
