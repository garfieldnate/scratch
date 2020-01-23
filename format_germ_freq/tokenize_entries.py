# input should be output of format_germ_freq.txt
# output will be separated and tokenized entries
# Entries that have a 'manual': True in the header could not be processed and
# will have to be imported by hand
import sys
import re
import json



POS = ["adj", "adv", "art", "aux", "conj", "inf", "interj", "num", "part", "prep", "pron", "verb", "der", "die", "das"]
ART = {"der", "die", "das"}
GENRE = ["A", "I", "L", "N", "S", "l"] # probably a typo that one line contains l instead of L
GENRE_NAMES = {'A': 'academia', 'I': 'instructional', 'L': 'literature', 'l': 'literature', 'N': 'news', 'S': 'spoken'}
GENRE_RE = f"[{''.join(GENRE)}]"
# rank and German, followed optionally by POS and English
headword_pattern = re.compile(f"^\\s*(?P<rank>\\d+) (?P<headword>.+?)(?: (?P<pos>{'|'.join(POS)}) (?P<english>.+))?$")
# index, the POS and the english
numbered_subheader_pattern = re.compile(f"^\\s*(?P<sub_index>\\d+) (?:(?P<alt1>.+)?(?P<pos>\\b(?:{'|'.join(POS)})\\b)|(?P<alt2>.+\\(sich\\) ))(?P<english>.+)?$")

# Note: m-dash not n-dash (– not -)
frequency_score_pattern = re.compile(f"^\\s+(?P<score>[0-9,]+)(?P<usage>(?: [+–]{GENRE_RE},?)*)$")
related_pattern = re.compile(f'^\\s+\\w+')

def separate_entries(lines):
    entries = []
    # rule for looking for entries happens to not work on the first one, 
    # since '1' is both index and subentry marker
    entry = lines[0:8]
    expected_index = 2
    for line in lines[9:]:
        if line.lstrip().startswith(str(expected_index) + ' '):
            entries.append(entry)
            entry = [line]
            expected_index += 1
        else:
            entry.append(line)
    entries.append(entry)
    return entries

# TODO: a class would be cleaner
current_token_name = None
current_token_contents = []
def tokenize(entry):
    def end_current_token():
        global current_token_name
        global current_token_contents

        if current_token_name:
            token_text = ' '.join([s.strip() for s in current_token_contents])
            new_entry.append(f'<{current_token_name}>{token_text}\n')

        current_token_name = None
        current_token_contents = []

    def start_token(token_name):
        global current_token_name
        global current_token_contents
        end_current_token()
        current_token_name = token_name

    def emit_text(text):
        global current_token_contents
        current_token_contents.append(text)

    type_ = {'lettered': False, 'numbered': False, 'related_headers': [], 'manual': False}
    new_entry = []
    last_line_was_score = False

    if (match := headword_pattern.match(entry[0])):
        start_token('rank')
        emit_text(match.group('rank'))
        start_token('headword')
        emit_text(match.group('headword'))
        if (pos := match.group('pos')):
            start_token('pos')
            emit_text(pos)
            start_token('english')
            emit_text(match.group('english'))
    else:
        raise ValueError("Didn't find headword in first line of entry: " + entry[0])

    for line_num, line in enumerate(entry[1:]):
        if last_line_was_score:
            last_line_was_score = False
            if (match := related_pattern.match(line)):
                start_token('rel_header')
                type_['related_headers'].append(line_num)
        elif (match := frequency_score_pattern.match(line)):
            last_line_was_score = True
            start_token('score')
            emit_text(match.group('score'))
            if (usage := match.group('usage')):
                for u in usage.split(', '):
                    u = u.strip()
                    start_token('usage')
                    if '+' in u:
                        text = "common in "
                    else:
                        text = "uncommon in "
                    genre_code = u[1]
                    text += GENRE_NAMES[genre_code]
                    emit_text(text)
            continue

        stripped_line = line.strip()
        if ' b) ' in line:
            # These complicate auto-processing, so will be manually handled later
            type_['lettered'] = True
            type_['manual'] = True
            type_['manual_reason'] = 'lettered headers'
            start_token('letter')
        elif stripped_line.startswith('1 ') or (type_['numbered'] and (stripped_line.startswith('2 ') or stripped_line.startswith('3 '))):
            type_['numbered'] = True
            if (match := numbered_subheader_pattern.match(line)):
                start_token('sub_index')
                emit_text(match.group('sub_index'))
                if (pos := match.group('pos')):
                    start_token('pos')
                    emit_text(pos)
                
                if (headword := match.group('alt1')):
                    start_token('headword')
                    emit_text(headword)
                elif (headword := match.group('alt2')):
                    start_token('headword')
                    emit_text(headword)

                if (en := match.group('english')):
                    start_token('english')
                    emit_text(en)
                continue
            else:
                # when the match fails, have to manually separate the German from the English
                type_['manual'] = True
                type_['manual_reason'] = 'unmatchable subheader'
                # raise ValueError("Couldn't process subheader " + line)
        elif '•' in line:
            start_token('example')
            line = line.split("•")[1]

        # if no new tokens were found, add current line to previous token
        if not current_token_name:
            raise ValueError('Unclassified text: ' + line)
        emit_text(line)

    end_current_token()

    if not type_['related_headers']:
        del type_['related_headers']

    # entries marked 'manual' couldn't be processed right and have to be hand-imported
    if type_['manual']:
        return entry, type_

    return new_entry, type_

def output_entries(classified_entries):
    for entry, type_ in classified_entries:
        print("***" + json.dumps(type_))
        for line in entry:
            print(line, end='')
        print()


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

