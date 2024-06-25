import requests
import argparse_module
import file_handling_module
import string_format_module
import output_handler_module
from datetime import datetime
from time import sleep, perf_counter_ns



####################################################################################################
def main() -> int:
    """Doc string"""

    cli_arguments = argparse_module.init_argparse()

    if cli_arguments.file:
        url_list = file_handling_module.create_url_list(cli_arguments.file)

    else:
        url_list = cli_arguments.url


    match cli_arguments.concurrency:
        case False:
            for target_url in url_list:
                loop_counter = 0
                while loop_counter < cli_arguments.repeat:
                    # print stdout
                    string_format_args_list = \
                        output_handler_module.run(cli_arguments.method, target_url)
                    output_handler_module.stdout_handler(string_format_args_list[0:4])

                    # output file handling
                    match cli_arguments.suppress:
                        case True:
                            pass
                        case False:
                            output_handler_module.output_file_handler(string_format_args_list)

                    if loop_counter < (cli_arguments.repeat - 1):
                        sleep(cli_arguments.interval)
                
                    loop_counter += 1



####################################################################################################
if __name__ == '__main__':
    main()
 