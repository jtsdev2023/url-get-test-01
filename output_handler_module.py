import requests
import argparse_module
import file_handling_module
import string_format_module
from datetime import datetime
from time import sleep, perf_counter_ns



####################################################################################################
TIMESTAMP_STR_FORMAT = '%Y%m%d - %H%M%S.%f'
TIME_DIVISOR = 1e9



####################################################################################################
def calculate_elapsed_time(
        start_time_ns: int, stop_time_ns: int, time_divisor: int) -> int:
    return (stop_time_ns - start_time_ns) / time_divisor



####################################################################################################
def stdout_handler(string_format_args: list) -> None:
      """Doc string"""
      # stdout dict            
      stdout_dict = \
            string_format_module.generate_output_dict('stdout', string_format_args)
      # write to stdout
      stdout_string = \
            string_format_module.generate_format_string('stdout', stdout_dict)
      
      print(stdout_string)



####################################################################################################
def output_file_handler(string_format_args_list: list) -> None:
      """Doc string"""
      string_format_args = string_format_args_list[0:4]
      text_output_file_name = string_format_args_list[4]
      csv_output_file_name = string_format_args_list[5]

      # text file dict
      text_dict = \
            string_format_module.generate_output_dict('text', string_format_args)
      # csv file dict
      csv_dict = \
            string_format_module.generate_output_dict('csv', string_format_args)

      # write text to file
      text_string = \
            string_format_module.generate_format_string('text', text_dict)
      
      file_handling_module.append_output_to_file(
            text_output_file_name, text_string)

      # write to csv file
      csv_string = \
            string_format_module.generate_format_string('csv', csv_dict)
      
      file_handling_module.append_output_to_file(
            csv_output_file_name, csv_string)



####################################################################################################
def run(http_method, target_url:str) -> dict:
      """Doc string"""
      requests.urllib3.disable_warnings()

      url_domain = file_handling_module.get_url_domain(target_url)

      text_output_file_name = \
                file_handling_module.generate_output_file_name(url_domain, 'txt')
      csv_output_file_name = \
            file_handling_module.generate_output_file_name(url_domain, 'csv')
      
      timestamp = datetime.now().strftime(TIMESTAMP_STR_FORMAT)

      start_time_ns = perf_counter_ns()
      url_request_result = requests.request(http_method, target_url)
      stop_time_ns = perf_counter_ns()

      elapsed_time_seconds = \
            calculate_elapsed_time(start_time_ns, stop_time_ns, TIME_DIVISOR)
      
      # return string format args to be passed to generate_format_string()
      # return {
      #       'timestamp': timestamp,
      #       'url_domain': url_domain,
      #       'elapsed_time_seconds': elapsed_time_seconds,
      #       'url_request_result': url_request_result,
      #       'text_output_file_name': text_output_file_name,
      #       'csv_output_file_name': csv_output_file_name
      # }
      return [
            timestamp,
            url_domain,
            elapsed_time_seconds,
            url_request_result,
            text_output_file_name,
            csv_output_file_name
      ]



####################################################################################################
if __name__ == "__main__":
      pass
