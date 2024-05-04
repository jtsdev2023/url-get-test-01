import re
import argparse
import requests
from datetime import datetime
from time import sleep, perf_counter_ns



# match urls
regex_pattern = re.compile(r'^https*://\w+\.\w+(\.\w+)*/')



####################################################################################################
# string formatting
OUTPUT_STRING_SEPARATOR = ':::::'

# timestamp, url, elapsed_time_seconds
STDOUT_FORMAT_STRING = (
    '\n{:<10}{:18}{:>10}{:>5}{:>10}\n'
    '{:<10}{:18}{:>10}{:>5}{:>10}\n'
    '{:<10}{:18}{:>10}{:>5}{:>10}\n'
)

# timestamp, url, elapsed time (sec), http headers, cookies, http content
OUTPUT_FILE_FORMAT_STRING = (
    '\n{:<10}{:18}{:>10}{:>5}{:>10}\n'
    '{:<10}{:18}{:>10}{:>5}{:>10}\n'
    '{:<10}{:18}{:>10}{:>5}{:>10}\n'
    '\n{:<10}{:18}{:>10}{:>5}\n\n{:>10}\n'
    '\n{:<10}{:18}{:>10}{:>5}\n\n{:>10}\n'
    '\n{:<10}{:18}{:>10}{:>5}\n\n{:>10}\n'
)

# timestamp, url, elapsed_time_seconds
CSV_FORMAT_STRING = '{},{},{}\n'


# other constants
TIME_DIVISOR = 1e9
TIMESTAMP_STR_FORMAT = '%Y%m%d - %H%M%S.%f'


####################################################################################################
def init_argparse() -> None:
    """Doc string"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-u', '--url', nargs='+', required=True, type=str,
        help='Target URL. Multiple URLs allowed.'
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
    parser.add_argument('-f', '--file', required=False, type=str,
        help='Read URL from file.'
    )
    parser.add_argument('-s', '--suppress', required=False, action='store_true',
        help='Suppress writing output to file.'
    )
    args = parser.parse_args()

    return args



####################################################################################################
def get_url_domain(target_url: str) -> str:
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
        start_time_ns: int, stop_time_ns: int, time_divisor: int) -> int:
    return (stop_time_ns - start_time_ns) / time_divisor



####################################################################################################
def generate_output_dict(dict_type: str, *args) -> dict:
    """Doc string"""
    timestamp, url_domain, elapsed_time_seconds, requests_object = args

    match dict_type:

        case output_stdout:
            stdout_dict = {
                    'timestamp':timestamp,
                    'url_domain':url_domain,
                    'elapsed_time_seconds':elapsed_time_seconds
                }
            return stdout_dict
    
        case output_file:
            output_file_dict = {
                **stdout_dict,
                'headers': requests_object.headers,
                'cookies': requests_object.cookies,
                'content': requests_object.content
            }
            return output_file_dict
        
        case _:
            pass




####################################################################################################
def generate_format_string(string_template_type: str, **kwargs: dict) -> str:
    """Doc string"""
    
    match string_template_type:

        case output_stdout:
            timestamp, url_domain, elapsed_time_seconds = kwargs
            stdout_tuple = (
                OUTPUT_STRING_SEPARATOR, 'TIMESTAMP', OUTPUT_STRING_SEPARATOR, ' ', timestamp,
                OUTPUT_STRING_SEPARATOR, 'URL', OUTPUT_STRING_SEPARATOR, ' ', url_domain,
                OUTPUT_STRING_SEPARATOR, 'ELAPSED TIME (sec)', OUTPUT_STRING_SEPARATOR, ' ', elapsed_time_seconds
            )
            return STDOUT_FORMAT_STRING.format(*stdout_tuple)

        case output_file:
            timestamp, url_domain, elapsed_time_seconds, headers, cookies, content = kwargs
            file_tuple = (
                OUTPUT_STRING_SEPARATOR, 'TIMESTAMP', OUTPUT_STRING_SEPARATOR, ' ', timestamp,
                OUTPUT_STRING_SEPARATOR, 'URL', OUTPUT_STRING_SEPARATOR, ' ', url_domain,
                OUTPUT_STRING_SEPARATOR, 'ELAPSED TIME (sec)', OUTPUT_STRING_SEPARATOR, ' ',
                    elapsed_time_seconds,
                OUTPUT_STRING_SEPARATOR, 'HTTP HEADERS', OUTPUT_STRING_SEPARATOR, ' ',
                    str(url_request_result.headers),
                OUTPUT_STRING_SEPARATOR, 'COOKIES', OUTPUT_STRING_SEPARATOR, ' ',
                    str(url_request_result.cookies),
                OUTPUT_STRING_SEPARATOR, 'HTML CONTENT', OUTPUT_STRING_SEPARATOR, ' ',
                    str(url_request_result.content)
            )
            return OUTPUT_FILE_FORMAT_STRING.format(*file_tuple)

        case _:
            pass


####################################################################################################
def run() -> int:
    """Doc string"""
    requests.urllib3.disable_warnings()

    cli_arguments = init_argparse()

    for _url in cli_arguments.url:

        loop_counter = 0
        while loop_counter < cli_arguments.repeat:

            url_index_number = cli_arguments.url.index(_url)
            url_domain = get_url_domain(_url)

            # file extension (.txt or .csv etc.) set here
            # NOTE: maybe create a class w/ methods that create specific file type?
            #
            text_output_file_name = generate_output_file_name(url_domain, 'txt')
            csv_output_file_name = generate_output_file_name(url_domain, 'csv')

            timestamp = datetime.now().strftime(TIMESTAMP_STR_FORMAT)

            start_time_ns = perf_counter_ns()
            url_request_result = requests.request(cli_arguments.method, _url, timeout=30)
            stop_time_ns = perf_counter_ns()

            # subtract nanosecond start from stop and divide by 1 billion to convert to seconds
            elapsed_time_seconds = calculate_elapsed_time(start_time_ns, stop_time_ns, TIME_DIVISOR)

            # get string format dicts
            # stdout
            string_format_args = [timestamp, url_domain, elapsed_time_seconds, url_request_result]
            stdout_dict = generate_output_dict('output_stdout', string_format_args)
            # output file
            output_file_dict = generate_format_string('output_file', string_format_args)

            # write to stdout
            stdout_str = generate_format_string('stdout_string', stdout_dict)

            # write to file
            file_out_str = generate_format_string('output_file_string', output_file_dict)

            
            csv_output_file_string = CSV_FORMAT_STRING.format(
                timestamp,
                url_domain,
                elapsed_time_seconds
            )


            # print(stdout_string)
            print(stdout_str)

            # write to text file
            # append_output_to_file(text_output_file_name, text_output_file_string)
            append_output_to_file(text_output_file_name, file_out_str)

            # write to csv file
            append_output_to_file(csv_output_file_name, csv_output_file_string)


            if loop_counter < (cli_arguments.repeat - 1):
                sleep(cli_arguments.interval)
            
            loop_counter += 1




####################################################################################################
if __name__ == '__main__':
    run()
