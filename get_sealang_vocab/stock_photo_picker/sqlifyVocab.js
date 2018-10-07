// Read the vocab file so far and put it in a sqlite database
// usage: node sqlifyVocab.js vocab.csv vocab.db
const fs = require('fs');
const getModel = require('./model').getModel;


const readLines = (file) =>
    fs.readFileSync(file, 'utf-8').split(/\r?\n/).slice(0,-1);

const parseVocab = (line) => {
    const fields = line.split('|');
    return {
        'notes': `category: ${fields[0]}, webRank: ${fields[1]}, source: http://www.sealang.net/thai/vocabulary/`,
        'headword': fields[2],
        'definition': fields[3],
        'example': fields[4],
        'pronunciation': fields[5]}
}
const readVocab = (vocabFile) => {
    const lines = readLines(vocabFile);
    return lines.map((line) => parseVocab(line));
}

const main = async (args) => {
    const vocabFile = args[0];
    const dbFile = args[1];
    const vocab = readVocab(vocabFile);
    const model = await getModel(dbFile);
    for (const v of vocab) {
        model.Vocab.create(v)
            .then(vocab => {
                console.log(vocab.toJSON());
            });
    }
}

if (!module.parent) {
    main(process.argv.slice(2));
}
