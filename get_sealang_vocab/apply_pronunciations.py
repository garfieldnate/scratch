import json
import sys
from time import sleep

from bs4 import BeautifulSoup
# like namedtuple but mutable
from namedlist import namedlist
import requests

Vocab = namedlist('vocab', ['cat', 'rank', 'thai', 'english', 'sentence', 'pronunciation'])
def read_vocab(vocab_file):
    vocab = []
    for line in open(vocab_file, 'r'):
        line = line.strip()
        fields = line.split('|')
        # write None where pronunciations are missing
        if len(fields) == 6:
            vocab.append(Vocab(*fields))
        else:
            vocab.append(Vocab(*fields, None))
    return vocab

wiktionary_url = "https://en.wiktionary.org/wiki/"

nlpl_thai_url = 'http://localhost:5000/api/v1/tokenize/th'

def tokenize_word(sentence):
    response = json.loads(requests.post(nlpl_thai_url, json={"text": sentence}).text)
    return [t['original'] for t in response['result']['tokens']]

def fetch_word_page(word):
    url = wiktionary_url + word
    response = requests.get(url).text
    return response

def get_pronunciation(word):
    try:
        html = fetch_word_page(word)
        parsed = BeautifulSoup(html, features="lxml")
        if parsed.find(class_="noarticletext"):
            # print(f"no wiktionary entry for {word}", file=sys.stderr)
            return None
        paiboon_el = parsed.find('a', text='Paiboon')
        pronunciation = paiboon_el.find_next('td').findChild('span').text
        return pronunciation
    except Exception as e:
        print(f"Couldn't find pronunciation in page for {word}", file=sys.stderr)
    return None

def get_pronunciations_splitting(word):
    tokens = tokenize_word(word)
    return [get_pronunciation(t) or '???' for t in tokens]

def get_all_pronuncations(vocab):
    for v in vocab:
        if v.pronunciation:
            continue
        pron = get_pronunciation(v.thai)
        if pron is None:
            tokens = tokenize_word(v.thai)
            if len(tokens) > 1:
                tokenized_pron = [get_pronunciation(t) or '???' for t in tokens]
                v.pronunciation = ' '.join(tokenized_pron)
                print(f'Setting tokenized pronuncation of {v.thai} ({v.english}) ({v.cat}) to {tokenized_pron}', file=sys.stderr)
            else:
                print(f"no wiktionary entry for {v.thai} ({v.english}) ({v.cat})", file=sys.stderr)
                v.pronunciation = '???'
        else:
            v.pronunciation = pron
        sleep(1)

def print_vocab(vocab):
    total_prons = 0
    for v in vocab:
        print('|'.join([v.cat, v.rank, v.thai, v.english, (v.sentence or ''), (v.pronunciation or '')]))
        if v.pronunciation:
            total_prons += 1
    print(f"{total_prons}/{len(vocab)} vocab had pronunciations", file=sys.stderr)

def main(vocab_file):
    vocab = read_vocab(vocab_file)
    get_all_pronuncations(vocab)
    print_vocab(vocab)

if __name__ == '__main__':
    main(sys.argv[1])
