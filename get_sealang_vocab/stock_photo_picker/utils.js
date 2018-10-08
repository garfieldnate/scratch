const cheerio = require('cheerio');
const fs = require('fs');
// required because Pexels is dynamic and won't render without a browser
const puppeteer = require('puppeteer');
const getModel = require('./model').getModel;

const openBrowser = async () => await puppeteer.launch({headless: true});

const pexelUrl = 'https://www.pexels.com/search/';
const scrapeImageUrls = async (page, query) => {
    const url = pexelUrl + encodeURIComponent(query) + '/';
    console.log("going to " + url);
    await page.goto(url);
    return await page.evaluate(pexelUrl => {
        let imageUrls = [];
        let elements = document.querySelectorAll('.photo-item__img');
        for (var element of elements){
            imageUrls.push(element.getAttribute('src'));
        }
        return imageUrls;
    }, pexelUrl);
}

// searches for images with permissive license
const googleImageUrl = "https://www.google.co.in/search?&source=lnms&tbm=isch&tbs=sur%3Afc&q="
const scrapeGoogleImageUrls = async (query) => {
    const url = googleImageUrl + encodeURIComponent(query);
    const res = await fetch(url, {
        headers: {
            'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
        }
    });
    const body = await res.text();
    const $ = cheerio.load(body);
    return $('div.rg_meta').map((i, el) => {
        const rg_meta = JSON.parse($(el).text());
        return rg_meta["ou"];
    }).get();
}

const forvoSearchUrl = 'https://forvo.com/word/'
const forvoAudioUrl = 'http://audio.forvo.com/mp3/'
//TODO: catch errors, return []
const scrapeAudioUrls = async (query) => {
    const url = forvoSearchUrl + encodeURIComponent(query);
    console.log(url);
    const res = await fetch(url);
    const body = await res.text();
    const $ = cheerio.load(body);
    return $('.play').map((i, el) => {
        // looks like this: Play(5097898,'OTcxNDI3MS8xNjIvOTcxNDI3MV8xNjJfMTU2NjUwMS5tcDM=','OTcxNDI3MS8xNjIvOTcxNDI3MV8xNjJfMTU2NjUwMS5vZ2c=',false,'Zy9iL2diXzk3MTQyNzFfMTYyXzE1NjY1MDEubXAz','Zy9iL2diXzk3MTQyNzFfMTYyXzE1NjY1MDEub2dn','h');return false;
        const playCall = $(el).attr('onclick');
        // skip PlayPhrase, etc.
        if(!playCall.match(/Play\s*\(/)) {
            return;
        }
        const args = playCall.split(',');
        const base64AudioUrl = args[1].slice(1, -1);
        const audioUrl = Buffer.from(base64AudioUrl, 'base64').toString('utf-8');
        return forvoAudioUrl + audioUrl;
    }).get();
}

const downloadUrlAsBase64 = async (url) => {
    const response = await fetch(url);
    const imageBytes = await response.arrayBuffer();
    const dataString = "data:" + response.headers.get("content-type") + ";base64," + new Buffer(imageBytes).toString('base64');
    return dataString;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

const main = async (args) => {
    const vocabModel = (await getModel(args[0])).Vocab;
    const browser = await openBrowser();
    const page = await browser.newPage();
    const allVocab = await vocabModel.all();
    for (const v of allVocab) {
        console.log(v.toJSON());
        // await scrapeImageUrls(page, v.english).then((value) => {
        //     console.log(value);
        // });
        // console.log(v.pronunciation);
        // await scrapeAudioUrls(v.thai).then((value) => {
        //     console.log(value);
        // });
        // don't spam the server
        // await sleep(2000);
    }
    // browser.close();
}

if (!module.parent) {
    main(process.argv.slice(2));
} else {
    module.exports = {
        openBrowser: openBrowser,
        scrapeImageUrls: scrapeImageUrls,
        scrapeGoogleImageUrls: scrapeGoogleImageUrls,
        scrapeAudioUrls: scrapeAudioUrls,
        downloadUrlAsBase64: downloadUrlAsBase64,
        sleep: sleep,
        main: main,
    }
}
