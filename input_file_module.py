import re
from inspect import currentframe, getframeinfo



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
def create_text_url_list(file_name:str) -> list[str]:
    """Doc string"""
    with open(file_name, 'r') as f:
            _url_list_text = f.readlines()
        
    return [ url.strip() for url in _url_list_text ]



####################################################################################################
def read_file(file_name: str) -> str:
    """Doc string"""
    with open(file_name, 'r') as f:
        _file_string = f.read()

    return _file_string



####################################################################################################
def create_yaml_list(file_name:str) -> list[str]:
    """Doc string"""
    yaml_string = read_file(file_name)
    # may need to validate yaml string/object
    _yaml_list = yaml.safe_load(yaml_string)

    return _yaml_list



####################################################################################################
def create_csv_list(file_name: str) -> list[str]:
    """Doc string"""
    csv_string = read_file(file_name)
    # a comma "," is a safe URL character
    # so this will need work to make it robust
    _csv_list = [ url.strip() for url in csv_string.split(',') ]

    return _csv_list



####################################################################################################
def create_url_list(file_name: str) -> list[str]:
    """Doc string"""
    parent_frame_info = getframeinfo(currentframe())

    # parse file name to determine file type - text, csv, yaml
    _file_extension = file_name.split('.')[-1]

    match _file_extension:

        case 'txt' | 'text':
            _text_list = create_text_url_list(file_name)
            return _text_list
        
        case 'yml' | 'yaml':
            _yaml_list = create_yaml_list(file_name)
            return _yaml_list

        case 'csv':
            _csv_list = create_csv_list(file_name)
            return _csv_list
        
        case _:
            sys.exit(
                '\n\n:::::     ERROR     :::::\n'
                f'{__name__}:: Function: {parent_frame_info.function} '
                f'Line: {parent_frame_info.lineno}\n\n'
            )



####################################################################################################

if __name__ == '__main__':
    pass
