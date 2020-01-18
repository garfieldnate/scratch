# input should be output of format_germ_freq.txt
import sys


def separate_entries(lines):
    entries = []
    # rule for looking for entries happens to not work on the first one
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


def output_entries(entries):
    for entry in entries:
        for line in entry:
            print(line, end='')
        print("***")


def main(argv):
    if len(argv) != 2:
        raise ValueError("Usage: python3 separate_entries <single column file>")
    with open(argv[1]) as f:
        lines = f.readlines()
        entries = separate_entries(lines)
        output_entries(entries)


if __name__ == '__main__':
    main(sys.argv)

