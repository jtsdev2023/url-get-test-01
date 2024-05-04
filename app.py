import re
import sys
import argparse
import requests
from datetime import datetime
from time import sleep, perf_counter_ns
from inspect import currentframe, getframeinfo



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
def generate_output_dict(dict_type: str, args_list: list) -> dict:
    """Doc string"""
    parent_frame_info = getframeinfo(currentframe())

    # expect args_list = [timestamp, url_domain, elapsed_time_seconds, url_requests_result]
        # CAUTION: basic checks... may need expanding
    
    # asserts for debugging
    def _author_assert_test1():
        assert_frame_info = getframeinfo(currentframe())
        assert dict_type in ['stdout', 'text', 'csv'], \
            f'\n\n\n{__name__}:: Function: {parent_frame_info.function} ' \
            f'Line: {parent_frame_info.lineno} - ' \
            f'Assertion Line: {assert_frame_info.lineno}.\n\n'
    def _author_assert_test2():
        assert_frame_info = getframeinfo(currentframe())
        _l = list( zip( args_list, [str, str, float, requests.models.Response] ) )
        assert all(_l) == True, \
            f'\n\n\n{__name__}:: Function: {parent_frame_info.function} ' \
            f'Line: {parent_frame_info.lineno} - ' \
            f'Assertion Line: {assert_frame_info.lineno}.\n\n'

    _author_assert_test1()
    _author_assert_test2()

    try:
        timestamp, url_domain, elapsed_time_seconds, url_requests_result = args_list
        test = list( zip( args_list, [str, str, float, requests.models.Response] ) )

        runtime_test_args_list = all( [isinstance(x, y) for x, y in test] )
        match runtime_test_args_list:
            
            case False:
                sys.exit(
                    '\n\n:::::     ERROR     :::::\n'
                    f'{__name__}:: Function: {parent_frame_info.function} '
                    f'Line: {parent_frame_info.lineno} - '
                    'args_list error.\n\n'
                )

            case True:
                runtime_test_dict_type = dict_type.lower() in ['stdout', 'text', 'csv']
                match runtime_test_dict_type:
                    case False:
                        sys.exit(
                            '\n\n:::::     ERROR     :::::\n'
                            f'{__name__}:: Function: {parent_frame_info.function} '
                            f'Line: {parent_frame_info.lineno} - '
                            'dict_type error.\n\n'
                        )

                    case True:
                        match dict_type:
                            case 'stdout':
                                stdout_dict = {
                                        'timestamp': timestamp,
                                        'url_domain': url_domain,
                                        'elapsed_time_seconds': elapsed_time_seconds
                                    }
                                return stdout_dict
                        
                            case 'text':
                                text_dict = {
                                    'timestamp': timestamp,
                                    'url_domain': url_domain,
                                    'elapsed_time_seconds': elapsed_time_seconds,
                                    'headers': url_requests_result.headers,
                                    'cookies': url_requests_result.cookies,
                                    'content': url_requests_result.content
                                }
                                return text_dict
                            
                            # csv is same as stdout... look to optimize
                            case 'csv':
                                csv_dict = {
                                    'timestamp': timestamp,
                                    'url_domain': url_domain,
                                    'elapsed_time_seconds': elapsed_time_seconds
                                }
                                return csv_dict

                            case _:
                                sys.exit(
                                    '\n\n:::::     ERROR     :::::\n'
                                    f'{__name__}:: Function: {parent_frame_info.function} '
                                    f'Line: {parent_frame_info.lineno} - ' 
                                    f'dict_type match case failure.'
                                )
            case _:
                sys.exit(
                    '\n\n:::::     ERROR     :::::\n'
                    f'{__name__}:: Function: {parent_frame_info.function} '
                    f'Line: {parent_frame_info.lineno} - '
                )

    except Exception as error:
        sys.exit(
            '\n\n:::::     ERROR     :::::\n'
            f'\n{__name__}:: Function: {parent_frame_info.function} '
            f'Line: {parent_frame_info.lineno}\n\n'
            'Ensure: "dict_type" is one of stdout:str, text:str, or csv:str.\n'
            'Ensure: args_list = '
            '[timestamp:str, url_domain:str, elapsed_time_seconds:int, '
            'url_requests_result:requests.models.Response].\n\n'
        )



