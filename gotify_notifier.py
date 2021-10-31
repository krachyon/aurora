import aurora_lib
import time
import requests
import argparse
import cli_common
import itertools
import sys

parser = argparse.ArgumentParser('gotify_notifier')

parser.add_argument('base_url', nargs='?', type=str, help='gotify server to point at')
parser.add_argument('token', nargs='?', type=str, help='api-token to use for the gotify request')
args = cli_common.add_args_and_verify(parser)

# infinite loop
for i in itertools.count():

    probab = aurora_lib.get_probability_at(args.latitude, args.longitude)
    print(f"{probab:.2f}")
    sys.stdout.flush()
    if probab > args.threshold or (args.everyN and i % args.everyN == 0):

        resp = requests.post(f'{args.base_url}/message?token={args.token}', json={
            "message": f"probability of visible aurora: {probab:.2f}%",
            "priority": 5000,
            "title": "Aurora forecast"})
        # assert resp.status_code == 200   # will explode anyway if failure

    time.sleep(args.interval)

