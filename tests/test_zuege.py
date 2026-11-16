from maedn import HAUS, Zug, legale_zuege


def leeres_brett():
    """Alle Figuren im Haus – praktisch, um gezielt Situationen aufzubauen."""
    return [[HAUS] * 4 for _ in range(4)]


# ---------- D1: Züge sammeln ----------

def test_normaler_zug():
    pos = leeres_brett()
    # keine Figur im Haus, Zielfiguren können nicht ziehen
    pos[0] = [5, 41, 42, 43]
    assert legale_zuege(pos, 0, 3) == [Zug(figur=0, von=5, nach=8)]


def test_rauskommen_nur_mit_6():
    pos = leeres_brett()
    assert legale_zuege(pos, 0, 5) == []
    assert Zug(figur=0, von=HAUS, nach=0) in legale_zuege(pos, 0, 6)


def test_eigene_figur_blockiert():
    pos = leeres_brett()
    pos[0] = [5, 8, 40, 41]
    assert Zug(figur=0, von=5, nach=8) not in legale_zuege(pos, 0, 3)


def test_nicht_ueber_das_ziel_hinaus():
    pos = leeres_brett()
    pos[0] = [41, 40, 42, 43]
    assert legale_zuege(pos, 0, 3) == []      # 41 + 3 = 44 > 43, 40 + 3 = 43 besetzt


def test_schlagen_wird_erkannt():
    pos = leeres_brett()
    pos[0] = [20, 41, 42, 43]                 # Rot auf Feld 20
    pos[2] = [3, HAUS, HAUS, HAUS]            # Gelb auf Feld 23
    assert legale_zuege(pos, 0, 3) == [Zug(figur=0, von=20, nach=23, geschlagen=(2, 0))]


# ---------- D2: Pflichtregeln ----------

def test_bei_6_muss_man_rauskommen():
    pos = leeres_brett()
    pos[0] = [12, HAUS, HAUS, HAUS]
    # Figur 0 könnte auf 18 ziehen, aber Rauskommen ist Pflicht
    assert all(z.von == HAUS for z in legale_zuege(pos, 0, 6))


def test_startfeld_raeumen():
    pos = leeres_brett()
    pos[0] = [0, 12, HAUS, HAUS]
    # Figur auf dem Startfeld muss weg, solange noch Figuren im Haus warten
    assert legale_zuege(pos, 0, 4) == [Zug(figur=0, von=0, nach=4)]


def test_startfeld_besetzt_dann_andere_figur():
    pos = leeres_brett()
    pos[0] = [0, 4, HAUS, HAUS]
    # Startfigur kann nicht (eigene Figur auf 4) -> die andere darf ziehen
    assert legale_zuege(pos, 0, 4) == [Zug(figur=1, von=4, nach=8)]
