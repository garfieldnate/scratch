# Parse out the tokenized entries and import them into tango; 
# you will also need to manually put a '|' character between the 
# en/de entries in rel_header tokens. This has to be done because the text formatting (bold, etc.)
# is lost in the PDF->txt conversion
import sys

import json

from tango import model

model = model.get_model()


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

    entry = {'pos': [], 'en': [], 'ex': [], 'usage': [], 'rel': []}
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
                current_related['ex'].append(ex)
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
                entry['score'] = score
        elif line.startswith("<rel_header>"):
            # there will only be one example and English, but using the same
            # structure will make processing easier
            current_related = {'ex': [], 'en': []}
            entry['rel'].append(current_related)
            try:
                de, en = line[12:].split('|')
                current_related['en'] = [en.strip()]
                current_related['headword'] = de.strip()
            except:
                raise ValueError(f"Couldn't extract en, de from {line[12:]}")
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
            entry = parse_entry_lines(current_entry_lines)
            if entry:
                entries.append(entry)
            current_entry_lines = []
        current_entry_lines.append(line.strip())

    entry = parse_entry_lines(current_entry_lines)
    if entry:
        entries.append(entry)

    return entries


def copy_guaranteed_fields_to_tango(entry, rank):
    tango = {'pronunciation': '', 'image_url': '', 'image_base64': '', 'morphology': ''}

    tango['headword'] = entry['headword']

    tango['source'] = f'FDG: {rank}'

    tango['definition'] = ';'.join(entry['en'])

    notes = entry.get('usage', [])
    notes += [f'frequency score: {entry["score"]}']
    tango['notes'] = "\n".join(notes)

    if len(entry['ex']) > 1:
        tango['example'] = "\n".join([f'* {ex}' for ex in entry['ex']])
    else:
        tango['example'] = entry['ex'][0]

    return tango

def import_tango(tango):
    print(f'Would call model.add_tango("de", {tango})')
    # commented out because it's a sensitive operation; uncomment to actually import
    # model.add_tango('de', tango)


def import_entries(entries):
    for entry in entries:
        print(entry)

        rank = entry['rank']
        tango = copy_guaranteed_fields_to_tango(entry, rank)

        tango['morphology'] = ';'.join(entry['pos'])

        import_tango(tango)

        for rel in entry['rel']:
            tango = copy_guaranteed_fields_to_tango(rel, rank)
            import_tango(tango)


def main(argv):
    if len(argv) != 2:
        raise ValueError("Usage: python3 parse_germ.py <tokenized file>")
    entries = parse_file(argv[1])
    import_entries(entries)
    print(f"Total entries parsed: {len(entries)}")

if __name__ == '__main__':
    main(sys.argv)

