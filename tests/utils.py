"""
This file is used as utilities to help simplify unit tests. The spell_check() method will take in a given exception
string message and expected string message to compare the two. If a discrepancy is not found, the spell check() method
will return true. Otherwise, it will print what the discrepancy is and return false.
"""


def spell_check(str1: str, str2: str, printing: bool) -> bool:
    """
    This will check the two given strings for any mismatching information.
    :param printing:
    :param str1:
    :param str2:
    :return: true or false
    """

    # Checks if str1 and str2's length are not equal
    if len(str1) != len(str2):
        if printing:
            print(f'\nThe length of "{str1}" and "{str2}" aren\'t equal')
        return False

    # Split the two Strings into lists divided by spaces
    temp1: list[str] = str1.split()
    temp2: list[str] = str2.split()

    # a list to be returned later
    result: list[tuple[str, str]] = []

    # Collects any discrepancies
    for i in range(len(temp1)):
        if temp1[i] != temp2[i]:
            result.append((temp1[i], temp2[i]))

    if len(result) == 0:
        return True

    # Prevents extra text from printing out
    if printing:
        space: str = '\n'
        # Print a message to show the discrepancies that were found in the "x | y" format
        print(f'\nDiscrepancies were found between "{str1}" and "{str2}". The following discrepancies are below in the '
              f'format "original | expected."\n')

        [print(pair[0] + " | " + pair[1] + space) for pair in result]

    return False
