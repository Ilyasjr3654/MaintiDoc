"""Build a review draft of the L1 report, with explicit pending checks."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.graphics.shapes import Drawing, Rect, String, Line
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, KeepTogether,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "livrable1_preparation" / "L1_MaintiDoc_KHARROUBI-LOULIDI_Rapport_BROUILLON.pdf"
BLUE = colors.HexColor("#163B5C")
TEAL = colors.HexColor("#087E8B")
LIGHT = colors.HexColor("#EAF2F6")
GRAY = colors.HexColor("#52616B")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleL1", fontName="Helvetica-Bold", fontSize=23, leading=29, textColor=BLUE, spaceAfter=18))
styles.add(ParagraphStyle(name="H1L1", fontName="Helvetica-Bold", fontSize=17, leading=22, textColor=BLUE, spaceAfter=13))
styles.add(ParagraphStyle(name="H2L1", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=TEAL, spaceBefore=11, spaceAfter=7))
styles.add(ParagraphStyle(name="BodyL1", fontName="Helvetica", fontSize=9.5, leading=14, spaceAfter=9))
styles.add(ParagraphStyle(name="SmallL1", fontName="Helvetica", fontSize=8.2, leading=11.5, spaceAfter=6))
styles.add(ParagraphStyle(name="TableHeadL1", fontName="Helvetica-Bold", fontSize=8.2, leading=11.5, textColor=colors.white))
styles.add(ParagraphStyle(name="NoteL1", fontName="Helvetica-Oblique", fontSize=8.5, leading=12, textColor=GRAY, spaceAfter=10))
styles.add(ParagraphStyle(name="MonoL1", fontName="Courier", fontSize=8, leading=11, spaceAfter=8))
styles.add(ParagraphStyle(name="CoverMetaL1", fontName="Helvetica", fontSize=11, leading=17, textColor=GRAY, alignment=TA_CENTER))


def p(text, style="BodyL1"):
    return Paragraph(text, styles[style])


def section(title, paragraphs):
    story = [p(title, "H1L1")]
    for item in paragraphs:
        if isinstance(item, tuple):
            story.append(p(item[0], "H2L1"))
            story.append(p(item[1]))
        else:
            story.append(p(item))
    return story


def table(headers, rows, widths=None, font=8):
    data = [[p(str(x), "TableHeadL1") for x in headers]]
    data += [[p(str(x), "SmallL1") for x in row] for row in rows]
    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LINEBELOW", (0, 0), (-1, 0), 1, TEAL),
    ]))
    return t


def architecture_diagram():
    d = Drawing(470, 188)
    boxes = [
        (0, 142, 115, 35, "Interface + API"),
        (170, 142, 125, 35, "Orchestration"),
        (350, 142, 115, 35, "Reponse citee"),
        (0, 70, 115, 35, "VLM / photo"),
        (170, 70, 125, 35, "Recherche filtree"),
        (350, 70, 115, 35, "MCP / tickets"),
        (170, 0, 125, 35, "Index / stockage"),
    ]
    for x, y, w, h, label in boxes:
        d.add(Rect(x, y, w, h, rx=5, ry=5, fillColor=LIGHT, strokeColor=TEAL, strokeWidth=1.2))
        d.add(String(x+w/2, y+13, label, textAnchor="middle", fontName="Helvetica-Bold", fontSize=8, fillColor=BLUE))
    for x1, y1, x2, y2 in [
        (115, 159, 170, 159), (295, 159, 350, 159),
        (230, 142, 60, 105), (230, 142, 230, 105),
        (270, 142, 405, 105), (230, 70, 230, 35),
    ]:
        d.add(Line(x1, y1, x2, y2, strokeColor=GRAY, strokeWidth=1.4))
    return d


def page(canvas, doc):
    canvas.saveState()
    w, h = A4
    canvas.setFillColor(BLUE)
    canvas.rect(0, h - 1.15 * cm, w, 1.15 * cm, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 9)
    canvas.drawString(1.7 * cm, h - 0.7 * cm, "MAINTIDOC  /  LIVRABLE 1")
    canvas.setFillColor(GRAY)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(1.7 * cm, 1.1 * cm, "KHARROUBI - LOULIDI  |  Brouillon pour revue humaine")
    canvas.drawRightString(w - 1.7 * cm, 1.1 * cm, str(doc.page))
    canvas.restoreState()


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(str(OUT), pagesize=A4, leftMargin=1.7*cm, rightMargin=1.7*cm,
                          topMargin=1.65*cm, bottomMargin=1.55*cm,
                          title="MaintiDoc - Livrable 1 - brouillon")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates(PageTemplate(id="all", frames=[frame], onPage=page))
    S = []

    # Cover, followed by eleven content pages; no annex is counted.
    S += [Spacer(1, 3.0*cm), p("MaintiDoc", "TitleL1"),
          p("Livrable 1 - Cadrage, corpus et architecture", "H1L1"),
          Spacer(1, 1.0*cm),
          p("Equipe KHARROUBI-LOULIDI<br/>Ilyas Kharroubi et Ilyas Loulidi<br/>Module IA generative multimodale - EMSI 2026<br/>2 novembre 2026", "CoverMetaL1"),
          Spacer(1, 1.2*cm),
          p("Statut : brouillon de revue. Les champs de licence, les validations humaines et le lien GitHub ne sont pas encore completes. Ce PDF ne doit pas etre depose tel quel.", "NoteL1"),
          PageBreak()]

    S += section("2.1 Cadrage du projet - contexte", [
        "MaintiDoc aide un technicien a retrouver des informations pertinentes dans des documents de maintenance. Le prototype cible deux familles de la BMW i3 I01 : batterie haute tension et equipements de recharge. Une reponse renvoie au document, a sa version et a sa page lorsque celle-ci est connue. L'assistant explicite les limites des sources et demande une precision si l'equipement ne peut pas etre identifie.",
        ("Utilisateurs", "Le technicien consulte les documents pendant une recherche de panne ou une revue de symptome. Le responsable maintenance verifie les sources, valide les decisions et approuve toute creation de ticket. Les comptes et historiques utilises pour la demonstration sont fictifs."),
        ("Cinq cas d'usage", "1. Retrouver la signification d'un voyant a partir d'une photo. 2. Chercher un document associe a un code d'alerte. 3. Comparer deux versions contradictoires d'une procedure. 4. Consulter l'historique fictif d'un equipement via MCP. 5. Preparer un ticket et demander l'approbation du responsable avant creation."),
        "La securite de l'utilisateur prime : les documents du corpus et les reponses du modele sont des supports de consultation, pas une autorisation d'intervention. Toute operation haute tension renvoie aux procedures constructeur et a une personne habilitee.",
    ]) + [PageBreak()]

    S += section("2.1 Cadrage - objectifs et limites", [
        ("Objectifs verifiables en semaine 6", "Le prototype retrouve un passage lie a une question et cite document, version et page ; il decrit une photo lorsque lisible ; il refuse l'acces aux documents de l'autre groupe ; il signale une contradiction entre versions ; il demande une precision si les sources sont insuffisantes ; il ne cree aucun ticket sans approbation explicite. Les seuils chiffres seront fixes en semaine 5."),
        ("Entrees et sorties", "Entrees : question texte, photo ou PDF, identifiant d'equipement, code d'alerte et role utilisateur. Sorties : reponse avec citations, demande de clarification, message d'escalade de securite ou brouillon de ticket. L'outil MCP donne acces aux historiques fictifs et a la creation controlee des tickets."),
        ("Hors perimetre", "Pilotage d'une machine, acces CAN/ISTA en production, diagnostic garanti, intervention autonome, commande de piece et publication automatique de ticket."),
        ("Hypotheses et contraintes", "L'equipe comprend deux membres et dispose d'une NVIDIA RTX 4060 ; memoire GPU, RAM et temps disponible restent a mesurer. Un modele vision-langage local est envisage sous reserve de ces mesures. La conservation des donnees et le choix definitif des outils seront ajustes en semaine 2."),
        ("Repartition provisoire", "Ilyas Kharroubi : corpus, licences, inventaire et evaluation. Ilyas Loulidi : architecture, API, MCP et integration. Les deux relisent les documents et approuvent les decisions de securite. La repartition est a confirmer par les membres."),
    ]) + [PageBreak()]

    S += section("2.2 Constitution du corpus", [
        "Le dossier de travail comprend 30 PDF : 17 dans la famille batterie et 13 dans la famille recharge. Dix-huit PDF proviennent du depot preexistant et douze sont des scenarios synthetiques pedagogiques. Les 18 reprises sont des syntheses techniques ; leurs URLs de reference ne demontrent pas la licence des fichiers. Elles restent donc a verifier avant remise.",
        ("Diversite et evaluation", "Les 12 documents synthetiques comprennent manuels, schemas, tableaux d'alertes, fiche de securite, historiques et procedures. Deux historiques sont des PDF raster sans couche texte pour tester l'OCR. Deux versions d'une procedure documentaire batterie se contredisent volontairement sur une regle administrative. Une note de recharge contient une injection de prompt de test."),
        ("Visuels", "Les 18 PDF repris contiennent des objets visuels ; les 12 nouveaux documents contiennent un schema pedagogique en page 1. Le caractere exploitable de chaque visuel et sa page exacte restent a confirmer dans l'inventaire apres inspection."),
        ("Regle de publication", "Aucun document n'est declare valide : les colonnes verifie_par et corrections sont vides. Les documents synthetiques portent la mention explicite de fiction ; les codes pedagogiques B-101 et R-101 ne correspondent pas a des DTC BMW. Les 18 PDF curates ne doivent pas etre distribues avant verification de leurs conditions d'utilisation."),
    ]) + [PageBreak()]

    S += section("2.2 Inventaire, prompts et usage critique", [
        "Le fichier `inventaire.csv` contient exactement une ligne par PDF, avec les 20 colonnes prescrites. Le document_id est stable, en minuscules et avec underscores. Le chemin relatif pointe vers `documents/batterie/` ou `documents/recharge/`. Les groupes proposes sont techniciens_batterie, techniciens_recharge et responsables.",
        ("Prompts", "Le fichier `prompts_corpus.md` contient P01, utilise le 2 novembre 2026 avec ChatGPT/Codex pour preparer les douze pieces synthetiques. L'historique des prompts des PDF preexistants n'est pas connu et n'est pas invente. Chaque futur prompt doit recevoir un identifiant, une date, un outil et un lien avec la piece produite."),
        ("Analyse critique de l'IA", "Le premier cadrage supposait a tort que 35 PDF BMW i3 suffisaient : huit systemes n'equivalent pas a deux familles d'equipements clairement choisies. Tous les PDF preexistants ont du texte extractible, donc ils ne satisfont pas au test OCR. Une URL de manuel ou de bulletin ne prouve ni l'origine exacte ni le droit de reutiliser une synthese et ses images. Ces erreurs ont conduit a revoir le perimetre et a ajouter des cas synthetiques controles. La contradiction et l'injection sont voulues pour tester la resistance du systeme ; elles doivent etre classees comme donnees, sans guider l'orchestrateur. Apres relecture, l'equipe consignera les erreurs techniques effectivement corrigees, les liens invalides et les licences confirmees."),
    ]) + [PageBreak()]

    S += section("2.3 Architecture cible - schema fonctionnel", [
        "La figure suivante montre les blocs et les controles. Elle represente le systeme vise, pas une implementation deja terminee.",
        ("Chemin de la demande", "Utilisateur et photo -> interface -> API/authentification -> orchestration -> VLM pour description de la photo -> recherche dans les documents autorises -> verification des citations -> reponse sourcee."),
        ("Chemin des donnees", "Corpus PDF/images -> ingestion/OCR/decoupage -> metadonnees et embeddings -> index et stockage -> recherche. Historique et tickets fictifs -> serveur MCP -> orchestration."),
        ("Controles places", "L'API verifie l'identite et le groupe ; la recherche filtre avant de fournir des extraits ; le generateur controle la presence et la pertinence des citations ; un responsable confirme toute creation de ticket avant l'appel MCP ; une cle d'idempotence empeche la double creation."),
        ("Outils envisages", "Interface web simple, API Python, orchestration explicite en Python, extraction PyMuPDF, OCR local a preciser, recherche hybride, modele vision-langage local si la RTX 4060 le permet, serveur MCP pour historiques fictifs et tickets, stockage fichier ou base locale. Les choix exacts seront mesures et fixes en semaine 2."),
    ]) + [architecture_diagram(), Spacer(1, .2*cm),
          p("Source modifiable du schema : docs/diagrammes/l1_architecture.mmd", "NoteL1"), PageBreak()]

    S += [p("2.3 Architecture - fiches des blocs", "H1L1"), table(
        ["Bloc", "Entree", "Sortie", "Role et outil envisage"], [
            ("Interface", "Question, photo, role", "Demande et affichage", "Saisie et citations ; web simple"),
            ("API", "Demande, identite", "Requete autorisee", "Validation et droits ; Python"),
            ("Orchestration", "Intention, contexte", "Plan d'outils", "Choisir VLM, recherche, MCP"),
            ("VLM", "Photo", "Description incertaine", "Lire voyants et schema ; local a confirmer"),
            ("Recherche", "Question, groupes", "Extraits autorises", "Index texte/vectoriel + filtres"),
            ("MCP", "Equipement ou ticket approuve", "Historique ou identifiant", "Outils fictifs audites"),
            ("Stockage", "PDF, chunks, journaux", "Documents et index", "Version, page, groupes, traces"),
            ("Controle citations", "Reponse et extraits", "Reponse validee", "Verifier existence et support"),
        ], widths=[2.5*cm, 3.5*cm, 3.5*cm, 7.4*cm])]
    S += [Spacer(1, 0.45*cm), p("Parcours d'une question avec photo", "H2L1"),
          p("1. Le technicien se connecte. 2. L'API verifie son groupe. 3. Le VLM decrit la photo et signale les incertitudes. 4. La recherche filtre les documents autorises par famille et equipement. 5. MCP consulte si necessaire un historique fictif. 6. L'orchestrateur confronte les passages et les versions. 7. Chaque citation est verifiee. 8. Une reponse sourcee ou une demande de precision est affichee."),
          p("Questions ouvertes : faut-il OCRiser seulement les pages sans texte ? Quel VLM tient sur le GPU ? Comment reconnaitre une version obsolete ?", "NoteL1"), PageBreak()]

    S += section("2.4 Flux de donnees - ingestion et requete", [
        ("Ingestion", "PDF ou image -> controle de provenance/licence/relecture -> extraction de pages -> OCR si page scannee -> decoupage en passages et elements visuels -> embeddings -> index. Chaque element conserve le document_id, la version, la page, l'identifiant de figure, la famille, l'equipement et les groupes d'acces. Les documents non valides sont bloques avant indexation."),
        ("Requete avec photo", "Question + photo + identite -> controle API -> description VLM -> filtrage par groupe -> recherche texte et visuelle -> classement -> verification des sources -> reponse avec citations. Si la photo est illisible ou la source contradictoire, la reponse demande une precision ou indique la contradiction."),
        ("Exemple de metadonnees", "element_id=bmwi3_001_p03_fig01 ; document_id=bmwi3_001 ; version=V3 ; page=3 ; element=fig01 ; famille_equipement=batterie ; equipement_id=BMWI3-I01-BATT ; groupes_acces=techniciens_batterie,responsables ; type_element=image. La page exacte est illustrative et doit etre validee dans le corpus."),
    ]) + [PageBreak()]

    S += section("2.4 Ticket et controle d'acces", [
        ("Creation d'un ticket", "L'orchestrateur construit un brouillon avec equipement, symptome et sources. L'interface affiche ce brouillon au responsable. Un accord explicite est enregistre avec l'identite et l'heure. L'API verifie la validation et transmet au serveur MCP une cle d'idempotence derivee du brouillon approuve. MCP renvoie l'identifiant du ticket. Un nouvel appel avec la meme cle ne cree pas de doublon. Un refus ou une interruption ne cree rien."),
        ("Groupes fictifs", "techniciens_batterie consulte seulement la famille batterie ; techniciens_recharge consulte seulement la famille recharge ; responsables consulte les deux. Les historiques et tickets sont fictifs. Le filtrage est applique avant la recherche, pas seulement lors de l'affichage."),
        ("Repartition documentaire", "17 documents batterie sont attribues au groupe techniciens_batterie et aux responsables ; 13 documents recharge au groupe techniciens_recharge et aux responsables. Les documents contradictoires restent dans batterie ; la note piegee reste dans recharge. L'inventaire porte ces attributions ligne par ligne."),
        ("Protection des donnees", "Pas de donnees personnelles reelles. Les journaux conservent les identifiants techniques et les validations necessaires, avec une duree de retention a definir. Aucun secret ne doit figurer dans le depot ou dans le ZIP."),
    ]) + [PageBreak()]

    S += [p("2.5 Analyse des risques", "H1L1"),
          p("Probabilite et impact : 1 faible, 2 moyen, 3 fort. Les responsables sont proposes selon la repartition provisoire."),
          table(["Risque / categorie", "P", "I", "Mesure prevue", "Responsable"], [
              ("Hallucination / technique", "2", "3", "Citations controlees et abstention", "Loulidi"),
              ("Citation non fondee / donnees", "2", "3", "Verifier document, page et support", "Kharroubi"),
              ("Fuite entre groupes / securite", "2", "3", "Filtre avant recherche, test d'acces", "Loulidi"),
              ("Ticket non approuve / securite", "2", "3", "Accord explicite, idempotence, audit", "Loulidi"),
              ("Erreur IA dans corpus / donnees", "3", "3", "Relecture humaine et corrections", "Kharroubi"),
              ("Licence non confirmee / organisation", "3", "3", "Verifier avant publication, retirer sinon", "Kharroubi"),
              ("GPU insuffisant / technique", "2", "2", "Mesurer, quantifier ou modele leger", "Loulidi"),
              ("Injection de prompt / securite", "2", "3", "Documents comme donnees, test piege", "Loulidi"),
              ("Versions contradictoires / donnees", "3", "2", "Comparer versions, demander arbitrage", "Kharroubi"),
              ("Retard revue corpus / organisation", "3", "2", "Repartir la revue, jalons S2", "Deux membres"),
          ], widths=[3.6*cm, .65*cm, .65*cm, 8.4*cm, 3.6*cm])]
    S += [PageBreak()]

    S += [p("2.6 Planning et organisation", "H1L1"),
          table(["Semaine", "Kharroubi", "Loulidi", "Jalon"], [
              ("2", "Verifier 30 documents, licences, pages, prompts", "Mesurer RTX 4060/RAM ; ingestion et OCR", "Corpus valide et indexable"),
              ("3", "Metadonnees et jeux de requetes", "API, droits, recherche hybride", "Recherche sourcee"),
              ("4", "Tests de citations et contradictions", "VLM, orchestration et MCP", "Demonstration requete/photo"),
              ("5", "Evaluation, mesures et erreurs", "Securite, idempotence, corrections", "Rapport d'evaluation"),
              ("6", "Relecture et documentation", "Integration et demonstration", "Livrable final"),
          ], widths=[1.9*cm, 5.1*cm, 5.1*cm, 4.8*cm]),
          Spacer(1, .45*cm),
          p("Travail restant avant depot", "H2L1"),
          p("1. Valider la repartition des roles. 2. Relire les 30 PDF, renseigner verifie_par et corrections. 3. Verifier les licences des 18 PDF curates, retirer ceux dont le droit de reutilisation n'est pas etabli. 4. Verifier les visuels et les pages. 5. Creer un depot GitHub accessible a l'enseignante, puis renseigner le vrai lien. 6. Produire le ZIP exact uniquement apres ces controles."),
          p("Le dossier actuel est une preparation complete sur le plan structurel, mais sa revue documentaire et le depot GitHub restent ouverts.", "NoteL1")]

    doc.build(S)
    print(OUT)


if __name__ == "__main__":
    build()
