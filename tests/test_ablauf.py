import numpy as np

from maedn import HAUS, Zug, wuerfeln, zug_ausfuehren


def leeres_brett():
    """Alle Figuren im Haus – praktisch, um gezielt Situationen aufzubauen."""
    return [[HAUS] * 4 for _ in range(4)]


# ---------- 3A: zug_ausfuehren ----------


def test_zug_ausfuehren_bewegt_figur():
    pos = leeres_brett()
    pos[0] = [5, 41, 42, 43]
    zug_ausfuehren(pos, 0, Zug(figur=0, von=5, nach=8))
    assert pos[0] == [8, 41, 42, 43]


def test_zug_ausfuehren_rauskommen():
    pos = leeres_brett()
    zug_ausfuehren(pos, 0, Zug(figur=1, von=HAUS, nach=0))
    assert pos[0] == [HAUS, 0, HAUS, HAUS]


def test_zug_ausfuehren_schlagen():
    pos = leeres_brett()
    pos[0] = [20, 41, 42, 43]
    pos[2] = [3, HAUS, HAUS, HAUS]
    zug_ausfuehren(pos, 0, Zug(figur=0, von=20, nach=23, geschlagen=(2, 0)))
    assert pos[0][0] == 23
    assert pos[2] == [HAUS, HAUS, HAUS, HAUS]


def test_zug_ausfuehren_andere_spieler_unveraendert():
    pos = leeres_brett()
    pos[0] = [5, 41, 42, 43]
    pos[1] = [7, HAUS, HAUS, HAUS]
    zug_ausfuehren(pos, 0, Zug(figur=0, von=5, nach=8))
    assert pos[1] == [7, HAUS, HAUS, HAUS]


# ---------- 3B: wuerfeln ----------


def test_wuerfeln_nur_1_bis_6():
    rng = np.random.default_rng(0)
    wuerfe = {wuerfeln(rng) for _ in range(1000)}
    assert wuerfe == {1, 2, 3, 4, 5, 6}


def test_wuerfeln_reproduzierbar():
    rng1 = np.random.default_rng(42)
    rng2 = np.random.default_rng(42)
    assert [wuerfeln(rng1) for _ in range(10)] == [wuerfeln(rng2) for _ in range(10)]


def test_wuerfeln_gibt_python_int_zurueck():
    assert type(wuerfeln(np.random.default_rng(0))) is int
