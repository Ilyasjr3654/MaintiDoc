# IA Distribuées — MaintiDoc BMW i3

> Publication GitHub publique : les PDF BMW i3 curates, leurs images extraites et les jeux de donnees textuels derives restent locaux jusqu'a verification des droits de reutilisation. Le corpus de preparation contient donc uniquement les PDF synthetiques sur GitHub ; `inventaire.csv` marque les pieces BMW i3 a verifier. Les scripts permettent de reconstruire les donnees apres acquisition de sources autorisees.

Projet de **collecte et constitution du dataset multimodal** pour MaintiDoc.

Le dossier local contient 35 PDF BMW i3 et le code pour les transformer en dataset RAG : métadonnées, chunks texte, images, exemples reranker et scénarios d'évaluation. Les fichiers BMW i3 dont les droits restent à vérifier sont exclus du dépôt GitHub public.

## 1. Arborescence

```text
IA Distribuées/
├── data/
│   ├── raw/
│   │   ├── pdf/bmw_i3/              # 35 PDF
│   │   ├── pdf/original_sources/    # à compléter avec BMW/NHTSA originaux
│   │   └── images/                  # généré automatiquement
│   ├── metadata/
│   │   ├── corpus_index.csv         # catalogue source
│   │   └── documents.csv            # généré par le pipeline
│   ├── processed/
│   │   ├── text_chunks.jsonl        # chunks RAG
│   │   ├── visual_elements.jsonl    # images + métadonnées
│   │   └── document_index.jsonl     # synthèse par document
│   ├── reranker/
│   │   ├── train.jsonl
│   │   ├── validation.jsonl
│   │   └── test.jsonl
│   └── evaluation/
│       └── eval_cases.jsonl
├── src/maintidoc_dataset/
│   ├── catalog.py
│   ├── chunking.py
│   ├── config.py
│   ├── io_utils.py
│   ├── pdf_extract.py
│   └── pipeline.py
├── scripts/
│   ├── build_dataset.py
│   ├── validate_dataset.py
│   ├── inspect_corpus.py
│   └── show_sample.py
├── tests/
├── .vscode/
└── requirements.txt
```

## 2. Ouvrir dans VS Code

```bash
code "IA Distribuées"
```

## 3. Créer l'environnement Python

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Construire le dataset

```bash
python scripts/build_dataset.py
```

Ce script :

1. lit `corpus_index.csv` ;
2. construit `documents.csv` ;
3. ouvre les 35 PDF avec PyMuPDF ;
4. extrait le texte page par page ;
5. nettoie et segmente le texte ;
6. extrait les images utiles ;
7. crée `text_chunks.jsonl` ;
8. crée `visual_elements.jsonl` ;
9. crée les splits reranker au **niveau document** ;
10. crée les premiers cas d'évaluation.

## 5. Valider le dataset

```bash
python scripts/validate_dataset.py
```

La validation contrôle notamment :

- 35 PDF présents ;
- 35 documents dans les métadonnées ;
- chunks texte non vides ;
- images extraites ;
- absence de fuite de documents entre train / validation / test ;
- cas d'évaluation présents.

## 6. Voir un exemple généré

```bash
python scripts/show_sample.py
```

## 7. Lancer les tests

```bash
pytest -q
```

## 8. VS Code Tasks

Dans VS Code : `Terminal > Run Task...`

- **MaintiDoc: construire le dataset**
- **MaintiDoc: valider le dataset**
- **MaintiDoc: lancer les tests**

## Important

Les 35 PDF MaintiDoc sont des documents curatés. Le champ `source_url` conserve la source BMW/NHTSA de référence. Pour la version finale du projet, les PDF BMW/NHTSA originaux doivent aussi être placés dans `data/raw/pdf/original_sources/` afin de pouvoir citer directement les sources primaires.

## 9. Télécharger les sources primaires BMW/NHTSA (optionnel mais recommandé)

Lorsque tu as Internet :

```bash
python scripts/download_original_sources.py
```

Le script lit `corpus_index.csv`, déduplique les URL et place les PDF originaux disponibles dans :

```text
data/raw/pdf/original_sources/
```

Les erreurs de téléchargement sont signalées sans casser le corpus curaté.
