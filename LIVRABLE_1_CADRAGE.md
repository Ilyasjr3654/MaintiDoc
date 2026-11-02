# MaintiDoc - Livrable 1 : cadrage, corpus et architecture cible

> **Brouillon de travail - ne pas deposer tel quel.** Les consignes detaillees du livrable 1 exigent un rapport PDF de 10 a 15 pages, un corpus de 30 a 50 documents sur exactement deux familles d'equipements, deux PDF scannes, deux documents contradictoires, un document piege, un inventaire au format impose, les prompts traces et un ZIP nomme selon les membres. Le depot actuel ne satisfait pas encore ces exigences. Voir `L1_ECARTS_CONSIGNES.md`.

Projet : assistant documentaire multimodal et agentique pour les techniciens de maintenance
Version : 1.0 - 2 novembre 2026
Perimetre : preparation du projet avant implementation de l'assistant final

> Distinction : les attentes ci-dessous viennent du sujet fourni dans le PDF du projet. Les choix techniques, hypotheses et propositions sont ceux du cadrage MaintiDoc a partir du depot existant.

## 1. Resume executif

MaintiDoc sera un assistant documentaire multimodal destine en priorite aux techniciens qui diagnostiquent une BMW i3 I01. Il devra retrouver les passages et schemas pertinents dans un corpus technique, repondre en francais avec des citations verifiables, demander des precisions lorsqu'une demande est trop vague et declencher une escalade de securite pour les operations haute tension dangereuses.

Le premier perimetre est maitrise : documentation BMW/NHTSA consacree a la BMW i3, notamment haute tension, recharge, eDrive, thermique, direction, carrosserie et securite. Il ne s'agit pas de commander des pieces, piloter un vehicule, remplacer un diagnostic constructeur ou donner une procedure de manipulation haute tension a une personne non habilitee.

## 2. Utilisateurs, cas d'usage et objectifs

### Utilisateurs cibles

| Utilisateur | Besoin principal | Acces propose |
|---|---|---|
| Technicien de maintenance | Retrouver une procedure, un symptome, un DTC ou un schema | `technician` |
| Responsable maintenance | Verifier une decision, une source et l'historique des reponses | `maintenance_manager` |
| Administrateur/equipe projet | Gerer corpus, prompts, evaluations et journaux | `project_admin` |

### Cas d'usage prioritaires

1. Rechercher la documentation correspondant a un symptome BMW i3.
2. Interpreter un ou plusieurs codes defaut (DTC) dans leur contexte.
3. Comparer des variantes documentaires, par exemple batterie 60 Ah / 94 Ah.
4. Exploiter une image ou un schema extrait d'un PDF avec son contexte textuel.
5. Produire une reponse courte, sourcee et orientee vers les controles suivants.
6. Refuser une conclusion trop forte ou demander les informations manquantes.
7. Signaler les risques et escalader les demandes concernant l'ouverture ou la mise hors tension d'un systeme haute tension.

### Objectifs mesurables proposes

| Objectif | Indicateur |
|---|---|
| Retrouver le bon document | document attendu dans le top-3 de recherche |
| Repondre avec tracabilite | chaque reponse technique cite un document et une source |
| Limiter les hallucinations | aucune conclusion non etayee dans les cas de test |
| Gerer l'incertitude | demande de clarification pour une requete sous-specifiee |
| Proteger l'utilisateur | escalade des scenarios haute tension dangereux |
| Preserver la confidentialite | aucun document ou groupe hors perimetre accessible |

## 3. Perimetre

### Inclus dans la V1

- BMW i3, plateforme I01, documentation technique en francais ou exploitable pour le projet.
- Recherche hybride texte + metadonnees + elements visuels.
- Reponses documentaires avec citations et niveau de confiance qualitatif.
- Gestion des DTC, symptomes, systemes, sous-systemes et variantes.
- Journalisation des requetes, documents recuperes, prompts et validations humaines.
- Jeux de test de recherche, reranking, clarification et securite.

### Hors perimetre

- Diagnostic autonome engageant la responsabilite du technicien.
- Commande d'un vehicule, d'un chargeur ou d'un equipement de garage.
- Acces direct aux donnees CAN/ISTA en production.
- Remplacement automatique d'une piece ou validation d'une reparation.
- Conseil de manipulation haute tension sans controle d'habilitation et procedure constructeur.
- Ingestion de documents sans source, version ou controle humain.

## 4. Corpus et constitution des donnees

### Etat actuel du depot

