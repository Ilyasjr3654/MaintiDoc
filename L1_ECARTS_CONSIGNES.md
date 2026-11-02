# Livrable 1 MaintiDoc - audit de conformite au sujet detaille

Date : 2 novembre 2026. Ce document compare les consignes de `L1_MaintiDoc_Consignes_du_livrable1.pdf` a l'etat **initial** du dossier local, avant la preparation situee dans `livrable1_preparation/`. Il ne tient pas lieu de rapport a deposer.

**Mise a jour :** un corpus de travail de 30 PDF, l'inventaire de 20 colonnes, les prompts et un brouillon PDF de 11 pages sont maintenant disponibles dans `livrable1_preparation/`. Les constats du tableau ci-dessous restent l'historique des ecarts initiaux. La revue humaine, les licences des 18 PDF repris, le depot GitHub et le ZIP final restent a accomplir.

## Exigences et etat constate

| Exigence du sujet | Etat local | Action necessaire |
|---|---|---|
| Rapport PDF en francais, 10 a 15 pages, six parties dans l'ordre 2.1 a 2.6 | Un brouillon Markdown, non conforme au format et a plusieurs rubriques | Recomposer le rapport et produire un PDF verifie |
| Equipe de 1 a 3 membres, noms de famille pour le nommage | Noms non communiques | Renseigner les membres, les roles et le nom d'equipe |
| 30 a 50 documents couvrant deux familles d'equipements | 35 PDF BMW i3 couvrant huit systemes ; familles non delimitees | Choisir deux familles, selectionner ou creer 30 a 50 documents coherents |
| Types documentaires varies | 35 syntheses techniques de meme type | Ajouter manuels, procedures, fiches de securite, schemas, codes d'alarme, photos et historiques fictifs |
| Au moins 10 documents visuels | 35 PDF contiennent des objets visuels | Verifier que les visuels sont exploitables et les relever par page |
| Au moins deux PDF scannes pour OCR | 0 PDF scanne parmi les 35 (texte extractible sur chaque document) | Constituer deux vrais scans et verifier l'absence de couche texte avant OCR |
| Documents publics reutilisables ou synthetiques, provenance et licence verifiees | URL de reference dans les metadonnees, mais aucune licence ni validation document par document | Verifier les droits, l'origine et les faits ; ne pas assimiler une URL de reference a une licence |
| Prompts `corpus/prompts_corpus.md` numerotes P01, P02... | Fichier absent | Tracer les prompts reels, outil et date ; ne pas inventer de prompts passes |
| Deux documents contradictoires, un document avec injection de test | Absents ou non identifies dans le catalogue | Creer des documents synthetiques controles, les signaler `contradictoire` et `injection` |
| Analyse critique d'une demi-page de l'usage de l'IA | Absente | Decrire les erreurs effectivement constatees et corrigees |
| `corpus/inventaire.csv` avec les 20 colonnes imposees | `data/metadata/documents.csv` a un autre schema | Construire l'inventaire exact ; un fichier du corpus = une ligne, et inversement |
| Architecture interface, API, orchestration, recherche, VLM, MCP, stockage | Brouillon sans API, VLM et MCP explicites | Faire un schema complet et une fiche role/entrees/sorties/outil par bloc |
| Droits, validation humaine et controle des citations sur le schema | Partiellement decrits | Placer les trois controles au bon endroit |
| Trois flux : ingestion, requete avec photo, creation de ticket | Deux flux generiques, ticket absent | Dessiner les trois flux, approbation humaine et idempotence du ticket |
| Metadonnees d'element indexe avec version/page/element/famille/groupes | Champs documentaires partiels | Decrire le schema du chunk et du visuel indexes |
| Deux groupes fictifs et repartition des documents | Roles generiques proposes | Nommer deux groupes associes aux deux familles et attribuer les documents |
| Au moins 8 risques avec categorie, probabilite 1-3, impact 1-3, mesure, responsable | 9 risques mais sans scores, categorie ni responsable | Refaire le tableau ; inclure hallucination, fuite, ticket, IA, licences, materiel |
| Planning semaines 2 a 6 par membre et ressources reelles | Planning generique semaines 1 a 6 | Adapter aux membres et materiel disponibles |
| ZIP unique, noms exacts, lien GitHub accessible | Aucun ZIP ; aucun depot Git local ou URL connue | Finaliser les fichiers, verifier le depot, puis creer `L1_MaintiDoc_<NomEquipe>.zip` |

## Enquetes encore necessaires

1. Noms de famille des membres et URL du depot GitHub.
2. Choix des deux familles d'equipements. Le theme BMW i3 peut etre conserve seulement si le corpus final est clairement recentre sur deux familles et atteint 30 documents verifiables.
3. Ressources disponibles : GPU, memoire, machines et temps reel de chaque membre. Les versions exactes des outils et la mesure precise de memoire GPU sont reportables a la semaine 2.
4. Licence, provenance et validation humaine de chaque document. Aucune entree ne peut etre declaree validee sans cette revue.

## Ordre de production

1. Fixer deux familles et les groupes d'acces ; faire la liste des 30 a 50 pieces effectivement retenues.
2. Constituer les documents manquants, dont deux scans, deux versions contradictoires et le document piege de test. Exclure les donnees personnelles reelles.
3. Controler source, licence, contenu, version, pages et visuels ; renseigner l'inventaire et les prompts.
4. Rediger les six parties du rapport, le schema et les flux dans `docs/diagrammes/`.
5. Generer le PDF, verifier ses pages, controler la correspondance fichiers/inventaire et empaqueter le ZIP exact.

Le dossier `data/raw/pdf/bmw_i3/` reste un materiau de depart. Ses 35 syntheses ne sont pas automatiquement un corpus conforme au livrable 1.
