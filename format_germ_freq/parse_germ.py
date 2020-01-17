import sys

from pyparsing import alphas, Word, nums, oneOf, SkipTo, Combine, tokenMap, Suppress, Literal, Optional, delimitedList

rank = Word(nums)('rank')
pos = oneOf("adj adv art aux conj inf interj num part prep pron verb der die das", asKeyword=True)('pos')
headword = SkipTo(pos)('headword')
english = SkipTo('\n')('english')
header = rank + headword + pos + english
bullet_text = Suppress(Word("•")) + SkipTo(Word(nums))('example')
score = Word(nums)('score')

genre = oneOf("A I L N S")('genre')
common = Literal('+')('common') + genre
uncommon = Literal('–')('uncommon') + genre # Note: not a '-' character!
usage_el = (common | uncommon)('usage_el')
# TODO: output structure wrong
usage = delimitedList(usage_el)('usage')


entry = header + bullet_text + score + Optional(usage)



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

# samples.append("""123 heißen verb to be called
#     • Sie heißt Anja.
#        740
#     das heißt, d.h. that is, i.e.
#     • Morgen Nachmittag muss ich zum Arzt,
#       das heißt, ich habe keine Zeit.
#        285""")



def parse_file(file):
    # text = open(file).read()
    for sample in samples:
        tree = entry.parseString(sample, parseAll=True)
        print(tree.dump())
    # usage.parseString('–A, +S').pprint()


def main(argv):
    if len(argv) != 2:
        raise ValueError("Usage: python3 parse_germ.py <file>")
    parse_file(argv[1])

if __name__ == '__main__':
    main(sys.argv)

