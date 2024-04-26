import re
import argparse
import requests
from datetime import datetime
from time import sleep, perf_counter_ns



# match urls
regex_pattern = re.compile(r'^https*://\w+\.\w+(\.\w+)*/')



####################################################################################################
# string formatting
OUTPUT_STRING = '{0:<10}{1:12}{2:>10}{3}{4:>10}'
OUTPUT_FORMAT = (':::::', {}, ':::::', ' ', {})

# other constants
TIME_DIVISOR = 1e9
TIMESTAMP_STR_FORMAT = '%Y%m%d - %H%M%S.%f'


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
    parser.add_argument(
        '-m', '--method', required=False, type=str.upper, default='GET',
        choices=['GET', 'PUT', 'POST'], help='HTTP method.')
    parser.add_argument(
        '-t', '--timeout', required=False, type=int, default=30,
        help='HTTP request timeout in seconds.')
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
def generate_output_file_name(url_domain: str, output_file_extension) -> str:
    """Doc string"""
    # regex to match and replace special characters
    re_exp = re.compile(r'\W')
    output_file_name = f"{re_exp.sub('_', url_domain)}.{output_file_extension}"

    return output_file_name



####################################################################################################
def append_output_to_file(
        output_file_name: str, output_string: str, output_file_encoding: str='utf-8') -> None:
    """Doc string"""
    with open(output_file_name, 'a', encoding=output_file_encoding) as f:
        f.write(output_string)


####################################################################################################
def calculate_elapsed_time(
        start_time_ns: int, stop_time_ns: int, time_divisor: int=TIME_DIVISOR) -> int:
    return (stop_time_ns - start_time_ns) / time_divisor



####################################################################################################
def run() -> int:
    """Doc string"""
    requests.urllib3.disable_warnings()

    cli_arguments = init_argparse()

    for url in cli_arguments.url:
        url_index_number = cli_arguments.url.index(url)
        url_domain = strip_url_domain(url)

        # file extension (.txt or .csv etc.) set here
        # NOTE: maybe create a class w/ methods that create specific file type?
        #
        text_output_file_name = generate_output_file_name(url_domain, 'txt')
        csv_output_file_name = generate_output_file_name(url_domain, 'csv')

        timestamp = datetime.now().strftime(TIMESTAMP_STR_FORMAT)

        start_time_ns = perf_counter_ns()
        url_request_result = requests.request(cli_arguments.method, url, timeout=30)
        stop_time_ns = perf_counter_ns()

        # subtract nanosecond start from stop and divide by 1 billion to convert to seconds
        elapsed_time_seconds = calculate_elapsed_time(start_time_ns, stop_time_ns, 1e9)

        stdout_string = OUTPUT_STRING.format(OUTPUT_FORMAT.format())



####################################################################################################
if __name__ == '__main__':
    # run()
    cli_arguments = init_argparse()

    for url in cli_arguments.url:
        url_index_number = cli_arguments.url.index(url)
        timestamp = datetime.now().strftime('%Y%m%d - %H%M%S.%f')
        start_time_ns = perf_counter_ns()
        url_request_result = requests.request(cli_arguments.method, url, timeout=30)
        stop_time_ns = perf_counter_ns()

        # subtract nanosecond start from stop and divide by 1 billion to convert to seconds
        elapsed_time_seconds = 
        print(url_index_number, url, timestamp, elapsed_time_seconds, sep='\n')
