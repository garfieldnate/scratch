# Requires python 3.8
# Split columns in the Zamzar text conversion of _A Frequency Dictionary of German: Core Vocabulary for Learners_
# Assuming pre-removal of extra matter (intro, index, and themed collocation/frequency lists)
# Pages are assumed to be split with 0x0C (form feed). 

import sys
import re
# pattern.match(string)

POS = ["adj", "adv", "art", "aux", "conj", "inf", "interj", "num", "part", "prep", "pron", "verb", "der", "die", "das"]
ART = {"der", "die", "das"}
NEXT_SCREEN = '<br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>'
# rank and German, followed optionally by POS and English
headword_pattern = re.compile(f"^(?P<rank>\\d+) (?P<headword>.+?)(?: (?P<pos>{'|'.join(POS)}) (?P<meaning>.+))?$")
# leading space followed by the index of the meaning, the POS and the meaning
polysemous_headword_pattern = re.compile(f"^\\s+(?P<index>\\d+) (?P<pos>{'|'.join(POS)}) (?P<meaning>.+)$")
secondary_meaning_pattern = re.compile(f"^\\s+[a-z]\\).+$")
frequency_score_pattern = re.compile(f"^\\s+(?P<score>[0-9,]+)$")
contraction_pattern = re.compile(f'^\\s+(?P<contraction>\\w+) (?P<meaning>.+)')
# print(headword_pattern)

GENRE = ["A", "I", "L", "N", "S"]


def lstrip_page(lines):
    """Remove common whitespace from the input lines"""
    margin = min([len(l) - len(l.lstrip()) if len(l) else 100 for l in lines])
    # print(f"margin is {margin}")
    new_lines = [l[margin:] for l in lines]
    # print(new_lines)
    return new_lines

def process_page(line_num, page_num, lines):
    # print(f"found page {page_num} at line {line_num}")
    stripped_lines = lstrip_page(lines)

    split_index = find_column_split_index(stripped_lines)
    # print(f"Page {page_num} (through line {line_num}) is split at char {split_index}")
    single_col_lines = split_cols(stripped_lines, split_index)
    # for line in single_col_lines:
    #     print(line)
    # sys.exit()
    # final_lines = [l.rstrip() for l in single_col_lines]
    output_new_lines(single_col_lines)


def find_column_split_index(lines):

    """Finds the character index at which the input lines containing two collumns of text are split.
    Scans all lines on the page from right to find first a "•" (bullet point) and then a number (the frequency ranking). 
    After the ranking is found, continues to scan left to find an index at which all lines contain whitespace. This index 
    is returned."""

    bullet_found = False
    ranking_found = False
    max_line_length = max([len(x) for x in lines])
    # I guess Python doesn't have labeled loops *shrug*
    class ContinueCharIndexLoop(Exception):
        pass

    for i in range(max_line_length, -1, -1):
        try:
            all_whitespace = True
            for line in lines:
                if i >= len(line):
                    continue

                if line[i] == "•":
                    bullet_found = True
                    ranking_found = False
                    # print(f'found bullet at {i}; reset ranking_found to false')
                    raise ContinueCharIndexLoop

                if bullet_found and line[i].isdigit():
                    ranking_found = True
                    # necessary because sometimes the bullets aren't aligned
                    all_whitespace = False
                    # print(f'found digit after bullet at {i} in line {line}')

                if ranking_found and not line[i].isspace():
                    all_whitespace = False

        except ContinueCharIndexLoop:
            pass
        if ranking_found and all_whitespace:
            # print(f'ranking found and all whitespace at {i}')
            return i

    raise ValueError("Could not find split index")


def split_cols(lines, index):
    left_col = []
    right_col = []
    for line in lines:
        left_line = line[0:index]
        # column at index is ommitted because it is whitespace
        right_line = line[index + 1:] 
        left_col.append(left_line.rstrip())
        right_col.append(right_line.rstrip())

    return left_col + right_col


