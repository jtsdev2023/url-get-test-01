

# process csv file
csv_output_file_string = \
"{},{},{},\n".format(
    url_domain, timestamp, elapsed_time
)

OUTPUT_FORMAT = (':::::', {}, ':::::', ' ', {})


# avoid sleep timer on last run
loop_counter = 0
while loop_counter < repeat:
    ...
    if loop_counter < (repeat - 1):
        sleep(interval)

    loop_counter += 1


OUTPUT_STRING_SEPARATOR, 'URL', OUTPUT_STRING_SEPARATOR, ' ', url,
OUTPUT_STRING_SEPARATOR, 'ELAPSED TIME', OUTPUT_STRING_SEPARATOR, ' ', elapsed_time_seconds

s1 = STDOUT_FORMAT_STRING.format(
    OUTPUT_STRING_SEPARATOR, 'TIMESTAMP', OUTPUT_STRING_SEPARATOR, ' ', timestamp,
    OUTPUT_STRING_SEPARATOR, 'URL', OUTPUT_STRING_SEPARATOR, ' ', url,
    OUTPUT_STRING_SEPARATOR, 'ELAPSED TIME (sec)', OUTPUT_STRING_SEPARATOR, ' ', elapsed_time_seconds
    )

s2 = OUTPUT_FILE_FORMAT_STRING.format(
    OUTPUT_STRING_SEPARATOR, 'TIMESTAMP', OUTPUT_STRING_SEPARATOR, ' ', timestamp,
    OUTPUT_STRING_SEPARATOR, 'URL', OUTPUT_STRING_SEPARATOR, ' ', url,
    OUTPUT_STRING_SEPARATOR, 'ELAPSED TIME (sec)', OUTPUT_STRING_SEPARATOR, ' ', elapsed_time_seconds,
    OUTPUT_STRING_SEPARATOR, 'HTTP HEADERS', OUTPUT_STRING_SEPARATOR, ' ', str(url_request_result.headers),
    OUTPUT_STRING_SEPARATOR, 'COOKIES', OUTPUT_STRING_SEPARATOR, ' ', str(url_request_result.cookies),
    OUTPUT_STRING_SEPARATOR, 'HTML CONTENT', OUTPUT_STRING_SEPARATOR, ' ', str(url_request_result.content)
)


    

