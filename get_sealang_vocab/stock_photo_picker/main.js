// Super simple example
const { app, BrowserWindow } = require('electron');

const main = async () => {
    // Create the browser window.
    win = new BrowserWindow({ width: 800, height: 600 })
    // and load the index.html of the app.
    win.loadFile('index.html')
}

app.on('ready', main)
