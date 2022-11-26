# from typing import Mapping, MutableMapping, Sequence, Iterable

import json
from typing import List, Tuple
import requests as req

SOTA_API_ROOT = "https://api2.sota.org.uk/"
ASSOC_CHECK_LIST = ["W4V", "W7V"]


def get_name(assoc: str, summit: str) -> str:
    """Get the name of a summit

    Args:
        assoc (str): the association code
        summit (str): the summit code

    Returns:
        str: the name of the summit
    """
    resp = req.get(f"{SOTA_API_ROOT}api/summits/{assoc}/{summit}")

    if resp.status_code == 200:
        summit_info = json.loads(resp.text)
        return summit_info["name"]

    return ""


def is_restricted(assoc: str, summit: str, check_assocs: List[str]) -> bool:
    """Return True if this summit has any restrictions

    Args:
        assoc (str): the association code
        summit (str): the summits code
        check_assocs (List[str]): the list of association codes to check for restrictions

    Returns:
        bool: True if the summit has any restrictions
    """
    if assoc in check_assocs:
        resp = req.get(f"{SOTA_API_ROOT}api/summits/{assoc}/{summit}")

        if resp.status_code == 200:
            summit_info = json.loads(resp.text)
            return len(summit_info["restrictionList"]) > 0

    return False


def get_spots(hours: int) -> List[Tuple[str, str, str, str]]:
    """Get a list of SOTA spots

    Args:
        hours (int): restrict the list to this age in hours

    Returns:
        List[Tuple[str, str, str, str]]: the list of spots, giving association code, summit code, timestamp and frequencies
    """
    resp = req.get(f"{SOTA_API_ROOT}api/spots/-{hours}/all")

    if resp.status_code == 200:
        spots = json.loads(resp.text)
        return [
            (
                spot["associationCode"],
                spot["summitCode"],
                spot["timeStamp"],
                spot["frequency"],
            )
            for spot in spots
        ]

    return []


def get_restricted_spots(hours: int, check_assocs: List[str]) -> List[str]:
    """Get a list of SOTA spots for which there are restrictions

    Args:
        hours (int): restrict the list to this age in hours
        check_assocs (List[str]): the list of association codes to check for restrictions

    Returns:
        List[str]: the list of spots, each formatted as a string
    """
    spots = get_spots(hours)

    restricted = filter(
        lambda spot: is_restricted(spot[0], spot[1], check_assocs), spots
    )
    return [
        f'{assoc}/{summit} "{get_name(assoc,summit)}" at {timestamp}, frequencies "{frequency}"'
        for (assoc, summit, timestamp, frequency) in restricted
    ]


def get_alerts() -> List[Tuple[str, str, str, str]]:
    """Get a list of SOTA alerts

    Returns:
        List[Tuple[str, str, str, str]]: the list of alerts, giving association code, summit code, timestamp and frequencies
    """
    resp = req.get(f"{SOTA_API_ROOT}api/alerts")

    if resp.status_code == 200:
        alerts = json.loads(resp.text)
        return [
            (
                alert["associationCode"],
                alert["summitCode"],
                alert["timeStamp"],
                alert["frequency"],
            )
            for alert in alerts
        ]

    return []


def get_restricted_alerts(check_assocs: List[str]) -> List[str]:
    """Get a list of SOTA alerts for which there are restrictions

    Args:
        check_assocs (List[str]): the list of association codes to check for restrictions

    Returns:
        List[str]: the list of alerts, each formatted as a string
    """
    alerts = get_alerts()

    restricted = filter(
        lambda alert: is_restricted(alert[0], alert[1], check_assocs), alerts
    )
    return [
        f'{assoc}/{summit} "{get_name(assoc,summit)}" at {timestamp}, frequencies "{frequency}"'
        for (assoc, summit, timestamp, frequency) in restricted
    ]


if __name__ == "__main__":
    """Print any spots in the last hour and any alerts for which there are restrictions."""
    print("List of restricted spots in last hour:")
    spots = get_restricted_spots(1, ASSOC_CHECK_LIST)
    if len(spots) == 0:
        print("None")
    else:
        for spot in spots:
            print(spot)
    print()
    print("List of restricted alerts:")
    alerts = get_restricted_alerts(ASSOC_CHECK_LIST)
    if len(alerts) == 0:
        print("None")
    else:
        for alert in alerts:
            print(alert)
