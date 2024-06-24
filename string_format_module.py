import sys
import yaml
import requests
from inspect import currentframe, getframeinfo



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

# app.py suppress true and concurrency true message
SUPPRESS_TRUE_CONCURRENCY_TRUE_MSG = (
    '\n\nSUPPRESS OUTPUT TO FILE - TRUE\n'
    'RUN CONCURRENT - TRUE\n'
    '\nconcurrency elapsed runtime: {}'
)



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
                    [ str(v) for v in string_format_dict.values() ]
                text_tuple = (
                    OUTPUT_STRING_SEPARATOR, 'TIMESTAMP', OUTPUT_STRING_SEPARATOR, ' ', timestamp,
                    OUTPUT_STRING_SEPARATOR, 'URL', OUTPUT_STRING_SEPARATOR, ' ', url_domain,
                    OUTPUT_STRING_SEPARATOR, 'ELAPSED TIME (sec)', OUTPUT_STRING_SEPARATOR, ' ',
                        elapsed_time_seconds,
                    OUTPUT_STRING_SEPARATOR, 'HTTP HEADERS', OUTPUT_STRING_SEPARATOR, ' ',
                        headers,
                    OUTPUT_STRING_SEPARATOR, 'COOKIES', OUTPUT_STRING_SEPARATOR, ' ',
                        cookies,
                    OUTPUT_STRING_SEPARATOR, 'HTML CONTENT', OUTPUT_STRING_SEPARATOR, ' ',
                        content
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
                    'dict_type match case failure.'
                )

    except Exception as error:
        sys.exit(
            '\n\n:::::     ERROR     :::::\n'
            f'\n{__name__}:: Function: {parent_frame_info.function} '
            f'Line: {parent_frame_info.lineno}\n\n'
        )



####################################################################################################

if __name__ == '__main__':
    pass
