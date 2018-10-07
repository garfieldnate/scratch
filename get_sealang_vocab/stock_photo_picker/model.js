const Sequelize = require('sequelize');

// dbFile can be ':memory:'
const getModel = async (dbFile) => {
    const sequelize = new Sequelize({
        dialect: 'sqlite',
        storage: dbFile,
    });

    const textFields = ["headword", "pronunciation", "morphology", "definition", "example", "image_url", "image_base64", "audio_url", "audio_base64", "notes"];
    const fieldsDef = textFields.reduce((acc, cur) =>
        Object.assign({}, acc, {[cur]: {type: Sequelize.TEXT, allowNull: true }}),
        {});
    const Vocab = sequelize.define('vocab', fieldsDef);

    await sequelize.sync();
    return {Vocab: Vocab};
}

module.exports = {
    getModel: getModel
}
