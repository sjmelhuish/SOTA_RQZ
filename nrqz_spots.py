# from typing import Mapping, MutableMapping, Sequence, Iterable

import json
from typing import List
from dataclasses import dataclass
import requests as req

SOTA_API_ROOT = "https://api2.sota.org.uk/"
ASSOC_CHECK_LIST = ["W4V", "W7V"]


@dataclass
class Activation:
    association: str
    summit: str
    date_time: str
    frequencies: str
    activator: str

    def __str__(self) -> str:
        return f'{self.association}/{self.summit} "{get_name(self.association, self.summit)}" at {self.date_time}, frequencies "{self.frequencies}" by {self.activator}'


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


def is_restricted(activation: Activation, check_assocs: List[str]) -> bool:
    """Return True if this summit has any restrictions

    Args:
        activation (Activation): the object giving details of the activation
        check_assocs (List[str]): the list of association codes to check for restrictions

    Returns:
        bool: True if the summit has any restrictions
    """
    if activation.association in check_assocs:
        resp = req.get(
            f"{SOTA_API_ROOT}api/summits/{activation.association}/{activation.summit}"
        )

        if resp.status_code == 200:
            summit_info = json.loads(resp.text)
            return len(summit_info["restrictionList"]) > 0

    return False


def get_spots(hours: int) -> List[Activation]:
    """Get a list of SOTA spots

    Args:
        hours (int): restrict the list to this age in hours

    Returns:
        List[Activation]: the list of spots as Activation objects
    """
    resp = req.get(f"{SOTA_API_ROOT}api/spots/-{hours}/all")

    if resp.status_code == 200:
        spots = json.loads(resp.text)
        return [
            Activation(
                spot["associationCode"],
                spot["summitCode"],
                spot["timeStamp"],
                spot["frequency"],
                spot["activatorCallsign"],
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
        List[Activation]: the list of spots for restricted summits as Activation objects
    """
    spots = get_spots(hours)

    restricted = filter(lambda spot: is_restricted(spot, check_assocs), spots)
    return [str(spot) for spot in restricted]


def get_alerts() -> List[Activation]:
    """Get a list of SOTA alerts

    Returns:
        List[Activation]: the lists of alerts, as Activatiom objects
    """
    resp = req.get(f"{SOTA_API_ROOT}api/alerts")

    if resp.status_code == 200:
        alerts = json.loads(resp.text)
        return [
            Activation(
                alert["associationCode"],
                alert["summitCode"],
                alert["timeStamp"],
                alert["frequency"],
                alert["activatingCallsign"],
            )
            for alert in alerts
        ]

    return []


def get_restricted_alerts(check_assocs: List[str]) -> List[str]:
    """Get a list of SOTA alerts for which there are restrictions

    Args:
        check_assocs (List[str]): the list of association codes to check for restrictions

    Returns:
        List[Activation]: the lists of alerts for restricted summits, as Activatiom objects
    """
    alerts = get_alerts()

    restricted = filter(lambda alert: is_restricted(alert, check_assocs), alerts)
    return [str(alert) for alert in restricted]


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
