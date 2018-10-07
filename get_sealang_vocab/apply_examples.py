import sys
import json
from collections import defaultdict
import subprocess
import re

# like namedtuple but mutable
from namedlist import namedlist
import requests

Vocab = namedlist('vocab', ['cat', 'rank', 'thai', 'english', 'sentence'])
def read_vocab(vocab_file):
    vocab = []
    for line in open(vocab_file, 'r'):
        line = line.strip()
        fields = line.split('|')
        vocab.append(Vocab(*fields, None))
    return vocab

nlpl_thai_url = 'http://localhost:5000/api/v1/tokenize/th'

def tokenize_sentence(sentence):
    response = json.loads(requests.post(nlpl_thai_url, json={"text": sentence}).text)
    return [t['original'] for t in response['result']['tokens']]

def check_sentence_length(tokens):
    # no use having a one-word example sentence!
    if len(tokens) == 1:
        print("skipping " + ''.join(tokens) + " because it only had one token", file=sys.stderr)
        return False
    # too long and I won't be able to understand it
    if len(tokens) > 20:
        print("skipping " + ''.join(tokens) + " because it had greater than 20 tokens", file=sys.stderr)
        return False
    return True

def format_sentence(tokens, author):
    # tokenize to make it easier for the user to read
    tokenized_string = '_'.join(tokens)
    # add attribution just in case
    return tokenized_string + '#' + author

def get_vocab_to_sentence_from_tatoeba(sentence_file, vocab_to_sentence):
    for line in open(sentence_file, 'r'):
        line = line.strip()
        tokens = tokenize_sentence(line)
        if not check_sentence_length(tokens):
            continue
        final_string = format_sentence(tokens, 'tatoeba')
        for token in tokens:
            vocab_to_sentence[token].append(final_string)

example_re = re.compile('Example: </span>([^<]+)</p>')
def get_sents_from_lexitron(vocab_to_sentence, vocab):
    cmd = ['/Users/nglenn/bin/mac_dic_lookup', 'LEXiTRON English-Thai, Thai-English', 'XXXXXXXX', 'html']
    for v in vocab:
        cmd[2] = v.thai
        result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('UTF-8')
        for match in example_re.finditer(result):
            tokens = tokenize_sentence(match.group(1))
            # Lexitron has lots of long sentences; don't want to throw away the data at this point
            # if not check_sentence_length(tokens):
            #     continue
            vocab_to_sentence[v.thai].append(format_sentence(tokens, 'LEXiTRON'))

def sort_sentences(vocab_to_sentence):
    # put the shortest sentences first for learning purposes!
    for sentences in vocab_to_sentence.values():
        sentences.sort(key=len)

def apply_sents_to_vocab(vocab_to_sentence, vocab):
    for v in vocab:
        if vocab_to_sentence[v.thai]:
            # don't reuse sentences
            v.sentence = vocab_to_sentence[v.thai].pop()

def print_vocab(vocab):
    total_sents = 0
    for v in vocab:
        print('|'.join([v.cat, v.rank, v.thai, v.english, (v.sentence or '')]))
        if v.sentence:
            total_sents += 1
    print(f"{total_sents}/{len(vocab)} vocab had example sentences", file=sys.stderr)

def main(sentence_file, vocab_file):
    vocab = read_vocab(vocab_file)
    vocab_to_sentence = defaultdict(lambda: list())
    get_sents_from_lexitron(vocab_to_sentence, vocab)
    get_vocab_to_sentence_from_tatoeba(sentence_file, vocab_to_sentence)
    sort_sentences(vocab_to_sentence)
    apply_sents_to_vocab(vocab_to_sentence, vocab)
    print_vocab(vocab)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
