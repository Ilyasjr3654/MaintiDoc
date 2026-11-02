# MaintiDoc - livrable 1 (preparation)

Equipe : Ilyas Kharroubi et Ilyas Loulidi. Nom normalise : `KHARROUBI-LOULIDI`.

Objectif : preparer un assistant documentaire multimodal pour deux familles BMW i3 I01, batterie haute tension et recharge, avec recherche sourcee, controle d'acces et creation de ticket soumise a approbation humaine.

Ce dossier contient un rapport PDF de revue et un corpus de travail de 30 PDF avec `inventaire.csv` et `prompts_corpus.md`. Le depot de developpement contient les scripts, les diagrammes Mermaid dans `docs/diagrammes/`, les tests et le corpus de depart.

Structure du corpus : `documents/batterie/` (17 PDF) et `documents/recharge/` (13 PDF). Deux PDF sont raster pour OCR ; une paire est contradictoire ; un document contient une injection de test. Les contenus de test sont fictifs.

**Avant la remise :** relire et valider les 30 documents, confirmer les licences des 18 PDF repris, completer `verifie_par` et `corrections`, creer le depot GitHub accessible a l'enseignante, renseigner son URL, puis construire l'archive au nom exact demande. Le present dossier ne doit pas etre depose tel quel.

Ne relancez pas `scripts/prepare_l1_corpus.py` apres avoir commence la relecture : ce script regenere les 12 PDF synthetiques et l'inventaire. Apres validation, produisez un rapport final sans la mention "brouillon" sous le nom `L1_MaintiDoc_KHARROUBI-LOULIDI_Rapport.pdf`, puis lancez `python scripts/finalize_l1.py --github-url https://github.com/<compte>/<depot>`. Le controle refuse le ZIP si les champs de validation ou le rapport final manquent.
