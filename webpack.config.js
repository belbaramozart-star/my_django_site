
const path = require('path');

module.exports = {
    // 1. Point d'entrée: où webapck doit commencer à chercher le code
    entry : './assets/js/main.js',

    // 2. Mode : "development" pour le développement et "production" pour la minification
    mode : "development",

    // 3. Sortie : où placer le fichire compilé
    output : {
        filename : 'bundle.js',
        // Assurer que le chemin pointe vers le dossier statique géré par Django
        path : path.resolve(__dirname, 'offers/static/offers/js'),
    },

    // 4. Résolution : permet d'importer Tagify sans les chemins relatifs complexes
    resolve : {
        extensions : ['.js'],
        modules : ['node_modules']
    }
};