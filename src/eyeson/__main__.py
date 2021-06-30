import argparse
import calendar
import datetime
import time

import requests
import json
from rich.console import Console
from rich.table import Table

from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

from . import core
from . import translators

console = Console()

parser = argparse.ArgumentParser()
parser.add_argument("-s", help="System name, closest match used", default="1DQ1-A")
parser.add_argument("-n", help="Number of frags to return in output", default="3")
args = parser.parse_args()


def main(requested_system, number_of_rows):
    # sys_name = "A1-AUH"
    sys_name = requested_system
    num_kills = number_of_rows
    print(f"System specified as: {sys_name}")
    sys_id = translators.name2id(sys_name)
    closest_match = translators.id2name(sys_id)
    print(f"Closest match is {closest_match}, using that...")
    kills_dict, kill_list, hash_list = core.get_kills_dict(sys_id, int(num_kills))

    obj_list = core.create_objects(num_kills)
    filled_vic_list = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_result = executor.map(
            core.fill_in_object, obj_list, kill_list, hash_list
        )
        for future in future_result:
            filled_vic_list.append(future)

    frag_list_final = core.create_table(filled_vic_list)

    console.print(frag_list_final)

    num_gates = core.num_stargates(sys_id)

    num_jumps = core.get_jumps(sys_id)

    interactions = core.get_recent_kills(sys_id)

    sys_stats_table = Table(title=f"System Stats At-a-glance:")
    sys_stats_table.add_column("Metric:", justify="center", style="white")
    sys_stats_table.add_column("Value:", justify="center", style="white")

    try:
        sys_stats_table.add_row("Recent NPC Kills:", str(interactions[0]))
    except:
        sys_stats_table.add_row("Recent NPC Kills:", "0")

    try:
        sys_stats_table.add_row("Recent Capsule Kills:", str(interactions[1]))
    except:
        sys_stats_table.add_row("Recent Capsule Kills:", "0")

    try:
        sys_stats_table.add_row("Recent Player Ship Kills:", str(interactions[2]))
    except:
        sys_stats_table.add_row("Recent Player Ship Kills:", "0")

    sys_stats_table.add_row("Number of jumps recently:", str(num_jumps))
    sys_stats_table.add_row("Number of stargates in system:", str(num_gates))

    console.print(sys_stats_table)


if __name__ == "__main__":

    main(args.s, args.n)