Le depot contient deja :

- 35 PDF BMW i3 dans `data/raw/pdf/bmw_i3/` ;
- 35 entrees dans `data/metadata/corpus_index.csv` et `data/metadata/documents.csv` ;
- 133 chunks texte dans `data/processed/text_chunks.jsonl` ;
- 105 elements visuels dans `data/processed/visual_elements.jsonl` ;
- 35 syntheses documentaires dans `data/processed/document_index.jsonl` ;
- des jeux `train`, `validation` et `test` pour le reranker ;
- des cas d'evaluation incluant clarification et escalade de securite.

Le corpus couvre notamment `HIGH_VOLTAGE`, `CHARGING`, `EDRIVE`, `THERMAL`, `STEERING`, `BODY` et `SAFETY`.

### Inventaire obligatoire

Chaque document doit conserver au minimum :

`document_id`, `filename`, `title`, `manufacturer`, `model`, `platform`, `system`, `subsystem`, `problem`, `dtc_codes`, `document_type`, `language`, `source_name`, `source_url`, `source_year`, `version`, `allowed_groups`, `verification_status`, `verified_by`, `verified_at`.

Les champs de verification doivent etre ajoutes ou maintenus dans l'inventaire final. Une entree ne doit pas etre publiee si le fichier est absent, illisible, non attribue a une source ou non verifie.

### Tracabilite des prompts

Les prompts utilises pour produire un resume, un chunk enrichi, un jeu de questions ou une reponse doivent etre inscrits dans `data/metadata/prompt_registry.csv` :

| Champ | Role |
|---|---|
| `prompt_id` | identifiant stable |
| `prompt_version` | version du texte et du modele |
| `purpose` | extraction, question, reponse, securite, evaluation |
| `input_document_ids` | documents utilises |
| `model` | modele appele |
| `parameters` | parametres utiles |
| `output_path` | artefact produit |
| `review_status` | a revoir, valide, rejete |
| `reviewer` / `reviewed_at` | validation humaine |

Prompts initiaux a versionner : extraction de faits, description d'un schema, generation de questions de recherche, reponse avec citations, refus/escalade securite et creation de cas d'evaluation. Toute formulation presente dans le code ou utilisee manuellement doit etre copiee dans ce registre, avec sa date et son modele.

## 5. Architecture cible

```text
Technicien / responsable
          |
          v
  Interface + authentification
          |
          v
  Orchestrateur de requete
    |       |       |
    |       |       +--> garde-fous : securite, perimetre, clarification
    |       +----------> recherche hybride : BM25/embeddings + metadonnees
    +------------------> routeur : texte / image / DTC / source
                          |
                          v
        reranker multimodal + filtre d'acces
                          |
                          v
        generateur de reponse avec citations
                          |
                          v
        reponse + sources + incertitude + journal

Sources --> ingestion --> OCR/extraction --> chunks + images --> index
                                      \\--> catalogue + versions + droits
```

### Role des blocs

- Interface : recoit texte, DTC, image ou document et affiche les sources.
- Authentification/autorisation : applique le groupe utilisateur avant la recuperation.
- Orchestrateur : identifie l'intention, reformule si necessaire et choisit les outils.
- Recherche hybride : combine texte, vecteurs, DTC, systeme, sous-systeme et titre.
- Reranker : classe les passages candidats et evite les passages proches mais incorrects.
- Garde-fous : detectent demande dangereuse, absence d'informations et sortie du perimetre.
- Generateur : repond uniquement a partir du contexte retenu et cite les documents.
- Journal : conserve requete, version des prompts, sources, reponse et retour humain.

### Parcours d'une requete

1. L'utilisateur envoie une question, un DTC et eventuellement une image.
2. Le systeme identifie le role utilisateur et controle les droits.
3. Le routeur classe la demande : recherche documentaire, diagnostic a preciser ou securite.
4. Les metadonnees et les chunks candidats sont recuperes.
5. Le reranker selectionne les passages et visuels les plus pertinents.
6. Le garde-fou verifie contradictions, sources et niveau de danger.
7. Le generateur produit une reponse : faits, controles proposes, limites, citations.
8. La trace complete est enregistree pour evaluation et amelioration.

## 6. Flux de donnees et modele d'acces

```text
PDF source / document verifie
  -> corpus_index.csv
  -> documents.csv
  -> extraction page par page
  -> text_chunks.jsonl + visual_elements.jsonl
  -> index de recherche / index vectoriel
  -> recuperation + reranking
  -> reponse citee
  -> journal d'audit et feedback humain
```

