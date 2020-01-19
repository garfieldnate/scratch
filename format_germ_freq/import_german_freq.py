# Imports the vocab into the local tango DB; input is the output of format_germ_freq.py
from collections import namedtuple
import sys

from bs4 import BeautifulSoup


def extract_vocab(soup):
    for entry in soup.find_all('div', 'entry'):
        v = {}
        
        v['rank'] = entry.find('span', 'rank').text
        # TODO: fix exraction of scores next to bias markers
        # v['score'] = entry.find('span', 'score').text
        # TODO: extract and import bias markers

        # TODO: fix bias markers being combined with examples
        v['examples'] = []
        for ex in entry.find_all('span', 'example'):
            v['examples'].append(ex.text.replace('\n', ' '))

        v['pos'] = []
        for pos in entry.find_all('span', 'pos'):
            v['pos'].append(pos.text)

        v['art'] = []
        for art in entry.find_all('span', 'art'):
            v['art'].append(art.text)

        print(v)
        # print(entry)


def import_vocab(vocab):
    for v in vocab:
        print(v)

def main(argv):
    if len(argv) != 2:
        print("Usage: python3 import_german_freq.py <content.html>")
        sys.exit()

    with open(argv[1]) as f:
        soup = BeautifulSoup(f, 'lxml')
        vocab = extract_vocab(soup)
        import_vocab(vocab)
    print(argv[1])

if __name__ == '__main__':
    main(sys.argv)
