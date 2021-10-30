import notify2
import aurora
import time
import argparse
import itertools

import cli_common

parser = argparse.ArgumentParser('kde_notifier')
args = cli_common.add_args_and_verify(parser)

notify2.init("kde")

# infinite loop
for i in itertools.count():

    probab = aurora.get_probability_at(aurora.getData(), args.latitude, args.longitude)
    if probab > args.threshold or (i and i % args.everyN == 0):
        n = notify2.Notification("Aurora!",
                                 f"Probability: {probab}",
                                 "notification-message-im")
        n.show()

    time.sleep(args.interval)
