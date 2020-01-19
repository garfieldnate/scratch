# Abandon! Tries to tokenize and parse all at once and fails miserably
from collections import namedtuple
import sys

from pprint import PrettyPrinter
from pyparsing import alphas, Word, nums, oneOf, SkipTo, Combine, tokenMap, Suppress, Literal, Optional, delimitedList, restOfLine, ZeroOrMore, ParseResults, OneOrMore, LineEnd, NotAny

printer = PrettyPrinter(indent=4)

def process_usage(string, location, parse_tree):
    usage = {'genre': parse_tree['genre']}
    if 'common' in parse_tree:
        usage['occurence'] = 'common'
    else:
        usage['occurence'] = 'uncommon'
    # print(f'Usage: returning {usage}')
    return usage


def buildTree(string, location, parse_tree):
    node = {}

    # Must handle strings, lists and dicts; ParserResults objects have to be classified as dicts or lists

    # strings
    if isinstance(parse_tree, str):
        # get rid of extra whitespace
        return " ".join(parse_tree.split())

    # lists
    treat_as_list = isinstance(parse_tree, list) or \
        (isinstance(parse_tree, ParseResults) and not parse_tree.haskeys())
    if treat_as_list:
        return [buildTree(None, None, t) for t in parse_tree]

    # dicts
    for k,v in parse_tree.items():
        node[k] = buildTree(None, None, v)

    return node




bullet = Suppress(Word("•"))#.setParseAction(buildTree)
bullet_text = (bullet + SkipTo(Word(nums) | bullet)('example')).setParseAction(buildTree)
score = Word(nums)('score')#.setParseAction(buildTree)

rank = Word(nums)('rank').setParseAction(buildTree)
pos = oneOf("adj adv art aux conj inf interj num part prep pron verb der die das", asKeyword=True)('pos').setParseAction(buildTree)
unified_headword = SkipTo(pos, failOn=Word(nums) | bullet)('unified_headword').setParseAction(buildTree)
english = SkipTo('\n')('english').setParseAction(buildTree)
unified_header = (rank + unified_headword + pos + english).setParseAction(buildTree)

# lettered_header = (rank + SkipTo(pos, failOn=Literal('(') | nums | bullet)('lettered_headword') + pos)
# lettered_subheader = Word('ab') + Literal(')') + restOfLine + Suppress(SkipTo(bullet))

subheader_number = Word(nums, max=1).setParseAction(buildTree)
# TODO: parse out English, German and POS if possible
numbered_subheader = (subheader_number + restOfLine + Suppress(SkipTo(bullet))).setParseAction(buildTree)
partial_headword = SkipTo(subheader_number).setParseAction(buildTree)
partial_header = (rank + partial_headword).setParseAction(buildTree)

genre = oneOf("A I L N S", asKeyword=True)('genre').setParseAction(buildTree)
common = (Literal('+')('common') + genre).setParseAction(process_usage)
uncommon = (Literal('–')('uncommon') + genre).setParseAction(process_usage) # Note: not a '-' character!
usage_el = (common | uncommon)('usage').setParseAction(buildTree)
# TODO: output structure wrong
usage = delimitedList(usage_el).setParseAction(buildTree)

subheader = (Combine(Word(alphas) + restOfLine) + Suppress(SkipTo(bullet)))('subheader').setParseAction(buildTree)

content = (bullet_text + score + Optional(usage))('content*').setParseAction(buildTree)

# lettered_bullet = (bullet + SkipTo(lettered_subheader | score))
# lettered_section = (lettered_subheader + lettered_bullet)('lettered_section')#.setDebug()

entry = ((unified_header + content + ZeroOrMore(subheader + content)) | 
         (partial_header + OneOrMore(numbered_subheader + 
                OneOrMore(bullet_text + Optional(score) + ZeroOrMore(subheader + content))))).setParseAction(buildTree)
 # | (lettered_header + lettered_section + lettered_section + score)

# strip extra whitespace stored in the SkipTo tokens
for el in [unified_headword, english, bullet_text]:
    el.setParseAction(tokenMap(str.strip))

samples = []
samples.append("""117 gegen prep against
    • Ich habe keine Chance gegen dich.
       798""")

samples.append("""235 gern, gerne adv (with a verb) enjoy
    • Meine Großeltern gehen gern in die Oper.
        372""")

samples.append("""3111 Mörder der murderer
     • Mörder können durch DNA-Analysen schnell
       gefunden werden.
        23 –A, –S""")

# Next: this structure is wrong
samples.append("""123 heißen verb to be called
    • Sie heißt Anja.
       740
    das heißt, d.h. that is, i.e.
    • Morgen Nachmittag muss ich zum Arzt,
      das heißt, ich habe keine Zeit.
       285""")

samples.append("""574 enthalten

    1 verb to contain
    • Die Creme enthält keine
      Konservierungsstoffe.
    2 enthalten (sich) to abstain
    • Ich enthalte mich der Stimme.

          148""")

samples.append("""589 pro
    1 prep per
    • Wir trinken pro Woche etwa einen Kasten
      Bier.
    2 Pro das pro
    • Pro und Contra sollte man gewissenhaft
      abwägen.
       145""")

samples.append("""126 erst
    1 adv ﬁrst, only, not until
    • Erst die Arbeit, dann das Vergnügen.
    2 part
    • Da geht’s erst richtig los.
       737
    erst mal ﬁrst
    • Darüber muss ich erst mal nachdenken.
       123""")

# Note: we do not handle entries with a)/b) sections; they complicate things, and there are only 10,
# so it is easier to process/import them manually

# def pprint(node, tab=""):
#     print(node)
    # print(f"node is {node[0]}, value is {node.value}, children are {node.children}")
    # if type(node) == Node:
    #     print(f"\t┗━ {node.value}")
    #     # print(node.value)
    #     # print(node.children)
    #     for child in node.children:
    #         pprint(child,  "\t    ")
    # else:
    #     # print(type(node))
    #     print(node)

def parse_file(file):
    # text = open(file).read()
    for sample in samples:
        tree = entry.parseString(sample, parseAll=True)
        # print(tree.dump())
        # print(tree)
        printer.pprint(tree[0])
        # print(type(tree.value))
        # pprint(tree[0])


def main(argv):
    if len(argv) != 2:
        raise ValueError("Usage: python3 parse_germ.py <file>")
    parse_file(argv[1])

if __name__ == '__main__':
    main(sys.argv)

