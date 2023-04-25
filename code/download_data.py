#!/usr/bin/env python3 

import sys
import os
from os import path
import argparse
from pathlib import Path
from data_utils import *

# default values
default_url = 'https://theportalwiki.com/wiki/GLaDOS_voice_lines'
wait_time = 150
fp = path.abspath(str(sys.modules['__main__'].__file__))
default_out_dir = path.abspath(join(fp ,"../..", 'glados_data'))

if __name__ == "__main__":
    # help messages
    url_help = """\
        URL to download data from.
        Default: 
        {}
        """.format(default_url)
    wait_help = """\
        Time (in seconds) to wait before re-trying a given file's download. 
        Default:
        {}
        """.format(wait_time)
    out_dir_help = """\
        Directory to save data being downloaded.
        Default: 
        {}
        """.format(default_out_dir)

    ## args
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        )
    # url for download
    parser.add_argument("-u", "--url", 
                        help=url_help,
                        default=default_url,
                        required=False)
    # dir to save data
    parser.add_argument('-o', '--out_dir',
                        help=out_dir_help,
                        default=default_out_dir,
                        required=False)
    # time-out pause
    parser.add_argument('-w', '--wait',
                        help=wait_help,
                        default=wait_time,
                        required=False)

    # get the args given to command line
    args = parser.parse_args()
    print()
    # arg values to variables
    base_url = args.url
    out_dir = args.out_dir
    wait_time = args.wait

    # download with given variables
    download_data(data_url=base_url,
                out_path=out_dir,
                wait_time=wait_time)
