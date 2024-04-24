import re
import argparse
from urllib.request import Request
from datetime import datetime
from time import sleep, perf_counter_ns



####################################################################################################
def init_argparse() -> None:
    """Doc string"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', '--url', nargs='+', required=True, type=str,
        help='Target URL. Multiple URLs allowed.')
    parser.add_argument(
        '-i', '--interval', required=False, type=int, default=1,
        help='URL polling internal.')
    parser.add_argument(
        '-r', '--repeat', required=False, type=int, default=1,
        help='Number of times to poll URL.')
    parser.add_argument('-m', '--method', required=False, type=str.upper,
        default='GET', choices=['GET', 'PUT', 'POST'], help='HTTP method.')
    parser.add_argument(
        '-p', '--performance', required=False, type=bool, default=False,
        help=('Run app without printing to stdout. '
              'Will utilize concurrency to increase performance.')
    )

    args = parser.parse_args()

    return args



####################################################################################################
def strip_url_domain(target_url: str) -> str:
    """Doc string"""
    url_domain = target_url.split('/')[2]

    return url_domain



####################################################################################################
def generate_output_file_name(url_domain: str) -> str:
    """Doc string"""
    # regex to match and replace special characters
    re_exp = re.compile(r'\W')
    output_file_name = re_exp.sub('_', url_domain)

    return output_file_name



####################################################################################################
def get_url(target_url: str, http_method: str='GET') -> object:
    """Doc string"""
    url_request_result = Request(target_url, method=http_method)

    return url_request_result



####################################################################################################
def run() -> int:
    """Doc string"""

