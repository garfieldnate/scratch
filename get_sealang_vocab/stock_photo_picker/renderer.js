const getModel = require('./model').getModel;
const utils = require('./utils');

// HAHA GLOBALS! I'm so evil!!!
var state = {
    currentlySelected: 0,
    allVocab: [],
    page: null,
};

const resetPage = (vocab) => {
    document.getElementById("vocab-header").innerHTML = `${vocab.definition} (${vocab.headword})`;
    document.getElementById("vocab-pronunciation").innerHTML = vocab.pronunciation;
    document.getElementById("vocab-images").innerHTML = '<p>fetching images...</p>';
    document.getElementById("vocab-audio").innerHTML = '<p>fetching audio...</p>';
    document.getElementById("vocab-image-downloaded").innerHTML = '';
    document.getElementById("save-notifier").innerHTML = '';
}

const stripDatatypeFromBase64MimeString = (base64data) => {
    return base64data.replace(/.+;base64,/, "");
}

const imageSelected = async (vocab, url, base64data) => {
    console.log("clicked " + url);
    await vocab.updateAttributes({image_url: url, image_base64: stripDatatypeFromBase64MimeString(base64data)});
    document.getElementById("save-notifier").innerHTML += '<p>Image saved to DB!';
}

const downloadAndDisplayImages = async (imageUrls, vocab) => {
    const container = document.getElementById("vocab-images");
    await Promise.all(
        imageUrls.map(url => {
            return utils.downloadUrlAsBase64(url).then(base64data => {
                var img = document.createElement('img');
                img.src = base64data;
                img.setAttribute("data-original-src", url);
                img.onclick = async () => {await imageSelected(vocab, url, base64data);}
                container.appendChild(img);
            })
        })
    );
}

const audioSelected = async (vocab, url, base64data) => {
    console.log("clicked " + url);
    await vocab.updateAttributes({audio_url: url, audio_base64: stripDatatypeFromBase64MimeString(base64data)});
    document.getElementById("save-notifier").innerHTML += '<p>Audio saved to DB!';
}

const downloadAndDisplayAudio = async (audioUrls, vocab) => {
    const container = document.getElementById("vocab-audio");
    await Promise.all(
        audioUrls.map(url => {
            return utils.downloadUrlAsBase64(url).then(base64data => {
                var singleAudioContainer = document.createElement('div');
                container.appendChild(singleAudioContainer);

                var audio = document.createElement('AUDIO');
                audio.src = base64data;
                audio.setAttribute("data-original-src", url);
                audio.setAttribute("controls", "controls");
                singleAudioContainer.appendChild(audio);

                var audioSelector = document.createElement('div');
                audioSelector.setAttribute('class', 'selector-square');
                audioSelector.onclick = async () => {await audioSelected(vocab, url, base64data);}
                singleAudioContainer.appendChild(audioSelector);
            })
        })
    );
}

const displayManualImageInput = vocab => {
    const container = document.getElementById("vocab-image-manual");
    container.innerHTML = '';

    const textInput = document.createElement("input");
    textInput.setAttribute('type', 'text');
    container.appendChild(textInput);

    var manualInputTrigger = document.createElement('div');
    manualInputTrigger.setAttribute('class', 'selector-square');
    manualInputTrigger.onclick = async () => {
        const url = textInput.value;
        const base64data = await utils.downloadUrlAsBase64(url);
        const downloadedContainer = document.getElementById("vocab-image-downloaded");
        downloadedContainer.innerHTML = '';
        const img = document.createElement("img");
        img.setAttribute("src", base64data);
        downloadedContainer.appendChild(img);
        await imageSelected(vocab, url, base64data);
    };
    container.appendChild(manualInputTrigger);
}

const displayPage = async (vocab) => {
    resetPage(vocab);
    console.log(vocab.toJSON());
    displayManualImageInput(vocab);
    // remove parentheticals from definition to simplify query
    var query = vocab.definition.replace(/ *\(.*/g, "");
    const imageUrls = await utils.scrapeImageUrls(state.page, query);
    await downloadAndDisplayImages(imageUrls, vocab);
    const audioUrls = await utils.scrapeAudioUrls(vocab.headword);
    await downloadAndDisplayAudio(audioUrls, vocab);
}

const run = async (dbFile) => {
    const vocabModel = (await getModel(dbFile)).Vocab;
    const browser = await utils.openBrowser();
    state.page = await browser.newPage();
    state.allVocab = (await vocabModel.all()).filter(v => v.image_url === null); // || v.audio_url === null
    state.currentlySelected = 0;
    document.getElementById('next').onclick = () => {
        state.currentlySelected++;
        if (state.currentlySelected !== state.allVocab.length) {
            const vocab = state.allVocab[state.currentlySelected];
            displayPage(vocab);
        }
    }
    displayPage(state.allVocab[state.currentlySelected]);
}

module.exports = {
    run: run
}
