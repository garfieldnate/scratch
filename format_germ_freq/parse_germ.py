from collections import namedtuple
import sys

from pyparsing import alphas, Word, nums, oneOf, SkipTo, Combine, tokenMap, Suppress, Literal, Optional, delimitedList, restOfLine, ZeroOrMore, ParseResults

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




rank = Word(nums)('rank')#.setParseAction(buildTree)
pos = oneOf("adj adv art aux conj inf interj num part prep pron verb der die das", asKeyword=True)('pos')#.setParseAction(buildTree)
headword = SkipTo(pos)('headword')#.setParseAction(buildTree)
english = SkipTo('\n')('english')#.setParseAction(buildTree)
header = (rank + headword + pos + english)#.setParseAction(buildTree)
bullet = Suppress(Word("•"))#.setParseAction(buildTree)
bullet_text =( bullet + SkipTo(Word(nums))('example'))#.setParseAction(buildTree)
score = Word(nums)('score')#.setParseAction(buildTree)

genre = oneOf("A I L N S", asKeyword=True)('genre')#.setParseAction(buildTree)
common = (Literal('+')('common') + genre)#.setParseAction(buildTree)
uncommon = (Literal('–')('uncommon') + genre)#.setParseAction(buildTree) # Note: not a '-' character!
usage_el = (common | uncommon)('usage_el')#.setParseAction(buildTree)
# TODO: output structure wrong
usage = delimitedList(usage_el)('usage')#.setParseAction(buildTree)

subheader = (Combine(Word(alphas) + restOfLine) + Suppress(SkipTo(bullet)))#.setParseAction(buildTree)

content = (bullet_text + score + Optional(usage))('content')#.setParseAction(buildTree)

entry = (header + content + ZeroOrMore(subheader + content))#.setParseAction(buildTree)

# strip extra whitespace stored in the SkipTo tokens
for el in [headword, english, bullet_text]:
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
    # usage.parseString('–A, +S').pprint()


def main(argv):
    if len(argv) != 2:
        raise ValueError("Usage: python3 parse_germ.py <file>")
    parse_file(argv[1])

if __name__ == '__main__':
    main(sys.argv)

