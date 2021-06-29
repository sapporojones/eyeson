import argparse
import calendar
import datetime
import time

import requests
from rich.console import Console
from rich.table import Table

# import pandas as pd
# import json

console = Console()

parser = argparse.ArgumentParser()
parser.add_argument("-s", help="System name, closest match used", default="1DQ1-A")
parser.add_argument("-n", help="Number of frags to return in output", default="3")
args = parser.parse_args()


def timestamper(timestamp):
    """
    Converts timestamps from json to NhNmNs output in a formatted string
    :param timestamp: formatted like "2021-06-04T01:25:26Z"
    :return: formatted f string containing time data
    """

    # timestamp = "2021-06-04T01:25:26Z"
    td = timestamp.split("T", 1)
    tdd = f"{td[0]} {td[1]}"
    tss = tdd.split("Z", 1)
    iso_stamp = tss[0]

    now = time.gmtime()
    nowsecs = calendar.timegm(now)
    nowstamp = datetime.datetime.utcfromtimestamp(nowsecs)
    killtime = datetime.datetime.fromisoformat(iso_stamp)
    tdelta = nowstamp - killtime

    tsdelta = str(tdelta)
    tssdelta = tsdelta.split(":", 2)
    deltastring = f"{tssdelta[0]}h {tssdelta[1]}m {tssdelta[2]}s ago"

    return deltastring


def num_stargates(sys_id):
    """
    Returns the number of stargates in a specified system.
    :param sys_id: System ID (int) of the designated system to lookup
    :return: integer value of the number of gates in a system.  Will always be >0
    """
    base_url = f"https://esi.evetech.net/latest/universe/systems/{sys_id}/"
    ret_obj = requests.get(base_url)
    obj_json = ret_obj.json()
    n_gates = len(obj_json["stargates"])
    return n_gates


def name2id(sys_name):
    """
    Converts a Solar System name to Solar System ID
    :param sys_name: String value name of the system such as "Jita" or "D-PNP9"
    :return: system_id: the ID value of the provided system name.
    """
    search_url = (
        f"https://esi.evetech.net/latest/search/?categories=solar_system&datasource=tranquility&language=en"
        f"&search={sys_name} "
    )
    search_object = requests.get(search_url)
    search_json = search_object.json()
    system_id = search_json["solar_system"][0]
    return system_id


def id2name(sys_id):
    """
    Helper function to convert system IDs to name for verification purposes
    :param sys_id: the integer value ID of the system to be checked
    :return: system_name: the string name of the system
    """
    search_url = f"https://esi.evetech.net/latest/universe/systems/{sys_id}/"
    search_object = requests.get(search_url)
    search_json = search_object.json()
    system_name = search_json["name"]
    return system_name


def getkillsdict(sys_id, list_len):
    """
    Creates a list of kill IDs and a list of hashes and zips those together in to a dictionary
    TODO:  Use this as the launcher for multithreaded killmail parsing
    :param sys_id: the integer value ID of the system to be checked
    :param list_len: The upper bound of number of entries in the lists to create
    :return: kills_dict a dictionary of kill_ID:hashes to run against ESI
    """

    kill_list = []
    hash_list = []

    zkb_base_url = f"https://zkillboard.com/api/solarSystemID/{sys_id}/"
    zkb_obj = requests.get(zkb_base_url)
    zkb_json = zkb_obj.json()
    # print(zkb_json)
    i = 0
    while i < list_len:
        kill_list.append(zkb_json[i]["killmail_id"])
        # print(zkb_json[i]["killmail_id"])
        hash_list.append(zkb_json[i]["zkb"]["hash"])
        # print(zkb_json[i]["zkb"]["hash"])
        i += 1

    kills_dict = dict(zip(kill_list, hash_list))
    return kills_dict


def getjumps(sysid):
    """
    Retrieves number of jumps in the last 24h or whatever
    :param sysid: the integer value ID of the system to be checked
    :return: Returns integer number of jumps for specified system
    """
    base_url = (
        "https://esi.evetech.net/latest/universe/system_jumps/?datasource=tranquility"
    )
    ret_obj = requests.get(base_url)
    ret_json = ret_obj.json()
    for i in ret_json:
        if i["system_id"] == sysid:
            sysjumps = i["ship_jumps"]
    return sysjumps


def getrecentkills(sysid):
    """
    Retrieves recent metrics for specified system in list format for ease of parsing
    :param sysid:  the integer value ID of the system to be checked
    :return: List of npc_kills, pod_kills, ship_kills for the specified system.
    """
    interaction_list = []
    base_url = (
        "https://esi.evetech.net/latest/universe/system_kills/?datasource=tranquility"
    )
    ret_obj = requests.get(base_url)
    ret_json = ret_obj.json()
    for i in ret_json:
        if i["system_id"] == sysid:
            interaction_list.append(i["npc_kills"])
            interaction_list.append(i["pod_kills"])
            interaction_list.append(i["ship_kills"])
    return interaction_list


