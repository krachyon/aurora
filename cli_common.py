import argparse


def add_args_and_verify(parser: argparse.ArgumentParser):
    parser.add_argument('latitude', type=float, nargs='?')
    parser.add_argument('longitude', type=float, nargs='?')
    parser.add_argument('threshold', type=float, nargs='?', default=50,
        help='number between 0-100, percent probability of spotting aurora that is needed to send notification')
    parser.add_argument('interval', default=5*60, type=int, nargs='?', help='how often to check forecast?')
    parser.add_argument('everyN', default=0, type=int, nargs='?',
                        help='send notification every N queries regardless if threshold is met (0->never)')

    args = parser.parse_args()

    assert args.interval <= 120, 'query interval {args.interval} too short, no DOSing NOAA plz'
    assert 0 <= args.threshold <= 100, f'{args.threshold} is not a valid percentage'

    return args
