import random

random.seed(0) # deterministic behavior across runs

from tango.model import get_model

# Output 100 German words and 10 each of the other available languages
focus_lang = 'de'
number_focus_lang = 100
number_other_langs = 10

model = get_model()

# TODO: add accessor for this field
languages = model._all_languages
# print(languages)

# TODO: too bad you can't tell what language the returned tango belong to T_T
# tango = model.get_tango_for_language('all')

all_tango = {lang: model.get_tango_for_language(lang) for lang in languages}
# shuffle once so that all words for a language are random
for lang in all_tango.keys():
    random.shuffle(all_tango[lang])

output_tango = []
while True:
    section = []
    has_words_left = False
    for _ in range(number_focus_lang):
        if all_tango[focus_lang]:
            tango = all_tango[focus_lang].pop()
            tango['lang'] = focus_lang
            section.append(tango)
            has_words_left = True
    for lang in languages:
        if lang == focus_lang:
            continue
        for _ in range(number_other_langs):
            if all_tango[lang]:
                tango = all_tango[lang].pop()
                tango['lang'] = lang
                section.append(tango)
                has_words_left = True

    # shuffle again so that the different language words are mixed together
    random.shuffle(section)
    output_tango.extend(section)

    if not has_words_left:
        break

def print_css():
    print("<style>")
    print("    .pagebreak {")
    print("        clear: both;")
    print("        page-break-after: always;")
    print("        height: 100vh;")
    print("    }")
    print("</style>")

def page_break():
    print("<div class='pagebreak'> </div>")

# print([t['headword'] for t in output_tango])
print("<!DOCTYPE html>")
print_css()
newline = "\n"
for tango in output_tango:
    print(f"<div id={tango['lang']}-{tango['id']}>")
    print(f"<p lang={tango['lang']}><span class='lang'>{tango['lang']}</span> {tango['headword']}</p>")
    if tango['pronunciation'] and tango['pronunciation'] != tango['headword']:
        print(f"<p class={field}>{tango['pronunciation']}</p>")
    for field in ["morphology", "definition", "example", "notes"]:
        if tango[field]:
            print(f"<p class={field}>{tango[field].replace(newline, '<br/>')}</p>")

    print(f"</div>")
    page_break()