def fill_lists(kills_dict):
    """
    Creates the list of kills and formats it in to a table.
    TODO:  Rework to be compatible with multi threading
    :param kills_dict: A dictionary of kills and hashes
    :return: a Table of kills and relevant information
    """
    vicnames = []
    viccorp = []
    viccorptick = []
    vicalice = []
    vicalicetick = []
    vicship = []
    killdate = []
    for k, v in kills_dict.items():
        mail_obj = requests.get(f"https://esi.evetech.net/latest/killmails/{k}/{v}/")
        mail_json = mail_obj.json()
        kd_json = mail_json["killmail_time"]
        adj_date = timestamper(kd_json)
        killdate.append(adj_date)

        try:
            vic_id = mail_json["victim"]["character_id"]
            viccorp_id = mail_json["victim"]["corporation_id"]
        except:
            vic_id = "none"
            viccorp_id = mail_json["victim"]["corporation_id"]

        try:
            vicalice_id = mail_json["victim"]["alliance_id"]
        except:
            vicalice_id = "none"

        vicship_id = mail_json["victim"]["ship_type_id"]

        if vic_id != "none":
            vicname_obj = requests.get(
                f"https://esi.evetech.net/latest/characters/{vic_id}"
            )
            vicname_json = vicname_obj.json()
            vicnames.append(vicname_json["name"])
        else:
            vicnames.append("none")

        viccorp_id_obj = requests.get(
            f"https://esi.evetech.net/latest/corporations/{viccorp_id}/?datasource=tranquility"
        )
        viccorp_json = viccorp_id_obj.json()
        viccorp.append(viccorp_json["name"])
        viccorptick.append(viccorp_json["ticker"])

        if vicalice_id == "none":
            vicalice.append("none")
            vicalicetick.append("NONE")
        else:
            vicalice_obj = requests.get(
                f"https://esi.evetech.net/latest/alliances/{vicalice_id}/?datasource=tranquility"
            )
            vicalice_json = vicalice_obj.json()
            vicalice.append(vicalice_json["name"])
            vicalicetick.append(vicalice_json["ticker"])

        ids_url = f"https://www.fuzzwork.co.uk/api/typeid.php?typeid={vicship_id}"
        vicship_obj = requests.get(ids_url)
        vicship_name = vicship_obj.json()
        vicship.append(vicship_name["typeName"])

    table = Table(title=f"Last {len(kills_dict)} kills")
    table.add_column("Time of Kill:", justify="left", style="white")
    table.add_column("Victim Ship:", justify="left", style="white")
    table.add_column("Victim Name:", justify="left", style="white")
    table.add_column("Victim Corp:", justify="left", style="white")
    table.add_column("Victim Alliance:", justify="left", style="white")

    n = 0
    for i in killdate:
        table.add_row(
            killdate[n],
            vicship[n],
            vicnames[n],
            viccorptick[n],
            vicalicetick[n],
        )
        n += 1

    return table


def main(requested_system, number_of_rows):
    # sys_name = "A1-AUH"
    sys_name = requested_system
    num_kills = number_of_rows
    print(f"System specified as: {sys_name}")
    sys_id = name2id(sys_name)
    closest_match = id2name(sys_id)
    print(f"Closest match is {closest_match}, using that...")
    kills_dict = getkillsdict(sys_id, int(num_kills))
    output_lists = fill_lists(kills_dict)

    console.print(output_lists)

    num_gates = num_stargates(sys_id)

    num_jumps = getjumps(sys_id)

    interactions = getrecentkills(sys_id)

    table1 = Table(title=f"System Stats At-a-glance:")
    table1.add_column("Metric:", justify="center", style="white")
    table1.add_column("Value:", justify="center", style="white")

    try:
        table1.add_row("Recent NPC Kills:", str(interactions[0]))
    except:
        table1.add_row("Recent NPC Kills:", "0")

    try:
        table1.add_row("Recent Capsule Kills:", str(interactions[1]))
    except:
        table1.add_row("Recent Capsule Kills:", "0")

    try:
        table1.add_row("Recent Player Ship Kills:", str(interactions[2]))
    except:
        table1.add_row("Recent Player Ship Kills:", "0")

    table1.add_row("Number of jumps recently:", str(num_jumps))
    table1.add_row("Number of stargates in system:", str(num_gates))

    console.print(table1)


if __name__ == "__main__":

    main(args.s, args.n)