# TODO: This is pretty silly. If further work is needed, just parse out the entries properly and then print the HTML in a separate step.
# TODO: there should be 4034 entries, but we are only printing 4011 div elements
def output_new_lines(lines):
    # print all non-empty lines as-is
    for line in lines:
        if line.strip():
            print(line)

    # try to parse lines and print as HTML
    # print('<!DOCTYPE html>')
    # print('<head><meta charset="utf-8"></head>')
    # print('<style>body { font-size: 60pt; }</style>')
    # in_entry = False
    # saw_frequency_score = False
    # close_prev = ''
    # for line in lines:
    #     if not line:
    #         if close_prev:
    #             print(close_prev)
    #             close_prev = ''
    #         continue
    #     if (match := headword_pattern.match(line)):
    #         if close_prev:
    #             print(close_prev)
    #             close_prev = ''
    #         if in_entry:
    #             print("</div>")
    #         print(NEXT_SCREEN)
    #         in_entry = True
    #         saw_frequency_score = False
    #         print("<div class='entry'>")
    #         close_prev = output_headword(match)
    #     elif (match := polysemous_headword_pattern.match(line)):
    #         if close_prev:
    #             print(close_prev)
    #             close_prev = ''
    #         close_prev = output_single_meaning(match)
    #     elif (match := secondary_meaning_pattern.match(line)):
    #         if close_prev:
    #             print(close_prev)
    #             close_prev = ''
    #         close_prev = output_secondary_meaning(match)
    #     elif (match := frequency_score_pattern.match(line)):
    #         if close_prev:
    #             print(close_prev)
    #             close_prev = ''
    #         output_frequency_score(match)
    #         saw_frequency_score = True
    #     elif line.lstrip()[0] == "•":
    #         if close_prev:
    #             print(close_prev)
    #             close_prev = ''
    #         close_prev = output_example(line.lstrip())
    #     elif saw_frequency_score and contraction_pattern.match(line):
    #         if close_prev:
    #             print(close_prev)
    #             close_prev = ''
    #         saw_frequency_score = False
    #         close_prev = output_contraction_header(contraction_pattern.match(line))
    #     else:
    #         print(line.lstrip())
    # print(close_prev)
    # print("</div>")

def output_headword(match):
    print('<h1>' + '<span class="rank">' + match.group('rank') + '</span> ' + '<span class="headword">' + match.group('headword'))
    if(pos := match.group('pos')):
        print('</span>' + '</h1>')
        # plenty of space so we can quiz ourselves before scrolling down
        print(NEXT_SCREEN)
        print('<h1>' + get_pos_html(pos) + '<span class="meaning">' + match.group('meaning'))

    return '</span>' + '</h1>'


def get_pos_html(pos):
    if pos in ART:
        return f'<span class="pos">noun</span>, <span class="art">{pos}</span>; '
    else:
        return f'<span class="pos">{pos}</span>; '


def output_single_meaning(match):
    print(NEXT_SCREEN)

    print('<h1>' + '<span class="index">' + match.group('index') + '</span> ' + get_pos_html(match.group('pos')) + '<span class="meaning">' + match.group('meaning'))
    return  '</span>' + '</h1>'


def output_secondary_meaning(match):
    print('<h1>' + '<span class="meaning">' + match.group(0).lstrip())
    return '</span>' + '</h1>'


def output_frequency_score(match):
    print('<br/>' + '<span class="score">' + match.group('score') + '</span>')
    return None


def output_example(line):
    print(f'<br/><span class="example">{line}')
    return '</span>'

def output_contraction_header(match):
    print(f'<br/><h1><span class="contraction">{match.group("contraction")}</span> <span class="meaning">{match.group("meaning")}')
    return '</span></h1>'

def main(argv):
    if len(argv) != 2:
        raise ValueError("Usage: python3 format_germ_freq.py <input_text>")


    input_file = argv[1]
    line_num = 0
    page_num = 0
    page_lines = []
    for line in open(input_file, 'r'):
        line_num += 1
        if line.startswith('\x0c'):
            # break
            page_num += 1
            process_page(line_num, page_num, page_lines)
            page_lines = []
        else:
            page_lines.append(line.rstrip())
    page_num += 1
    process_page(line_num, page_num, page_lines)


if __name__ == '__main__':
    main(sys.argv)

