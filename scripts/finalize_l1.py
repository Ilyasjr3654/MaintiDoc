"""Validate the reviewed L1 materials and create the exact Classroom ZIP."""

from __future__ import annotations

import argparse
import csv
import shutil
import tempfile
import zipfile
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "livrable1_preparation"
TEAM = "KHARROUBI-LOULIDI"
STEM = f"L1_MaintiDoc_{TEAM}"
CORPUS = BASE / f"{STEM}_Corpus"
REPORT_FINAL = BASE / f"{STEM}_Rapport.pdf"
REQUIRED = [
    "document_id", "fichier", "titre", "famille_equipement", "equipement_id",
    "type_document", "version", "nb_pages", "langue", "format",
    "elements_visuels", "provenance", "licence", "genere_par_ia", "outil_ia",
    "verifie_par", "corrections", "groupe_acces", "usage_test", "remarques",
]


def check() -> list[str]:
    errors = []
    index = CORPUS / "inventaire.csv"
    if not index.is_file():
        return ["inventaire.csv manquant"]
    with index.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != REQUIRED:
            errors.append("Colonnes d'inventaire non conformes ou ordre incorrect")
        rows = list(reader)
    if not 30 <= len(rows) <= 50:
        errors.append(f"Nombre de documents hors plage : {len(rows)}")
    if {r["famille_equipement"] for r in rows} != {"batterie", "recharge"}:
        errors.append("Les deux familles attendues ne sont pas presentes")
    ids = [r["document_id"] for r in rows]
    if len(ids) != len(set(ids)):
        errors.append("document_id dupliques")
    on_disk = {p.relative_to(CORPUS).as_posix() for p in (CORPUS / "documents").rglob("*.pdf")}
    listed = {r["fichier"] for r in rows}
    if on_disk != listed:
        errors.append("Inventaire et fichiers du corpus divergent")
    if sum(r["format"] == "pdf_scanne" for r in rows) < 2:
        errors.append("Moins de deux PDF scannes")
    if sum(r["usage_test"] == "contradictoire" for r in rows) < 2:
        errors.append("Moins de deux documents contradictoires")
    if sum(r["usage_test"] == "injection" for r in rows) < 1:
        errors.append("Document piege absent")
    for r in rows:
        tag = r["document_id"]
        for key in ("verifie_par", "corrections", "licence", "provenance", "elements_visuels"):
            if not r.get(key, "").strip() or "A_VERIFIER" in r[key] or "a confirmer" in r[key]:
                errors.append(f"{tag} : {key} non finalise")
        if r["genere_par_ia"] == "a_verifier":
            errors.append(f"{tag} : usage IA inconnu")
        if not r["fichier"].endswith(f"{tag}.pdf"):
            errors.append(f"{tag} : nom de fichier non conforme")
        if r["fichier"] in on_disk:
            actual = len(pymupdf.open(CORPUS / r["fichier"]))
            if str(actual) != r["nb_pages"]:
                errors.append(f"{tag} : nombre de pages incorrect")
    if not REPORT_FINAL.is_file():
        errors.append("Rapport final PDF manquant (le brouillon ne peut pas etre empaquete)")
    elif not 10 <= len(pymupdf.open(REPORT_FINAL)) <= 15:
        errors.append("Rapport hors plage de 10 a 15 pages")
    if not (CORPUS / "prompts_corpus.md").is_file():
        errors.append("prompts_corpus.md manquant")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--github-url", required=True, help="URL reelle du depot equipe accessible a l'enseignante")
    args = parser.parse_args()
    if not args.github_url.startswith("https://github.com/") or args.github_url.count("/") < 4:
        raise SystemExit("URL GitHub invalide ou incomplete")
    errors = check()
    if errors:
        print("ZIP non cree. Controles a terminer :")
        for err in errors:
            print(" -", err)
        raise SystemExit(1)
    with tempfile.TemporaryDirectory(prefix="l1_maintidoc_") as temp:
        folder = Path(temp) / STEM
        folder.mkdir()
        shutil.copyfile(REPORT_FINAL, folder / f"{STEM}_Rapport.pdf")
        shutil.copyfile(BASE / "README.md", folder / "README.md")
        shutil.copytree(CORPUS, folder / CORPUS.name)
        (folder / f"{STEM}_LienGitHub.txt").write_text(args.github_url + "\n", encoding="utf-8")
        output = BASE / f"{STEM}.zip"
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as z:
            for path in folder.rglob("*"):
                if path.is_file():
                    z.write(path, path.relative_to(Path(temp)))
        print(output)


if __name__ == "__main__":
    main()
