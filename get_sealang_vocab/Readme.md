# Thai Vocab Deck Creator

Scripts for downloading vocab from sealang and inserting them in a sqlite DB. Very dirty, but was fun and fulfills a purpose (plus allowed me to try some new things). Won't work on anyone else's computer (required for Thai dictionary lookups and tokenization), and has a truly horrible interface for downloading pictures and audio for the deck.

* `get_sealang.pl` will download the initial csv.
* `apply_examples.py` will get examples from a text file (downloaded manually from Tatoeba) and from the local Mac dictionary app with Lexitron installed. Also requires that Thai NLPL is running locally.
* `apply_pronunciations.py` gets pronunciations from Wiktionary; also uses Thai NLPL.
* inside `stock_photo_picker`:
    - `node sqlifyVocab.js vocab.csv vocab.db` inserts the so-far-obtained info into a sqlite DB
    - `npm start` starts an electron app for downloading images and audio for the DB. Click on the pictures you want, or paste a link into box at the bottom and click the green square. Click a green square next to an audio controller to insert the audio data.

### What's next?

* scrape google images (filtering for free license) instead of just Pexels.
* pre-load the next screen while the user is editing the current screen
* finish manually creating the full deck
* possibly download more license-required info into the notes sections 
