

# process csv file
csv_output_file_string = \
"{},{},{},\n".format(
    url_domain, timestamp, elapsed_time
)


# avoid sleep timer on last run
loop_counter = 0
while loop_counter < repeat:
    ...
    if loop_counter < (repeat - 1):
        sleep(interval)

    loop_counter += 1
