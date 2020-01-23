# Parse out the tokenized entries
import sys

import json


def parse_entry_lines(lines):
    # skip empty lines and untokenizable entries
    if not lines:
        return None
    info = json.loads(lines[0][3:])
    if info['manual']:
        print('Please handle this one manually:')
        for line in lines:
            print(line)
        return None

    def raise_if_in_subheader(line, current_related):
        if current_related:
            raise ValueError(f"Not sure how to put {line} in {current_related}")

    entry = {'pos': [], 'en': [], 'ex': [], 'usage': [], 'scores': [], 'rel': []}
    current_related = None
    for line in lines[1:]:
        if not line:
            continue
        elif line.startswith("<rank>"):
            raise_if_in_subheader(line, current_related)
            entry['rank'] = line[6:]
        elif line.startswith("<headword>"):
            raise_if_in_subheader(line, current_related)
            entry['headword'] = line[10:]
        elif line.startswith("<pos>"):
            raise_if_in_subheader(line, current_related)
            entry['pos'].append(line[5:])
        elif line.startswith("<english>"):
            raise_if_in_subheader(line, current_related)
            entry['en'].append(line[9:])
        elif line.startswith("<example>"):
            ex = line[9:]
            if current_related:
                current_related['ex'] = ex
            else:
                entry['ex'].append(ex)
        elif line.startswith("<usage>"):
            raise_if_in_subheader(line, current_related)
            entry['usage'].append(line[7:])
        elif line.startswith("<score>"):
            score = line[7:]
            if current_related:
                current_related['score'] = score
            else:
                entry['scores'].append(score)
        elif line.startswith("<rel_header>"):
            current_related = {}
            entry['rel'].append(current_related)
            current_related['header'] = line[12:]
        elif line.startswith("<sub_index>"):
            raise_if_in_subheader(line, current_related)
            # meh
            pass
        else:
            raise ValueError("Unparseable line: " + line)

    return entry

def parse_file(file):
    entries = []
    current_entry_lines = []
    for line in open(file):
        if line.startswith('***'):
            if (entry := parse_entry_lines(current_entry_lines)):
                entries.append(entry)
            current_entry_lines = []
        current_entry_lines.append(line.strip())


    if (entry := parse_entry_lines(current_entry_lines)):
        entries.append(entry)

    return entries



def main(argv):
    if len(argv) != 2:
        raise ValueError("Usage: python3 parse_germ.py <tokenized file>")
    entries = parse_file(argv[1])
    for entry in entries:
        print(entry)
    print(f"Total entries parsed: {len(entries)}")

if __name__ == '__main__':
    main(sys.argv)

