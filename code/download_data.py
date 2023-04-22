#!/usr/bin/env python3 

import sys
import os
import argparse
from data_utils import *

# default values
default_url = 'https://theportalwiki.com/wiki/GLaDOS_voice_lines'
wait_time = 15

if __name__ == "__main__":
    # help messages
    url_help = '''URL to download data from.
                Default: {}'''.format(default_url)
    wait_help = '''Time (in seconds) to wait before re-trying a given
                file's download. Default is {} seconds.'''.format(wait_time)
    ## args
    parser = argparse.ArgumentParser()
    # url for download
    parser.add_argument("-u", "--url", 
                        help=url_help,
                        default=default_url,
                        required=True)
    # dir to save data
    parser.add_argument('-o', '--out_dir',
                        help='Directory to save data',
                         required=True)
    # time-out pause
    parser.add_argument('-w', '--wait',
                        help=wait_help,
                        default=15,
                        required=False)

    args = parser.parse_args()
    if not args.help:
        print("hello world!")
