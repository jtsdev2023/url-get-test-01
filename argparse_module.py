import re
import sys
import argparse
from inspect import currentframe, getframeinfo



# match urls
regex_pattern = re.compile(r'^https*://\w+\.\w+(\.\w+)*/')



####################################################################################################
def verify_input_file(input_string: str) -> str:
    """Doc string"""
    input_file_pattern = re.compile(r'^[\w\W]+\.(txt|text|csv|yaml|yml)$')
    if input_file_pattern.match(input_string):
        return True
    else:
        return False



####################################################################################################
def init_argparse() -> None:
    """Doc string"""
    parser = argparse.ArgumentParser()
    url_read_exclusion = parser.add_mutually_exclusive_group(required=True)
    url_file_version_group = parser.add_argument_group()

    # don't allow -u/--url and -f/--file at same time
    url_read_exclusion.add_argument(
        '-u', '--url', nargs='+', required=False, type=str,
        help= \
            'Target URL. Multiple URLs allowed. '
            'Cannot be used in conjunction with -f/--file argument.'
    )
    url_read_exclusion.add_argument('-f', '--file', required=False, type=str,
        help= \
            'Read URL from file. '
            'Cannot be used in conjunction with -u/--hrl argument.'
    )


    parser.add_argument(
        '-i', '--interval', required=False, type=int, default=1,
        help='URL polling internal.'
    )
    parser.add_argument(
        '-r', '--repeat', required=False, type=int, default=1,
        help='Number of times to poll URL.'
    )
    parser.add_argument(
        '-m', '--method', required=False, type=str.upper, default='GET',
        choices=['GET'], help='HTTP method.'
    )
    parser.add_argument(
        '-t', '--timeout', required=False, type=int, default=30,
        help='HTTP request timeout in seconds.'
    )
    parser.add_argument(
        '-c', '--concurrency', required=False, action='store_true',
        help= \
            'Utilize ThreadPoolExecutor for concurrency. '
            'Will not write URL output to STDOUT.'
    )
    parser.add_argument('-s', '--suppress', required=False, action='store_true',
        help='Suppress writing output to file.'
    )

    args = parser.parse_args()

    if args.file:

        if verify_input_file(args.file) == True:
            return args

        else:
            sys.exit('\n\n:::::     ERROR     :::::\n\n'
                f'Invalid CLI argument -f/--file "{args.file}".\n\n'
                'Must be one of ".(txt|text)", ".csv", or ".(yaml|yml)".\n'
                'Example: "file.txt", "file.csv", or "file.yaml".\n\n'
            )
    
    else:
        return args



####################################################################################################

if __name__ == '__main__':
    pass