### Modele d'acces propose

| Ressource | Technicien | Responsable | Administrateur |
|---|---:|---:|---:|
| Documents publies et sources | lecture | lecture | lecture/ecriture |
| Reponses et citations | lecture | lecture | lecture |
| Cas d'evaluation | lecture partielle | lecture | lecture/ecriture |
| Prompts et configurations | aucun acces direct | lecture | lecture/ecriture |
| Journaux de requetes | ses traces | traces de l'equipe | toutes les traces |
| Publication/retrait d'un document | non | validation | execution apres validation |

Principes : moindre privilege, separation lecture/ecriture, controle par groupe, versionnement, journal d'audit et retrait reversible d'une source.

## 7. Risques et mesures de reduction

| Risque | Impact | Mesure proposee |
|---|---|---|
| Reponse inventee ou non sourcee | decision technique incorrecte | reponse contrainte par contexte, citations obligatoires, tests negatifs |
| Mauvais document ou mauvaise variante | procedure inadaptee | filtrage modele/plateforme/systeme, reranking, clarification |
| Conseil haute tension dangereux | blessure ou dommage materiel | garde-fou securite, refus, escalade vers personnel habilite |
| Source obsolete ou non verifiee | maintenance erronee | version, annee, URL primaire, statut et revue humaine |
| Fuite entre train/validation/test | metriques trompeuses | separation au niveau document et controle automatise |
| Acces excessif aux documents/journaux | confidentialite | RBAC, filtrage avant retrieval, retention definie |
| Image mal interpretee | mauvais composant identifie | page et contexte conserves, score de confiance, revue humaine |
| Prompt injection dans un document | contournement des regles | traiter les documents comme donnees, jamais comme instructions |
| Dependance a un service externe | indisponibilite ou cout | timeouts, fallback recherche, cache, journal des modeles |

## 8. Planification sur 6 semaines

| Semaine | Travail | Sortie attendue |
|---|---|---|
| S1 | cadrage, roles, inventaire, verification des sources | livrable 1 valide et registre du corpus |
| S2 | ingestion, normalisation, extraction texte/images, catalogue | corpus reproductible et controles qualite |
| S3 | recherche hybride, metadonnees, droits, orchestrateur | prototype retrieval + modele d'acces |
| S4 | reranking, reponses citees, garde-fous | chaine RAG multimodale demonstrable |
| S5 | evaluation, erreurs, securite, tests utilisateurs | rapport de tests et corrections prioritaires |
| S6 | integration, documentation, demonstration et remise | version finale, guide et bilan |

## 9. Repartition des roles dans l'equipe

La composition nominative doit etre renseignee dans le fichier partage du cours. En attendant les noms, la repartition fonctionnelle recommandee est :

| Role | Responsabilites |
|---|---|
| Product owner / cadrage | utilisateurs, perimetre, criteres d'acceptation, planning |
| Data/corpus lead | sources, inventaire, verification, metadonnees |
| Data/ML lead | extraction, embeddings, reranking, evaluation |
| Backend/agent lead | orchestration, outils, garde-fous, journalisation |
| UX/documentation lead | parcours technicien, citations, guide et demonstration |

Un meme etudiant peut cumuler deux roles, mais chaque sortie doit avoir un responsable et, si possible, un relecteur distinct.

## 10. Criteres d'acceptation du livrable 1

- [x] Utilisateurs, cas d'usage, objectifs, perimetre et hors-perimetre definis.
- [x] Corpus initial et etat actuel du depot quantifies.
- [x] Champs d'inventaire et verification documentaire definis.
- [x] Tracabilite des prompts specifiee.
- [x] Architecture par blocs et parcours d'une requete decrits.
- [x] Flux de donnees et modele d'acces decrits.
- [x] Au moins 8 risques analyses avec mesures de reduction.
- [x] Planning sur 6 semaines propose.
- [ ] Noms de l'equipe ajoutes depuis le fichier partage Classroom.
- [ ] Verification humaine de chaque document et des sources primaires finalisee.

## 11. Points a valider par l'equipe

1. Confirmer noms et responsabilites de chaque membre.
2. Confirmer si le perimetre reste BMW i3 I01 ou s'etend a d'autres vehicules.
3. Choisir le modele d'embeddings, le modele generatif et la retention des journaux.
4. Completer le statut de verification de chaque document et faire relire les documents de securite.
5. Valider les seuils d'evaluation top-k, citation, clarification et escalade.
