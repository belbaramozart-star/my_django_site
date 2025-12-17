// 1. Importer les bibliothèques nécessaires

import $ from 'jquery';
import Tagify from '@yaireo/tagify';

// 2. Initialisation (fiable via JQuery)
$(document).ready(function(){
    const inputElement = document.getElementById('id_required_skills');

    if (inputElement){
        console.log("Tagify: installation via npm/jquery");

        // Configuration de Tagify
        const suggestionList = ["HTML", "CSS", "JavaScript", "Python", "PHP", "React"];
        const tagifyOptions = {
                whitelist: suggestionList,
                originalInputValueFormat: valuesArr => valuesArr.map(item => item.value).join(','),
                dropdown: {
                    maxItems: 20,
                    enabled: 0,
                    closeOnSelect: false
                },
                // Configuration du bouton 'Ajouter'
                addTagOn: ';|Tab|Enter', // Permet d'ajouter un tag en utilisant ; Tab ou Enter
            };
            // 3. Initialisation de Tagify sur l'élément
            new Tagify(inputElement, tagifyOptions);
                                           
            // Note: Tagify gére le champ de saisie, l'affichage des tags, et maintenant la valeur du champ caché (qui est le format CSV attencu par djange-taggit) pour la soumission.
    } else{
        console.error("ERREUR: Champ 'id_required_skills' introuvable");
    }
});
