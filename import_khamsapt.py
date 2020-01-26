# Import CSV vocab output from ThaiDict app
# Not sure why, but you may have to wait minutes before seeing the update in the DB
import csv
import sys


from tango import model

model = model.get_model()


def row_to_tango(row):
    v = {
        'headword': row['th'], 
        'pronunciation': row['pron'],
        'morphology': row['pos'],
        'source': 'TDA: ' + row['link'],
        'image_url': '',
        'image_base64': '',
        'example': ''}

    # use bullet points if multiple definitions were provided
    defs = row['en'].split(' | ')
    def_text = '' if len(defs) == 1 else '• '
    def_text += '\n• '.join(defs)
    v['definition'] = def_text

    notes = []
    if row['cat']:
        notes.append('category: ' + row['cat'])
    if row['usage']:
        notes.append('usage: ' + row['usage'])
    v['notes'] = '\n'.join(notes)
    return v


def read_tango(file):
    tango = []
    with open(file) as f:
        reader = csv.DictReader(f, dialect='unix', fieldnames=['en', 'th', 'pron', 'usage', 'pos', 'cat', 'link'])
        for row in reader:
            tango.append(row_to_tango(row))
    return tango

def import_tango(tango):
    for t in tango:
        print(f"Importing {t}")
        model.add_tango('th', t)

def main(argv):
    if len(argv) != 2:
        print('Usage: python3 import_thaidict.py <csv file>')
        exit()
    tango = read_tango(argv[1])
    import_tango(tango)
    # print(tango)


if __name__ == '__main__':
    main(sys.argv)
