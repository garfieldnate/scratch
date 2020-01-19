# input should be output of format_germ_freq.txt
# output will be separated entries with information about their structure
import sys
import re


frequency_score_pattern = re.compile(f"^\\s+[0-9,]+$")
related_pattern = re.compile(f'^\\s+\\w+')

def separate_entries(lines):
    entries = []
    # rule for looking for entries happens to not work on the first one, 
    # since '1' is both index and subentry marker
    entry = lines[0:8]
    expected_index = 2
    for line in lines[9:]:
        if line.lstrip().startswith(str(expected_index)):
            entries.append(entry)
            entry = [line]
            expected_index += 1
        else:
            entry.append(line)
    entries.append(entry)
    return entries

def tokenize(entry):
    type_ = {'lettered': False, 'numbered': False, 'related_headers': []}
    last_line_was_score = False
    for line_num, line in enumerate(entry):

        if last_line_was_score:
            last_line_was_score = False
            if (match := related_pattern.match(line)):
                type_['related_headers'].append(line_num)
        elif (match := frequency_score_pattern.match(line)):
            last_line_was_score = True



        if ' b) ' in line:
            type_['lettered'] = True
        elif ' 2 ' in line:
            type_['numbered'] = True

    if not type_['related_headers']:
        del type_['related_headers']
    return entry, type_

def output_entries(classified_entries):
    for entry, type_ in classified_entries:
        print(f"***{type_}")
        for line in entry:
            print(line, end='')


def main(argv):
    if len(argv) != 2:
        raise ValueError("Usage: python3 separate_entries <single column file>")
    with open(argv[1]) as f:
        lines = f.readlines()
        entries = separate_entries(lines)
        entries = [tokenize(entry) for entry in entries]
        output_entries(entries)


if __name__ == '__main__':
    main(sys.argv)

