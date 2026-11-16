from maedn import HAUS, erster_zug, spiele, spielerzug


class FesteWuerfe:
    """Ersetzt den Zufallsgenerator im Test: liefert vorgegebene Würfe."""

    def __init__(self, wuerfe):
        self.wuerfe = list(wuerfe)

    def integers(self, low, high):
        return self.wuerfe.pop(0)


def leeres_brett():
    """Alle Figuren im Haus – praktisch, um gezielt Situationen aufzubauen."""
    return [[HAUS] * 4 for _ in range(4)]


def test_normaler_spielerzug():
    pos = leeres_brett()
    pos[0] = [5, 41, 42, 43]
    wuerfel = FesteWuerfe([3, 1])
    spielerzug(pos, 0, erster_zug, wuerfel)
    assert pos[0][0] == 8
    assert wuerfel.wuerfe == [1]  # nur ein Wurf verbraucht


def test_nach_6_nochmal():
    pos = leeres_brett()
    pos[0] = [5, 41, 42, 43]
    wuerfel = FesteWuerfe([6, 2, 1])
    spielerzug(pos, 0, erster_zug, wuerfel)
    assert pos[0][0] == 13  # 5 + 6 + 2
    assert wuerfel.wuerfe == [1]


def test_drei_versuche_ohne_figur_auf_bahn():
    pos = leeres_brett()
    wuerfel = FesteWuerfe([1, 2, 6, 4, 1])
    spielerzug(pos, 0, erster_zug, wuerfel)
    # 3. Versuch ist eine 6 -> raus auf 0, Zusatzwurf 4 -> Startfeld räumen
    assert pos[0] == [4, HAUS, HAUS, HAUS]
    assert wuerfel.wuerfe == [1]


def test_drei_fehlversuche():
    pos = leeres_brett()
    wuerfel = FesteWuerfe([1, 2, 3, 5])
    spielerzug(pos, 0, erster_zug, wuerfel)
    assert pos[0] == [HAUS, HAUS, HAUS, HAUS]
    assert wuerfel.wuerfe == [5]  # genau 3 Würfe verbraucht


def test_nur_ein_versuch_mit_figur_auf_bahn():
    pos = leeres_brett()
    pos[0] = [39, 43, HAUS, HAUS]  # 39 + 4 = 43 ist besetzt
    wuerfel = FesteWuerfe([4, 6])
    spielerzug(pos, 0, erster_zug, wuerfel)
    assert pos[0] == [39, 43, HAUS, HAUS]
    assert wuerfel.wuerfe == [6]  # kein zweiter Versuch


def test_nach_6_ohne_zug_nur_ein_weiterer_versuch():
    pos = leeres_brett()
    pos[0] = [39, 41, 42, 43]
    # 6: kein Zug möglich, aber Zusatzwurf. 3: wieder kein Zug -> Ende.
    # Die 1 (39 -> 40) darf NICHT mehr gewürfelt werden.
    wuerfel = FesteWuerfe([6, 3, 1])
    spielerzug(pos, 0, erster_zug, wuerfel)
    assert pos[0] == [39, 41, 42, 43]
    assert wuerfel.wuerfe == [1]


def test_spiel_endet_mit_sieger():
    assert spiele([erster_zug] * 4, seed=1) in {0, 1, 2, 3}


def test_spiel_reproduzierbar():
    assert spiele([erster_zug] * 4, seed=7) == spiele([erster_zug] * 4, seed=7)
