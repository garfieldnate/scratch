from collections import namedtuple
import sys

from pyparsing import alphas, Word, nums, oneOf, SkipTo, Combine, tokenMap, Suppress, Literal, Optional, delimitedList, restOfLine, ZeroOrMore, ParseResults, OneOrMore, LineEnd, NotAny

# Node = namedtuple("Node", ["value", "children"])
# def buildTree(string, location, tokens):
#     return tokens
    # node = {}
    # for k,v in tokens.items():
    #     # print(k,v)
    #     if(type(v) == ParseResults):
    #         node[k] = buildTree(None, None, v)
    #     else:
    #         node[k] = v
    # print(node)
    # return node

    # print(list(tokens.items()))
    # print(tokens)

    # if len(tokens) > 1:
    #     return Node(value=tokens[0], children=tokens[1:])
    # elif len(tokens) == 1:
    #     return tokens[0]
    # else:
    #     return None




bullet = Suppress(Word("•"))#.setParseAction(buildTree)
bullet_text =(bullet + SkipTo(Word(nums) | bullet)('example'))#.setParseAction(buildTree)
score = Word(nums)('score')# + NotAny(Word(alphas))#.setDebug()#.setParseAction(buildTree)

rank = Word(nums)('rank')#.setParseAction(buildTree)
pos = oneOf("adj adv art aux conj inf interj num part prep pron verb der die das", asKeyword=True)('pos')#.setParseAction(buildTree)
unified_headword = SkipTo(pos, failOn=Word(nums) | bullet)('unified_headword')#.setParseAction(buildTree)
english = SkipTo('\n')('english')#.setParseAction(buildTree)
unified_header = (rank + unified_headword + pos + english)#.setParseAction(buildTree)

lettered_header = (rank + SkipTo(pos, failOn=Literal('(') | nums | bullet)('lettered_headword') + pos)
lettered_subheader = Word('ab') + Literal(')') + restOfLine + Suppress(SkipTo(bullet))

subheader_number = Word(nums, max=1)
# TODO: parse out English, German and POS if possible
numbered_subheader = subheader_number + restOfLine + Suppress(SkipTo(bullet))
partial_headword = SkipTo(subheader_number)
partial_header = (rank + partial_headword)

genre = oneOf("A I L N S", asKeyword=True)('genre')#.setParseAction(buildTree)
common = (Literal('+')('common') + genre)#.setParseAction(buildTree)
uncommon = (Literal('–')('uncommon') + genre)#.setParseAction(buildTree) # Note: not a '-' character!
usage_el = (common | uncommon)('usage_el')#.setParseAction(buildTree)
# TODO: output structure wrong
usage = delimitedList(usage_el)('usage')#.setParseAction(buildTree)

subheader = (Combine(Word(alphas) + restOfLine) + Suppress(SkipTo(bullet)))#.setDebug()#.setParseAction(buildTree)

content = (bullet_text + score + Optional(usage))('content')#.setDebug()#.setParseAction(buildTree)

lettered_bullet = (bullet + SkipTo(lettered_subheader | score))
lettered_section = (lettered_subheader + lettered_bullet)('lettered_section')#.setDebug()

entry = ((unified_header + content + ZeroOrMore(subheader + content)) | (partial_header + OneOrMore(numbered_subheader + OneOrMore(bullet_text + Optional(score) + ZeroOrMore(subheader + content)))) | (lettered_header + lettered_section + lettered_section + score))#.setDebug()#.setParseAction(buildTree)

# entry = ((unified_header + content + ZeroOrMore(Optional(subheader) + content)) | (partial_header + OneOrMore(numbered_subheader + bullet_text) + score))#.setDebug()#.setParseAction(buildTree)

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

# Note: I moved (clothes) up a line because it seems to be the only place where the definition spans two lines
samples.append("""2302 ausziehen verb a) to move out, take off (clothes)
      • Nasse Strümpfe sollte man ausziehen, damit
        man sich nicht erkältet.
        b) ausziehen (sich) to undress, get
        undressed

      • Die Kinder ziehen sich vor dem
        Mittagsschlaf aus.
        34""")

samples.append("""126 erst
    1 adv ﬁrst, only, not until
    • Erst die Arbeit, dann das Vergnügen.
    2 part
    • Da geht’s erst richtig los.
       737
    erst mal ﬁrst
    • Darüber muss ich erst mal nachdenken.
       123""")

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
        print(tree.dump())
        # print(type(tree.value))
        # pprint(tree[0])


def main(argv):
    if len(argv) != 2:
        raise ValueError("Usage: python3 parse_germ.py <file>")
    parse_file(argv[1])

if __name__ == '__main__':
    main(sys.argv)

