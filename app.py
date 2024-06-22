import requests
import argparse_module
import input_file_module
import string_format_module
from datetime import datetime
from time import sleep, perf_counter_ns




####################################################################################################
# other constants
TIME_DIVISOR = 1e9
TIMESTAMP_STR_FORMAT = '%Y%m%d - %H%M%S.%f'



####################################################################################################
def calculate_elapsed_time(
        start_time_ns: int, stop_time_ns: int, time_divisor: int) -> int:
    return (stop_time_ns - start_time_ns) / time_divisor




####################################################################################################
def run() -> int:
    """Doc string"""
    requests.urllib3.disable_warnings()

    cli_arguments = argparse_module.init_argparse()

    if cli_arguments.file:
        url_list = input_file_module.create_url_list(cli_arguments.file)

    else:
        url_list = cli_arguments.url


    for _url in url_list:

        loop_counter = 0
        while loop_counter < cli_arguments.repeat:

            url_index_number = url_list.index(_url)
            url_domain = input_file_module.get_url_domain(_url)

            # file extension (.txt or .csv etc.) set here
            # NOTE: maybe create a class w/ methods that create specific file type?
            #
            text_output_file_name = \
                input_file_module.generate_output_file_name(url_domain, 'txt')
            csv_output_file_name = \
                input_file_module.generate_output_file_name(url_domain, 'csv')

            timestamp = datetime.now().strftime(TIMESTAMP_STR_FORMAT)

            start_time_ns = perf_counter_ns()
            url_request_result = requests.request(cli_arguments.method, _url, timeout=30)
            stop_time_ns = perf_counter_ns()

            elapsed_time_seconds = calculate_elapsed_time(start_time_ns, stop_time_ns, TIME_DIVISOR)

            # get string format dicts - passed to generate_format_string()
            string_format_args = [timestamp, url_domain, elapsed_time_seconds, url_request_result]
                # stdout dict            
            stdout_dict = \
                string_format_module.generate_output_dict('stdout', string_format_args)
                # text file dict
            text_dict = \
                string_format_module.generate_output_dict('text', string_format_args)
                # csv file dict
            csv_dict = string_format_module.generate_output_dict('csv', string_format_args)


            # write to stdout
            stdout_string = \
                string_format_module.generate_format_string('stdout', stdout_dict)
            print(stdout_string)


            match cli_arguments.suppress:
                case False:
                    # write text to file
                    text_string = \
                        string_format_module.generate_format_string('text', text_dict)
                    input_file_module.append_output_to_file(text_output_file_name, text_string)

                    # write to csv file
                    csv_string = \
                        string_format_module.generate_format_string('csv', csv_dict)
                    input_file_module.append_output_to_file(csv_output_file_name, csv_string)
                case True:
                    pass


            if loop_counter < (cli_arguments.repeat - 1):
                sleep(cli_arguments.interval)
            
            loop_counter += 1




####################################################################################################
if __name__ == '__main__':
    run()
