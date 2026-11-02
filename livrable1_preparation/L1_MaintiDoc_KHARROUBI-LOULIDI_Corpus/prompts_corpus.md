# Prompts et usage de l'IA pour le corpus

## P01 - Preparation de documents synthetiques de test

- Date : 2 novembre 2026.
- Outil : ChatGPT / Codex.
- Usage : conception et generation par script de 12 documents pedagogiques fictifs, sept pour la batterie haute tension et cinq pour la recharge, dont deux versions contradictoires, deux pages scannees pour OCR et une injection de prompt de test.
- Instruction de travail : "Preparer un corpus MaintiDoc de formation pour la BMW i3, organise en deux familles batterie et recharge. Ajouter des documents synthetiques courts, clairement fictifs, avec identifiants stables, schema simple, deux PDF raster sans couche texte, deux versions volontairement contradictoires d'une regle administrative, et une instruction hostile placee comme donnee de test. Ne pas fournir de procedure physique de maintenance ni presenter ces contenus comme des faits BMW verifies."
- Sortie : `documents/batterie/` et `documents/recharge/`, script `scripts/prepare_l1_corpus.py` dans le depot local.
- Relecture : **a faire par Ilyas Kharroubi et Ilyas Loulidi**. Aucun document ne porte encore la mention `verifie_par` dans l'inventaire.

## Documents du depot anterieur

Les 18 PDF curates repris du dossier `data/raw/pdf/bmw_i3/` existaient avant cette preparation. Leur historique de generation, les prompts eventuellement utilises et les corrections passees ne sont pas documentes dans le depot. Il serait incorrect d'inventer ces informations. Leur `outil_ia`, `verifie_par` et `corrections` restent a completer apres enquete et relecture.

## Analyse critique provisoire

Le premier brouillon du livrable traitait les 35 PDF BMW i3 comme un corpus conforme. La comparaison avec les consignes a revele plusieurs erreurs : les documents couvraient huit systemes au lieu de deux familles delimitees, aucun n'etait scanne, et l'URL technique citee ne suffisait pas a etablir le droit de reutilisation du PDF curate. Nous avons recentre le dossier de travail sur deux familles et ajoute des cas de test controles. Les 18 PDF repris restent a verifier individuellement : titres, faits techniques, visuels, URL, licence, corrections et provenance. Les documents synthetiques ajoutent volontairement une contradiction et une injection ; l'index devra les traiter comme donnees, non comme instructions. Cette analyse devra etre actualisee apres la revue humaine, avec les erreurs effectivement trouvees et corrigees.
