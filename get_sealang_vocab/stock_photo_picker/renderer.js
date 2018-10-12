const getModel = require('./model').getModel;
const utils = require('./utils');

// HAHA GLOBALS! I'm so evil!!!
var state = {
    currentlySelected: 0,
    allVocab: [],
    page: null,
    // TODO
    nextStateData: {}
};

const resetPage = (vocab) => {
    document.getElementById("vocab-header").innerHTML = `${vocab.definition} (${vocab.headword})`;
    document.getElementById("vocab-pronunciation").innerHTML = vocab.pronunciation;
    document.getElementById("vocab-images").innerHTML = '';
    document.getElementById("vocab-audio").innerHTML = '<p>fetching audio...</p>';
    document.getElementById("vocab-images-google").innerHTML = '';
    document.getElementById("vocab-image-downloaded").innerHTML = '';
    document.getElementById("save-notifier").innerHTML = '';
    document.getElementById("more-images-query").value = '';
}

const constructImageQuery = (vocab) => {
    // remove parentheticals from definition to simplify query
    var query = vocab.definition.replace(/ *\(.*/g, "");
    // remove leading meaningless words (gets better results)
    query = query.replace(/^to /,"");
    query = query.replace(/^the /,"");
    query = query.replace(/^a /,"");
    return query;
}

// get from pexels if possible, else google images
const getImagesFromPexelsWithFallback = async query => {
    return await utils.scrapeImageUrls(state.page, query).then(async imageUrls => {
        if(imageUrls.length === 0) {
            imageUrls = await utils.scrapeGoogleImageUrls(state.nextStateData.vocab.headword);
            // 100 is way too many
            imageUrls.length = Math.min(imageUrls.length, 30);
            return imageUrls;
        } else {
            return imageUrls;
        }
    });
}

// next: store basd64 data in nextStateData
const loadResourcesForNextPage = async () => {
    if(state.currentlySelected === state.allVocab.length) {
        console.log("Finished editing vocab data");
        // will error at the end but who cares
        state.nextStateData = {};
    }

    const vocab = state.allVocab[state.currentlySelected + 1];
    state.nextStateData.vocab = vocab;

    const query = constructImageQuery(vocab);
    console.log(`querying Pexels for ${query}`);
    var imageUrls = await getImagesFromPexelsWithFallback(query);
    state.nextStateData.images = Promise.all(
        imageUrls.map(url => {
            return utils.downloadUrlAsBase64(url).then(base64data => {
                return {url: url, base64data: base64data};
            })
        })
    );
    console.log(state.nextStateData.images);

    state.nextStateData.audioUrls = utils.scrapeAudioUrls(vocab.headword)
}

const setMoreImagesListener = (vocab) => {
    const button = document.getElementById("more-images-loader");
    button.onclick = () => {
        var query = document.getElementById("more-images-query").value;
        if(!query) {
            query = vocab.headword;
        }
        utils.scrapeGoogleImageUrls(query).then(imageUrls => {
            // 100 is way too many
            imageUrls.length = Math.min(imageUrls.length, 20);
            downloadAndDisplayImages(imageUrls, vocab, document.getElementById("vocab-images-google"));
       });
    }
    // press enter to search
    document.getElementById("more-images-query").addEventListener("keyup", function(event) {
        event.preventDefault();
        if (event.keyCode === 13) {
            button.click();
        }
    });
}

const stripDatatypeFromBase64MimeString = (base64data) => {
    return base64data.replace(/.+;base64,/, "");
}

const imageSelected = async (vocab, url, base64data) => {
    // console.log("clicked " + url);
    await vocab.updateAttributes({image_url: url, image_base64: stripDatatypeFromBase64MimeString(base64data)});
    document.getElementById("save-notifier").innerHTML += '<p>Image saved to DB!';
}

const displayImages= (vocab, container, images) => {
    container.innerHTML = '<p>fetching images...</p>';
    console.log(images);
    images.forEach(image => {
        var img = document.createElement('img');
        img.src = image.base64data;
        img.setAttribute("data-original-src", image.url);
        img.onclick = async () => {await imageSelected(vocab, image.url, image.base64data);}
        container.appendChild(img);
    });
}

const downloadAndDisplayImages = async (imageUrls, vocab, container) => {
    container.innerHTML = '<p>fetching images...</p>';
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
    // console.log("clicked " + url);
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

                var audioSelector = document.createElement('button');
                audioSelector.setAttribute('type', 'button');
                audioSelector.innerHTML = 'Select Audio';
                audioSelector.onclick = async () => {await audioSelected(vocab, url, base64data);}
                singleAudioContainer.appendChild(audioSelector);

                var audio = document.createElement('AUDIO');
                audio.src = base64data;
                audio.setAttribute("data-original-src", url);
                audio.setAttribute("controls", "controls");
                singleAudioContainer.appendChild(audio);
            })
        })
    );
}

const displayManualImageInput = vocab => {
    const container = document.getElementById("vocab-image-manual");
    container.innerHTML = '';

    const textInput = document.createElement("input");
    textInput.setAttribute("type", "text");
    textInput.setAttribute("id", "vocab-image-manual-input");
    container.appendChild(textInput);

    // const textInput = document.getElementById("vocab-image-manual-input");
    var manualInputTrigger = document.createElement('button');
    manualInputTrigger.setAttribute('type', 'button');
    manualInputTrigger.innerHTML = 'Download from URL';
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

    // press enter to download
    textInput.addEventListener("keyup", function(event) {
        event.preventDefault();
        if (event.keyCode === 13) {
            manualInputTrigger.click();
        }
    });
}

const displayPage = async () => {
    const vocab = state.nextStateData.vocab;
    resetPage(vocab);
    // console.log(vocab.toJSON());
    displayManualImageInput(vocab);
    setMoreImagesListener(vocab);
    displayImages(vocab, document.getElementById("vocab-images"), await state.nextStateData.images);
    const audioUrls = await state.nextStateData.audioUrls;
    await downloadAndDisplayAudio(audioUrls, vocab);
    window.scrollTo(0,0);
}

const goToNextVocab = async () => {
    state.currentlySelected++;
    await displayPage();
    loadResourcesForNextPage();
}

const run = async (dbFile) => {
    const vocabModel = (await getModel(dbFile)).Vocab;
    const browser = await utils.openBrowser();
    state.page = await browser.newPage();
    state.allVocab = (await vocabModel.all()).filter(v => v.image_url === null); // || v.audio_url === null

    document.getElementById('next').onclick = () => goToNextVocab();
    state.currentlySelected = -1;
    await loadResourcesForNextPage();
    goToNextVocab();
}

module.exports = {
    run: run
}