####################################################################################################
def generate_format_string(string_template_type: str, string_format_dict: dict) -> str:
    """Doc string"""
    
    parent_frame_info = getframeinfo(currentframe())
    
    # asserts for debugging
    def _author_assert_test1():
        assert_frame_info = getframeinfo(currentframe())
        assert string_template_type in ['stdout', 'text', 'csv'], \
            f'\n\n\n{__name__}:: Function: {parent_frame_info.function} ' \
            f'Line: {parent_frame_info.lineno} - ' \
            f'Assertion Line: {assert_frame_info.lineno}.\n\n'
    def _author_assert_test2():
        assert_frame_info = getframeinfo(currentframe())
        assert isinstance(string_format_dict, dict) == True, \
            f'\n\n\n{__name__}:: Function: {parent_frame_info.function} ' \
            f'Line: {parent_frame_info.lineno} - ' \
            f'Assertion Line: {assert_frame_info.lineno}.\n\n'

    _author_assert_test1()
    _author_assert_test2()

    try:
        match string_template_type:

            case 'stdout':
                timestamp, url_domain, elapsed_time_seconds = \
                    [ v for v in string_format_dict.values() ]
                stdout_tuple = (
                    OUTPUT_STRING_SEPARATOR, 'TIMESTAMP', OUTPUT_STRING_SEPARATOR, ' ', timestamp,
                    OUTPUT_STRING_SEPARATOR, 'URL', OUTPUT_STRING_SEPARATOR, ' ', url_domain,
                    OUTPUT_STRING_SEPARATOR, 'ELAPSED TIME (sec)', OUTPUT_STRING_SEPARATOR, ' ', elapsed_time_seconds
                )
                return STDOUT_FORMAT_STRING.format(*stdout_tuple)

            case 'text':
                timestamp, url_domain, elapsed_time_seconds, headers, cookies, content = \
                    [ v for v in string_format_dict.values() ]
                text_tuple = (
                    OUTPUT_STRING_SEPARATOR, 'TIMESTAMP', OUTPUT_STRING_SEPARATOR, ' ', timestamp,
                    OUTPUT_STRING_SEPARATOR, 'URL', OUTPUT_STRING_SEPARATOR, ' ', url_domain,
                    OUTPUT_STRING_SEPARATOR, 'ELAPSED TIME (sec)', OUTPUT_STRING_SEPARATOR, ' ',
                        elapsed_time_seconds,
                    OUTPUT_STRING_SEPARATOR, 'HTTP HEADERS', OUTPUT_STRING_SEPARATOR, ' ',
                        str(headers),
                    OUTPUT_STRING_SEPARATOR, 'COOKIES', OUTPUT_STRING_SEPARATOR, ' ',
                        str(cookies),
                    OUTPUT_STRING_SEPARATOR, 'HTML CONTENT', OUTPUT_STRING_SEPARATOR, ' ',
                        str(content)
                )
                return OUTPUT_FILE_FORMAT_STRING.format(*text_tuple)

            case 'csv':
                timestamp, url_domain, elapsed_time_seconds = \
                    [ v for v in string_format_dict.values() ]
                return CSV_FORMAT_STRING.format(timestamp,url_domain,elapsed_time_seconds)

            case _:
                sys.exit(
                    '\n\n:::::     ERROR     :::::\n'
                    f'{__name__}:: Function: {parent_frame_info.function} '
                    f'Line: {parent_frame_info.lineno} - ' 
                    f'dict_type match case failure.'
                )

    except Exception as error:
        sys.exit(
            '\n\n:::::     ERROR     :::::\n'
            f'\n{__name__}:: Function: {parent_frame_info.function} '
            f'Line: {parent_frame_info.lineno}\n\n'
        )


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

            # get string format dicts - passed to generate_format_string()
            string_format_args = [timestamp, url_domain, elapsed_time_seconds, url_request_result]
                # stdout dict            
            stdout_dict = generate_output_dict('stdout', string_format_args)
                # text file dict
            text_dict = generate_output_dict('text', string_format_args)
                # csv file dict - timestamp, url_domain, elapsed_time_seconds
            csv_dict = generate_output_dict('csv', string_format_args)


            # write to stdout
            stdout_string = generate_format_string('stdout', stdout_dict)
            print(stdout_string)

            # write text to file
            text_string = generate_format_string('text', text_dict)
            append_output_to_file(text_output_file_name, text_string)

            # write to csv file
            csv_string = generate_format_string('csv', csv_dict)
            append_output_to_file(csv_output_file_name, csv_string)


            if loop_counter < (cli_arguments.repeat - 1):
                sleep(cli_arguments.interval)
            
            loop_counter += 1




####################################################################################################
if __name__ == '__main__':
    run()
