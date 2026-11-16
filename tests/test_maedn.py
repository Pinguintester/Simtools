from maedn import HAUS, absolut, auf_bahn, fertig, neue_position, startzustand


def test_startzustand_offizielle_aufstellung():
    pos = startzustand()
    assert len(pos) == 4
    assert pos[0] == [0, HAUS, HAUS, HAUS]


def test_auf_bahn():
    assert auf_bahn(0)
    assert auf_bahn(39)
    assert not auf_bahn(HAUS)
    assert not auf_bahn(40)


def test_absolut_startfeld():
    assert absolut(2, 0) == 20


def test_absolut_ueberlauf():
    # Spieler 3 startet bei 30; 30 + 15 = 45 -> 45 % 40 = 5
    assert absolut(3, 15) == 5


def test_rot_trifft_gelb():
    # Rot (0) auf 23 und Gelb (2) auf 3 stehen auf demselben Feld
    assert absolut(0, 23) == absolut(2, 3)


def test_fertig():
    pos = startzustand()
    assert not fertig(pos, 0)
    pos[0] = [40, 41, 42, 43]
    assert fertig(pos, 0)
    pos[0] = [40, 41, 42, 39]
    assert not fertig(pos, 0)


def test_neue_position_haus_mit_6():
    assert neue_position(HAUS, 6) == 0


def test_neue_position_haus_ohne_6():
    assert neue_position(HAUS, 4) is None


def test_neue_position_normaler_zug():
    assert neue_position(12, 4) == 16


def test_neue_position_ueber_das_ziel_hinaus():
    # 41 + 3 = 44 liegt hinter dem letzten Zielfeld (43)
    assert neue_position(41, 3) is None


def test_neue_position_von_der_bahn_ins_ziel():
    # 38 + 4 = 42 ist ein Zielfeld, ganz ohne Sonderregel
    assert neue_position(38, 4) == 42


def test_neue_position_genau_auf_letztes_zielfeld():
    # Grenzfall: 40 + 3 = 43 ist gerade noch erlaubt
    assert neue_position(40, 3) == 43
