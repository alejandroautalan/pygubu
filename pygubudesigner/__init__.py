import logging
import argparse

# Setup logging level
parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('--loglevel')
args = parser.parse_args()

loglevel = str(args.loglevel).upper()
loglevel = getattr(logging, loglevel, logging.WARNING)
logging.basicConfig(level=loglevel)
